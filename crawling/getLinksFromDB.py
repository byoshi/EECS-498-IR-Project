#!/usr/bin/python
import mysql.connector
import time
from collections import deque
from random import shuffle
import random
import json
import re
import io

class WikiDB:
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = mysql.connector.Connect(host="liyiying.com", user="irgroup", password="werethebest", database="wikipagelinks")
        self.cursor = self.db.cursor()

    def get_page_id_if_redirect(self, id):
        self.cursor.execute("select rd_namespace, rd_title from redirect where rd_from=%s", (id, ))

        idx = 0
        ret = None
        for r in self.cursor:
            if idx > 0:
                print "Error: more than 1 redirect"
            else:
                ret = r

            idx += 1

        if r[0] != 0:
            return None

        ret, title = self.get_page_id_from_title(r[1])
        return ret, title

    def get_page_id_from_title(self, title):
        self.cursor.execute("select page_id, page_is_redirect from page where page_namespace=0 and page_title=%s", (title, ))

        idx = 0
        ret = None
        for r in self.cursor:
            if idx > 0:
                print "Warning: page id not unique given page title"
            else:
                ret = r

            idx += 1
        
        if ret is None:
            pass
            # print "no result: ", title
        elif ret[1] == 1:
            # print "redirect:", title
            ret = self.get_page_id_if_redirect(ret[0])
        else:
            ret = ret[0], title

        return ret

    def get_in_links(self, title):
        self.cursor.execute("select pl_from from pagelinks where pl_namespace=0 and pl_title=%s", (title, ))
        ids = []
        for r in self.cursor:
            ids.append(r)

        return ids
    
    
    def get_num_in_links(self, title):
        self.cursor.execute("select count(*) from pagelinks where pl_namespace=0 and pl_title=%s", (title, ))
        ret = 0
        for r in self.cursor:
            ret = r

        return ret[0]


    def get_num_out_links(self, id):
        self.cursor.execute("select count(*) from pagelinks where pl_from=%s", (id, ))
        ret = 0
        for r in self.cursor:
            ret = r

        return ret[0]

    def get_page_links(self, id):
        self.cursor.execute("select pl_namespace, pl_title from pagelinks where pl_from=%s", (id, ))
        titles = []
        for r in self.cursor:
            if r[0] == 0:
                titles.append(r[1])

        ret = titles
        # for r in titles:
        #    page_id_title = self.get_page_id_from_title(r)
        #    if page_id_title is not None:
        #        ret.append(page_id_title)
        #        # print page_id, page_title

        return ret


def crawl():
    db = WikiDB()
    db.connect()

    links = {}
    page_nodes = []
    page_ids = []
    page_links = []
    page_degree = []
    page_idx = 0

    visited = set()
    q = deque()
    start_page = "World_War_II"
    # page_id_title = db.get_page_id_from_title(start_page)
    q.append((start_page, None, 0))

    stop_len = 500
    g_start = time.time()
    degree = 0
    while len(q) > 0 and len(visited) < stop_len and degree < 6:
        start = time.time()
        page_title, from_id, degree = q.popleft()

        
        # check if page exists or is a redirect
        page_id_title = db.get_page_id_from_title(page_title)
        if page_id_title is not None:
            page_id = page_id_title[0]

            # add node to page_nodes
            if page_title not in page_nodes:
                page_nodes.append(page_title)
                page_ids.append(page_id)

            # get index
            page_nodes_idx = page_nodes.index(page_title)

            # add degree
            if page_nodes_idx >= len(page_degree):
                page_degree.insert(page_nodes_idx, degree)

            # add link to page_links regardless of if we seen it, could be a reverse arrow
            if from_id is not None:
                page_links.append((from_id, page_nodes_idx))

            # don't crawl for links if we've already crawled for links
            if page_id not in visited:
                links = db.get_page_links(page_id)
                visited.add(page_id)
       
                # links come in alphabetical order need to shuffle here
                shuffle(links)
                for l in links:#[:10]:
                    q.append((l, page_nodes_idx, degree + 1))

        end = time.time()
        print "Links: {0:5} Degree: {1:2} Num_Links: {2:5} Last (s): {3:8.5f} Q size: {4:6}, Time left: {5:10.5f}".format( \
            len(visited), degree, len(links), end - start, len(q), (end - g_start)/len(visited) * (stop_len - len(visited)))
   
    json_dict = {"nodes": [], "links": []}

    clusters = [None]*10

    for i, pn in enumerate(page_nodes):
        cluster_idx = page_degree[i]#random.randint(0, 9)
        c_check = clusters[cluster_idx]
        d_temp = {"name": re.sub("_", " ", pn), "cluster": cluster_idx}
        if c_check is None:
            d_temp["clusterCenter"] = True
            clusters[cluster_idx] = cluster_idx

        if i == 0:
            d_temp["root"] = True

        json_dict["nodes"].append(d_temp)

    links_file = open("links", "w")

    for pl in page_links:
        json_dict["links"].append({"source": pl[0], "target": pl[1]})
        links_file.write(str(pl[0]) + " " + str(pl[1]) + "\n")

    links_file.close()

    outfile = io.open("out.json", "wb") 
    outfile.write(json.dumps(json_dict, ensure_ascii=False))
    

    articlesToGetFile = open("articles", "w")
    for pn in page_nodes:
        articlesToGetFile.write(pn + "\n")

    articlesToGetFile.close()

    # page rank estimate
    page_ranks = [0]*len(page_nodes)
    for i, pn in enumerate(page_nodes):
        NumInLinks = db.get_num_in_links(pn)
        # print pn, NumInLinks
        pr = NumInLinks
        # for l_id in InLinks:
        #     numOutLinks = db.get_num_out_links(l_id[0])
        #     pg += 1.0/numOutLinks
        page_ranks[i] = pr

    sort_pr = []
    pageRankFile = open("pagerank", "w")
    for i, pn in enumerate(page_nodes):
        # print pn, page_ranks[i]
        sort_pr.append((pn, page_ranks[i]))
        pageRankFile.write(str(page_ranks[i]) + "\n")

    pageRankFile.close()

    sort_pr.sort(key=lambda tup: tup[1], reverse=True)
    for l in sort_pr[:10]:
        print l

if __name__ == '__main__':
    crawl()
