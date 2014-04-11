#!/usr/bin/env python
import bow
import k_means_np
import numpy as np
import sys
import subprocess

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
    tf_dict_list, all_words = bow.tokenizeWiki(wiki_file.read(), stopwords_file)

    list_list = bow.bagOfWords(tf_dict_list, all_words)

    data = np.array(list_list, dtype=float)

    k = 3

    c = k_means_np.kmeans(data, k, k_means_np.cosSim)

    article_names = 'article_names.txt'
    names_file = open(article_names)
    names = names_file.read().split('\n')

    for i in xrange(k):
        print "============== CLUSTER: ", i, "============="
        for j in np.where(c == i)[0]:
            print names[int(j)]

    # print k_means_np.cosSim(data, data)