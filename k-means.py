
import numpy
import random
#import PyCluster # is this available??

#n obervations into k clusters
#obervations belong to cluster which the nearest mean (mean serves as prototype)

#Lloyd's algorithm: assignment step; update step

def convert_list_to_string(coord):
    string = str(coord[0])
    first = 1
    for num in range(0, len(coord)):
        if first == 1:
            first = 0
            continue
        string = string + ' ' + str(coord[num])

    return string

def euclidean_dist(point1, point2):
    #dist = numpy.sqrt(numpy.sum(point1-point2)**2)
    #GREAT DEBUG print "point1: %s point2: %s" % (point1, point2)

    p1 = numpy.array(point1, dtype=float)
    p2 = numpy.array(point2, dtype=float)
    dist = numpy.linalg.norm(p1-p2)
    #print "dist: %d" % (dist)
    return dist

def find_closest_mean(coord, mean_values, mean_clusters):
    min_dist = 1000000000
    new_mean = -1
    for index in mean_clusters:
        dist = euclidean_dist(mean_values[index].split(), coord)
        if dist < min_dist:
            min_dist = dist
            new_mean_index = index

    return new_mean_index

def initial_classify(num_clusters, coordinates):
    #initialize mean_clusters [map mean index to set of coord pairs]
    mean_clusters = dict()
    for index in range(0, num_clusters):
        mean_clusters[index] = set()

    #coord_classification dict [map coord to mean]
    coord_classification = dict()

    index = 0
    #randomlly cluster vectors
    for coord in coordinates:
        #new_mean_index = find_closest_mean(coord, mean_values, mean_clusters)
        new_mean_index = random.randint(0, num_clusters-1)
        coord_classification[convert_list_to_string(coord)] = new_mean_index
        mean_clusters[new_mean_index].add(convert_list_to_string(coord))
        #print "converted coord to store: %s" % (convert_list_to_string(coord))

    return mean_clusters, coord_classification

#find num_means points that are furthest from each other (Euclidean distance)
def initial_means(num_means, coordinates):
    mean_values = dict()
    #for index in range(0, len(means)):
    #    means_values[index]
    
    #pick initial means
    mean_1 = [1, 1]
    mean_2 = [3, 4]
    mean_values[0] = convert_list_to_string(mean_1)
    mean_values[1] = convert_list_to_string(mean_2)
    
    #for each coordinate calculate distance to each other coordinate; set pair to be centers
    #repeat until have num_clusters number of points?? OR CHOSE RANDOMLY...

    return mean_values

def classify_coords(mean_values, mean_clusters, coord_classification):
    num_changes = 0

    for key_coord in coord_classification:
        new_mean_index = find_closest_mean(key_coord.split(), mean_values, mean_clusters)

        if new_mean_index != coord_classification[key_coord]:
            old_mean_index = coord_classification[key_coord]
            coord_classification[key_coord] = new_mean_index
            mean_clusters[old_mean_index].discard(key_coord) #remove coord from old mean
            mean_clusters[new_mean_index].add(key_coord) #add cord to new mean
            #print "converted coord to store: %s" % (convert_list_to_string(coord))
            #print "coord to store in mean_clusters: %s " % (key_coord)
            num_changes += 1
    
    #for each coordinate
        #calculate Euclidean distance to each mean
        #classify coordinate as part of cluster with least distance to the mean
        #after inital time count how many coordinates change groups

    #GREAT DEBUG print "num_changes: %d" % (num_changes)
    return num_changes

def recalculate_means(mean_values, mean_clusters, coord_len):

    #for each mean
    for index in mean_clusters:
        #recalculate mean based on points in the cluster
        summation = [0.] * coord_len
        for coord in mean_clusters[index]:
            coord = coord.split()
            i = 0
            for num in coord:
                summation[i] += float(num)
                i += 1

        normalized = summation
        if len(mean_clusters[index]) > 0:
            i = 0
            for sum_val in summation:
                normalized[i] = sum_val/len(mean_clusters[index])
                i += 1

        mean_values[index] = convert_list_to_string(normalized)
        #print "new mean: %s" % (mean_values[index])

    return mean_values



def kmeans(num_clusters, coordinates):
    # initial means = find furthest points from each other - Euclidean distance 
    #mean_values = initial_means(num_clusters, coordinates)
    vector_len = len(coordinates[0])
    mean_values = dict()
    for index in range(0, num_clusters):
        mean_values[index] = [0.] * vector_len
    # classify coordinates into the initial groups randomly
    mean_clusters, coord_classification = initial_classify(num_clusters, coordinates)

    num_changes = 1

    #while more than one coordinate changes clusters:
    while num_changes > 0:
        #recalculate mean values based on points in the cluster
        mean_values = recalculate_means(mean_values, mean_clusters, vector_len)
        #GREAT DEBUG print "recalculated means: %s" % (mean_values)

        #classify each coordinate as part of cluster with least distance to the mean
        num_changes = classify_coords(mean_values, mean_clusters, coord_classification)

    #end while

    return mean_values, mean_clusters, coord_classification

def main():

    data_path = '/afs/umich.edu/user/e/m/emjansen/EECS498/EECS-498-IR-Project/coordinates.in'

    num_clusters = 2

    data_file = open(data_path, 'r')
    data_contents = data_file.read()
    pairs = data_contents.split('\n')

    #coordinates = dict(p.split(' ', 1) for p in pairs)

    coordinates = list()
    #convert pairs to numpy.array(pair)
    for pair in pairs:
        coord = pair.split()
        #print "coord: %s" % (str(coord))
        coordinates.append(coord)

    mean_values, mean_clusters, coord_to_mean = kmeans(num_clusters, coordinates)

    for index in mean_clusters:
        print "mean: %s" % (mean_values[index])
        print "values: %s" % (mean_clusters[index])

if __name__ == '__main__':
    main()