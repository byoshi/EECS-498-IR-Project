#!/usr/bin/python
import numpy
import random
#import PyCluster # is this available??

#n obervations into k clusters
#obervations belong to cluster which the nearest mean (mean serves as prototype)

#Lloyd's algorithm: assignment step; update step

def euclidean_dist(point1, point2):
    #print "point1: %s point2: %s" % (point1, point2)
    dist = numpy.linalg.norm(point1-point2)
    return dist

def find_closest_mean(coord, mean_values, mean_clusters):
    min_dist = 1000000000
    new_mean = -1
    for index in mean_clusters:
        dist = euclidean_dist(mean_values[index], coord)
        if dist < min_dist:
            min_dist = dist
            new_mean_index = index

    return new_mean_index

def initial_classify(num_clusters, coordinates):
    mean_clusters = dict()
    for index in range(0, num_clusters):
        mean_clusters[index] = set()

    empty_list = [0.] * len(coordinates)
    coord_classification = numpy.array(empty_list, dtype=float)

    #randomlly cluster vectors
    index = 0
    for coord in coordinates:
        new_mean_index = random.randint(0, num_clusters-1)
        coord_classification[index] = new_mean_index
        mean_clusters[new_mean_index].add(index)
        index += 1

    return mean_clusters, coord_classification

    
#for each coordinate
#calculate Euclidean distance to each mean
#classify coordinate as part of cluster with least distance to the mean
#after inital time count how many coordinates change groups
def classify_coords(mean_values, mean_clusters, coord_classification, coordinates):
    num_changes = 0

    index = 0
    for coord in coordinates:
        new_mean_index = find_closest_mean(coord, mean_values, mean_clusters)

        if new_mean_index != coord_classification[index]:
            old_mean_index = coord_classification[index]
            coord_classification[index] = new_mean_index
            mean_clusters[old_mean_index].discard(index) #remove coord from old mean
            mean_clusters[new_mean_index].add(index) #add cord to new mean
            num_changes += 1

        index += 1

    #GREAT DEBUG print "num_changes: %d" % (num_changes)
    return num_changes

#recalculate mean based on points in the cluster
def recalculate_means(mean_values, mean_clusters, coordinates):
    for mean_index in mean_clusters:
        coord_index_set = mean_clusters[mean_index]
        empty_list = [0.] * len(coordinates[0])
        summation = numpy.array(empty_list, dtype=float)

        for coord_index in coord_index_set:
            summation += coordinates[coord_index]

        if len(mean_clusters[mean_index]) > 0:
            summation = summation/len(coord_index_set)

        #print "old means: %s len: %d" % (mean_values[mean_index], len(mean_values[mean_index]))
        #print "summation: %s len: %d" % (summation, len(summation))
        mean_values[mean_index] = summation

    return mean_values

def kmeans(num_clusters, coordinates):
    empty_list = [0.]*len(coordinates[0])
    zeroed_cluster_means = list()
    for index in range(0, num_clusters):
        zeroed_cluster_means.append(empty_list)

    mean_values = numpy.array(zeroed_cluster_means, dtype=float)
    #print "inital mean_values: %s" % (mean_values)

    # classify coordinates into the initial groups randomly
    mean_clusters, coord_classification = initial_classify(num_clusters, coordinates)

    #print "initial classification: %s" % (coord_classification)
    #print "mean_clusters: %s" % (mean_clusters)

    num_changes = 1

    #while more than one coordinate changes clusters and less than max iterations:
    iteration = 0
    while num_changes > 0 and iteration < 10000:
        #recalculate mean values based on points in the cluster
        mean_values = recalculate_means(mean_values, mean_clusters, coordinates)
        #GREAT DEBUG print "recalculated means: %s" % (mean_values)

        #classify each coordinate as part of cluster with least distance to the mean
        num_changes = classify_coords(mean_values, mean_clusters, coord_classification, coordinates)

        iteration += 1

    #end while

    return mean_values, mean_clusters, coord_classification

def main():

    data_path = 'coordinates.in'

    num_clusters = 2

    data_file = open(data_path, 'r')
    data_contents = data_file.read()
    pairs = data_contents.split('\n')

    #coordinates = dict(p.split(' ', 1) for p in pairs)

    coordinates = list()
    #convert pairs to numpy.array(pair)
    for pair in pairs:
        coord = pair.strip().split()
        coordinates.append(coord)

    coordinates = numpy.array(coordinates, dtype=float)
    #GREAT DEBUG print "inital vectors: %s" % (coordinates)

    mean_values, mean_clusters, coord_to_mean = kmeans(num_clusters, coordinates)

    for index in mean_clusters:
        print "mean: %s" % (mean_values[index])
        print "values: "
        for value in mean_clusters[index]:
            print coordinates[value]

if __name__ == '__main__':
    main()