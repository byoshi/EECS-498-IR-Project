#!/usr/bin/python

from tree import *
import collections


def build_tree(articles, rankings, links):
    trees = dict()

    print '=========== Rankings ==========='
    print rankings

    for index in range(0, len(rankings)):
        #find a root node - high ranking with no articles ranked higher
        highest_rank_index = rankings[index]

        to_links = links[str(highest_rank_index[1])]

        print "Link to classify: ", highest_rank_index[1]

        node_inserted = False

        for tree in trees.values():
            for to_link_index in to_links:
                if articles[int(to_link_index)] in tree:
                    print '==== LINK FOUND! ========'
                    node_inserted = True

                    #TODO this is broken and results in infinite recursion
                    tree.create_node(highest_rank_index[1], articles[highest_rank_index[1]], parent = articles[int(to_link_index)])

                    tree.show(0)


        if node_inserted == False:
            print '==== LINK NOT FOUND ====='
            new_tree_index = len(trees)
            new_tree = Tree()
            new_tree.create_node("tree" + str(new_tree_index), "tree" + str(new_tree_index))
            new_tree.create_node(highest_rank_index[1], articles[highest_rank_index[1]], parent = "tree"+str(new_tree_index))
            trees[new_tree_index] = new_tree

        #EXAMPLE trees[0].create_node("tree0", "tree0")  # root node
        #EXAMPLE trees[0].create_node("Jane", "jane", parent = "tree0")

        trees[0].show(0)

    return trees


def run():
    articles_path = 'articles_test'
    articles_file = open(articles_path, 'r')
    articles = articles_file.read().split('\r\n')
    
    rankings_path = 'pagerank_test'
    rankings_file = open(rankings_path, 'r')
    rankings_list = rankings_file.read().split()

    #TODO: Use list of tuples instead?? what if two have same ranking???
    rankings = list()
    for index in range(0, len(rankings_list)):
        #print 'ranking at index: ', rankings_list[index]
        temp = [int(rankings_list[index]), index]
        next = tuple(temp)
        rankings.append(next)

    rankings.sort(key=lambda tup: tup[0])
    rankings.reverse()

    #print '======== Ordered Rankings ========: ', rankings

    links_path = 'links_test'
    links_file = open(links_path, 'r')
    links_list = links_file.read().split('\n')

    links = dict()
    for link in links_list:
        link_parts = link.split()
        link_source = link_parts[0]
        link_target = link_parts[1]
        if link_source not in links:
            links[link_source] = set()
        links[link_source].add(link_target)

    print '============ Links ==========='
    print links

    trees = build_tree(articles, rankings, links)

    print '======== Trees ==========='

    for index in range(0, len(trees)):
        print 'tree num: %s root: %s' % (index, trees[index].get_index(0))
        trees[index].show(0)


if __name__ == '__main__':
    run()
