import numpy as np
import random
import time

#n obervations into k clusters
#obervations belong to cluster which the nearest mean (mean serves as prototype)

#Lloyd's algorithm: assignment step; update step

def calc_means(data, c, k):
    n, m = data.shape
    means = np.zeros((k, m), dtype=float)
    for i in xrange(k):
        if len(data[np.where(c == i)[0], :]) > 0:
            means[i, :] = np.mean(data[np.where(c == i)[0], :], 0)

    return means

def cosSim(data1, data2):
    n1, m1 = data1.shape
    n2, m2 = data2.shape

    if m1 != m2:
        print "Error: dimension mismatch for dist 2, data1 has to be mxn and data2 has to be kxn"
    
    dists = np.zeros((n1, n2), dtype=float)

    for x in xrange(n1):
        for y in xrange(n2):
            x1 = data1[x, :]
            x2 = data2[y, :]
            # print x, y, np.linalg.norm(x1), np.linalg.norm(x2)
            dists[x, y] = np.inner(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))

    return -dists

def dist2(data1, data2):
    n1, m1 = data1.shape
    n2, m2 = data2.shape

    if m1 != m2:
        print "Error: dimension mismatch for dist 2, data1 has to be mxn and data2 has to be kxn"

    a = np.dot(np.ones((n2, 1), dtype=float), np.sum(np.power(data1, 2).T, axis=0).reshape(1, n1)).T
    b = np.dot(np.ones((n1, 1), dtype=float), np.sum(np.power(data2, 2).T, axis=0).reshape(1, n2))
    c = -2*np.dot(data1, data2.T)

    ret = a + b + c
    return ret

def kmeans(data, k, dist_fn=dist2):
    print "### START K-MEANS ###"
    start = time.time()
    n, m = data.shape

    c = np.ones((n, 1), dtype=float)

    # for i in xrange(n):
    #     # c[i] = i % k
    #     # c[i] = random.randint(0, k - 1)
    #     c[i] = int(i/(n/k))

    # means = calc_means(data, c, k)
    
    list_of_means = []
    start_center = random.randint(0, n)
    list_of_means.append(data[start_center, :])

    print start_center
    for i in xrange(k - 1):
        means = np.array(list_of_means, dtype=float)
        dists = dist_fn(data, means)
        # print dists, dists.shape
        # print np.min(dists, axis=1)
        next_center = np.argmax(np.min(dists, axis=1))
        list_of_means.append(data[next_center, :])
        print next_center

    means = np.array(list_of_means, dtype=float)

    count = 0
    while True:
        dists = dist_fn(data, means)
        c = np.argmin(dists, axis=1)

        means2 = calc_means(data, c, k)
        check = np.linalg.norm(means**2 - means2**2)
        means = means2

        print dists
        
        count += 1
        print "Iterations: {0:5} Time (s): {1:9.5f} Diff: {2:11.5f}".format(count, time.time() - start, check)
        if check == 0 or count > 10000:
            break;

    # print "======= Means ======="
    # print means
    print "===== Clusters ======"
    print c
    print "======= Stats ======="
    print "Iterations:", count, "Time (s):", time.time() - start
    print "#### END K-MEANS ####"
    return c

def main():
    data_path = 'k_means_input'

    # number of clusters
    data_file = open(data_path, 'r')
    data_contents = data_file.read()
    pairs = data_contents.split('\n')

    #convert pairs to numpy.array(pair)
    for pair in pairs:
        coord = pair.split()

    for i, p in enumerate(pairs):
        pairs[i] = p.strip().split(" ")

    if len(pairs[-1]) < pairs[1]:
        del pairs[-1]

    data = np.array(pairs, dtype=float)

    k = 20
    # c = kmeans(data, k)
    c = kmeans(data, k, cosSim)

    article_names = 'article_names.txt'
    names_file = open(article_names)
    names = names_file.read().split('\n')

    for i in xrange(k):
        print "============== CLUSTER: ", i, "============="
        for j in np.where(c == i)[0]:
            print names[int(j)]

if __name__ == '__main__':
    main()
