#!/usr/bin/python

from tree import *
import collections

def find_lowest_degrees(tree, to_links, parent_roots, rankings_by_index):

    #print '======== Find Lowest Degrees =========='

    ranking_subset = list()
    for link in to_links:
        #temp = [int(rankings_list[index]), index]
        #next = tuple(temp)
        ranking_subset.append(rankings_by_index[link])

    ranking_subset.sort(key=lambda tup: tup[1])


    #print '============ Rankings Subset Sorted =============='
    #print ranking_subset

    roots_inserted_into = list()
    new_parents = list()

    for rank in ranking_subset:
        #if rank[1] not in tree.nodes.keys():
            #break;
        roots_to_check = tree.get_roots_of_nodes(rank[1])
            
        for root in roots_to_check:
            if root not in roots_inserted_into:
                new_parents.append(rank[1])
                roots_inserted_into.append(root)

        if len(roots_inserted_into) == len(parent_roots):
            break

    #link_node = tree.get_node(to_link_index)

    return new_parents        



def build_tree(articles, rankings, links, rankings_by_index):
    tree = Tree()

    for index in range(0, len(rankings)):
        #find a root node - high ranking with no articles ranked higher
        highest_rank_index = rankings[index]

        if highest_rank_index[1] in links:
            to_links = links[highest_rank_index[1]]
        else:
            to_links = set()

        print "Classify: ", articles[highest_rank_index[1]]

        nodes_to_find_roots = list()

        #print tree.nodes.keys()

        for to_link_index in to_links:
            #print "look for link: ", to_link_index, tree.nodes.keys(), to_link_index in tree.nodes.keys()

            if to_link_index in tree.nodes.keys():
                #print '==== LINK FOUND! ======== ' #, articles[int(to_link_index)]
                nodes_to_find_roots.append(to_link_index)

       # print "nodes_found: ", nodes_to_find_roots
        
        parent_roots = list()
        if len(nodes_to_find_roots) > 0:
            parent_roots = tree.get_roots_of_nodes(nodes_to_find_roots)
            #print "parent's roots found: ", parent_roots

        #find lowest degree with different roots
        if len(parent_roots) > 0:
            #for root_index in parent_roots:
            new_parents = find_lowest_degrees(tree, nodes_to_find_roots, parent_roots, rankings_by_index)

            for p in new_parents:
                print '========== Add node with parent %s %s ========' % (p, tree.get_node(p).get_value())
                tree.add_node(highest_rank_index[1], articles[highest_rank_index[1]], p)
            #tree.add_node(highest_rank_index[1], articles[highest_rank_index[1]], new_parents)
        else:
            print '==== LINK NOT FOUND - Add New Root ====='
            tree.add_node(highest_rank_index[1], articles[highest_rank_index[1]])

        #EXAMPLE trees[0].create_node("tree0", "tree0")  # root node
        #EXAMPLE trees[0].create_node("Jane", "jane", parent = "tree0")

        #trees[0].show(0)

    return tree


def run():
    articles_path = 'articles_test'
    articles_file = open(articles_path, 'r')
    articles = articles_file.read().split('\r\n')
    
    rankings_path = 'pagerank_test'
    rankings_file = open(rankings_path, 'r')
    rankings_list = rankings_file.read().split()

    rankings_by_index = list()
    for index in range(0, len(rankings_list)):
        #print 'ranking at index: ', rankings_list[index]
        temp = [int(rankings_list[index]), index]
        next = tuple(temp)
        rankings_by_index.append(next)

    rankings = sorted(rankings_by_index, key=lambda tup: tup[0])
    rankings.reverse()


    #print '====== Rankings by index ========'
    #print rankings_by_index

    #print '=========== Rankings ==========='
    #print rankings

    links_path = 'links_test'
    links_file = open(links_path, 'r')
    links_list = links_file.read().split('\n')

    links = dict()
    for link in links_list:
        link_parts = link.split()
        link_source = int(link_parts[0])
        link_target = int(link_parts[1])
        if link_source not in links:
            links[link_source] = set()
        links[link_source].add(link_target)

    #print '============ Links ==========='
    #print links

    tree = build_tree(articles, rankings, links, rankings_by_index)


    '''print '========== Roots ==========='
    roots = tree.get_roots().values()
    for root in roots:
        #print 'root key: ', root
        #ode =  tree.get_node(root)
        print root.get_value()
        print 'num_children: ', len(root.get_children())
    '''

    print '======== Trees ==========='
    tree.show()


if __name__ == '__main__':
    run()
