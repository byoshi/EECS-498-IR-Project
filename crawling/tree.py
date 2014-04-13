#tree implementation by Brett Kromkamp (via stackoverflow)

import uuid
from collections import deque

def sanitize_id(id):
    return id.strip().replace(" ", "")

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class Node:
    def __init__(self, value, parents, degree):
        if type(parents) is not list:
            p_l = [parents]
            self.parents = p_l
        else:
            self.parents = parents
        self.children = []
        self.value = value
        self.degree = degree

    def add_parents(self, parents):
        if type(parents) is not list:
            self.parents.append(parents)
        else:
            self.parents.extend(parents)

    def add_child(self, node_id):
        self.children.append(node_id)

    def get_props(self):
        return self.parents, self.children, self.value, self.degree

    def get_parents(self):
        return self.parents

    def get_children(self):
        return self.children

    def get_value(self):
        return self.value

    def get_degree(self):
        return self.degree

class Tree:
    def __init__(self):
        self.nodes = {}
        self.roots = {}

    def get_index(self, position):
        for index, node in enumerate(self.nodes):
            if node.identifier == position:
                break
        return index

    def add_node(self, key, value, parents=None, degree=0):
        if parents is None:
            degree = 0
        else:
            if type(parents) is not list:
                degree = self.nodes[parents].get_degree() + 1
            else:
                max_deg = 0;
                for p in parents:
                    if self.nodes[p].get_degree() > max_deg:
                        max_deg = p.get_degree()
                degree = max_deg + 1

        node = Node(value, parents, degree)
        self.nodes[key] = node

        if parents is None:
            self.roots[key] = node
        else:
            for p in node.get_parents():
                self.nodes[p].add_child(key)

        return node

    def get_roots(self):
        return self.roots

    def get_node(self, key):
        return self.nodes[key]

    def show(self):
        d = deque()
        for ri in self.get_roots():
            d.append(ri)

        while len(d) > 0:
            ni = d.popleft()
            node = self.get_node(ni)
            print "\t"*node.get_degree(), node.value
            for ci in node.get_children():
                d.append(ci)

    def __getitem__(self, key):
        return self.nodes[key]

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, key):
        return key in self.nodes

if __name__ == "__main__":

    tree = Tree()
    tree.add_node("Harry", "harry")  # root node
    tree.add_node("Jane", "jane", "Harry")
    tree.add_node("Bill", "bill", "Harry")
    tree.add_node("Joe", "joe", "Jane")
    tree.add_node("Diane", "diane", "Jane")
    tree.add_node("George", "george", "Diane")
    tree.add_node("Mary", "mary", "Diane")
    tree.add_node("Jill", "jill", "George")
    tree.add_node("Carol", "carol", "Jill")
    tree.add_node("Grace", "grace", "Bill")
    tree.add_node("Mark", "mark", "Jane")

    tree.show()