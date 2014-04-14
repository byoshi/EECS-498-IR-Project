#!/usr/bin/env python
import bow
import k_means_np
import numpy as np
import sys
import subprocess
import getLinksFromDB as linksdb
import time
import HTMLParser
import json

if __name__ == "__main__":
    articles_path = 'article_names.txt'
    articles_file = open(articles_path, 'r')
    articles = articles_file.read().strip().split("\n")
    
    clusters_path = 'clusters'
    clusters_file = open(clusters_path, 'r')
    clusters = [int(i) for i in clusters_file.read().strip().split("\n")]

    links_path = 'links'
    links_file = open(links_path, 'r')
    links_list = links_file.read().strip().split('\n')

    json_dict = {"nodes": [], "links": []}

    roots_file = open('roots', 'r')
    roots = roots_file.read().strip().split('\n')
    roots = [r.strip().split(' ') for r in roots]
    for i, r in enumerate(roots):
        roots[i] = [int(j) for j in r] 

    for i, pn in enumerate(articles):
        d_temp = {"name": pn, "cluster": clusters[i]};

        if i == 0:
            d_temp["root"] = True
        if i in roots[clusters[i]]:
            d_temp["clusterCenter"] = True

        json_dict["nodes"].append(d_temp)


    for l in links_list:
        lp = l.split()
        pl = (int(lp[0]), int(lp[1]))
        c1 = clusters[pl[0]]
        c2 = clusters[pl[1]]
        if c1 != c2:
            d_temp = {"source": pl[0], "target": pl[1], "weight": 1}
            json_dict["links"].append(d_temp)


    f = open("cluster.json", "w")

    f.write(json.dumps(json_dict, ensure_ascii=False, indent=4, separators=(',', ': ')))
