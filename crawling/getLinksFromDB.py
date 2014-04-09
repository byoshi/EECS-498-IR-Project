#!/usr/bin/python
import mysql.connector
import time
from Queue import Queue
from random import shuffle

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

    def get_page_links(self, id):
        self.cursor.execute("select pl_namespace, pl_title from pagelinks where pl_from=%s", (id, ))
        titles = []
        for r in self.cursor:
            if r[0] == 0:
                titles.append(r[1])

        ret = []
        for r in titles:
            page_id_title = self.get_page_id_from_title(r)
            if page_id_title is not None:
                ret.append(page_id_title)
                # print page_id, page_title

        return ret


def crawl():
    db = WikiDB()
    db.connect()

    links = {}
    page_nodes = []
    page_nodes_idx = 0
    page_links = []
    page_idx = 0

    visited = set()
    q = Queue()
    page_id_title = db.get_page_id_from_title("Lie_to_me")
    q.put((page_id_title[0], "Lie_to_me", None))

    stop_len = 10
    g_start = time.time()
    while not q.empty() and len(visited) < stop_len:
        start = time.time()
        page_id, page_title, from_id = q.get()

        # add node to page_nodes
        page_nodes.append(page_title)
        # add link to page_links
        if from_id is not None:
            page_links.append((from_id, page_nodes_idx))

        links = db.get_page_links(page_id)
        print len(links)
        visited.add(page_id)
        shuffle(links)
        for l in links:
            q.put((l[0], l[1], page_nodes_idx))

        # increament page_nodes index to next open slot
        page_nodes_idx += 1
        end = time.time()
        print len(visited), "last link:", end - start, "time left", (end - g_start)/len(visited) * stop_len


    print page_nodes
    print page_links

if __name__ == '__main__':
    crawl()
