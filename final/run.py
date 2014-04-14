#!/usr/bin/env python
import bow
import k_means_np
import numpy as np
import sys
import subprocess
import getLinksFromDB as linksdb
import time
import HTMLParser

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: ./run.py [wiki file xml]"
        sys.exit(1)

    wiki_file_name = sys.argv[1]

    print "cat " + wiki_file_name + " | python WikiExtractor.py -b 2000M"
    ret = subprocess.call("cat " + wiki_file_name + " | python WikiExtractor.py -b 2000M", shell=True)
    if ret:
        sys.exit(ret)

    stopwords_file = "stopwords.txt"

    wiki_file = open("AA/wiki_00", "r")
    tf_dict_list, all_words, names = bow.tokenizeWiki(wiki_file.read(), stopwords_file)

    # fixing links
    db = linksdb.WikiDB()
    db.connect()
    g_start = time.time()
    page_links = []
    for i, name in enumerate(names):
        start = time.time()
        name_unescapted = HTMLParser.HTMLParser().unescape(name)
        pi = db.get_page_id_from_title(name_unescapted)
        # print name, pi
        links = db.get_page_links(pi[0])
        count = 0
        for l in links:
            try:
                l_idx = names.index(l)
                # print page_nodes[page_ids.index(pi)], l
                count += 1
                page_links.append((i, l_idx))
            except:
                pass
        end = time.time()
        print "Added Links: {0:5} Last (s): {1:8.5f} Time left: {2:10.5f}".format( \
            count, end - start, (end - g_start)/(i + 1) * (len(names) - i - 1))

    links_file = open("links", "w")

    for pl in page_links:
        links_file.write(str(pl[0]) + " " + str(pl[1]) + "\n")

    links_file.close()

    # page rank estimate
    g_start = time.time()
    page_ranks = [0]*len(names)
    for i, pn in enumerate(names):
        start = time.time()
        NumInLinks = db.get_num_in_links(pn)
        # print pn, NumInLinks
        pr = NumInLinks
        # for l_id in InLinks:
        #     numOutLinks = db.get_num_out_links(l_id[0])
        #     pg += 1.0/numOutLinks
        page_ranks[i] = pr
        end = time.time()
        print "Last (s): {0:8.5f} Time left: {1:10.5f}".format( \
            end - start, (end - g_start)/(i + 1) * (len(names) - i - 1))

    sort_pr = []
    pageRankFile = open("pagerank", "w")
    for i, pn in enumerate(names):
        # print pn, page_ranks[i]
        sort_pr.append((pn, page_ranks[i]))
        pageRankFile.write(str(page_ranks[i]) + "\n")

    pageRankFile.close()
    # end fixing links


    list_list = bow.bagOfWords(tf_dict_list, all_words)

    data = np.array(list_list, dtype=float)

    k = 10

    c = k_means_np.kmeans(data, k, k_means_np.cosSim)

    clusters_names = 'clusters'
    clusters_file = open(clusters_names, 'w')
    for cluster in c:
        clusters_file.write(str(cluster) + '\n')
    clusters_file.close()

    for i in xrange(k):
        print "============== CLUSTER: ", i, "============="
        for j in np.where(c == i)[0]:
            print names[int(j)]
    # print k_means_np.cosSim(data, data)
