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
import math

if __name__ == "__main__":
    clusters_path = 'clusters'
    clusters_file = open(clusters_path, 'r')
    clusters = [int(i) for i in clusters_file.read().strip().split("\n")]
    

    k = 10
    ps = [0]*k
    for c in clusters:
        ps[c] += 1

    e = 0
    for p in ps:
        e -= p*1.0/len(clusters)*math.log(p*1.0/len(clusters), 2)

    print e
