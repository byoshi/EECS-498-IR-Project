#tree implementation by Brett Kromkamp (via stackoverflow)

import uuid
from collections import deque
import json

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
        if parents is not None:
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
        print key, value, parents
        if key in self.nodes:
            node = self.nodes[key]
            if type(parents) is not list:
                node.add_parents(parents)
                self.nodes[parents].add_child(key)
            else:
                for p in parents:
                    node.add_parents(p)
                    self.nodes[p].add_child(key)  
            max_deg = 0;
            for p in node.get_parents():
                if self.nodes[p].get_degree() > max_deg:
                    max_deg = self.nodes[p].get_degree()
            degree = max_deg + 1
            node.degree = degree
        else:
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

    def get_roots_of_nodes(self, ni):
        d = deque()
        if type(ni) is not list:
            d.append(ni)
        else:
            for nii in ni:
                d.append(nii)
        roots = []

        while len(d) > 0:
            nii = d.popleft()
            if nii in self.roots:
                if nii not in roots:
                    roots.append(nii)
            node = self.get_node(nii)      
            for p in node.get_parents():
                if p is not None:
                    d.append(p)
        return roots

    def get_roots(self):
        return self.roots

    def get_node(self, key):
        return self.nodes[key]

    def show(self):
        d = deque()
        for ri in self.get_roots():
            d.append(ri)

        while len(d) > 0:
            ni = d.pop()
            node = self.get_node(ni)
            print "\t"*node.get_degree(), node.value
            for ci in node.get_children():
                d.append(ci)

    def json(self):
        json_dict = {"nodes": [], "links": []}
        keys = self.nodes.keys()
        values = [l.value for l in self.nodes.values()]
        degrees = [l.degree for l in self.nodes.values()]
        for k in keys:
            d_temp = {"name": self.get_node(k).value, "degree": self.get_node(k).degree + 1}
            json_dict["nodes"].append(d_temp)

        d = deque()
        for ri in self.get_roots():
            d.append(ri)

        while len(d) > 0:
            ni = d.pop()
            node = self.get_node(ni)
            nii = values.index(node.value)
            for ci in node.get_children():
                d.append(ci)
                cnode = self.get_node(ci)
                cii = values.index(cnode.value)
                json_dict["links"].append({"source": nii, "target": cii, "weight": 1})

        return json.dumps(json_dict, ensure_ascii=False, indent=4, separators=(',', ': '))

    def show_recursive(self):
        for ri in self.get_roots():
            self.show_recursive_helper(ri)

    def show_recursive_helper(self, ni):
        node = self.get_node(ni)
        if len(node.get_children()) == 0:
            print "\t"*node.get_degree(), node.value, str(node.get_parents()), str(node.get_children())

        i = 0
        for ci in node.get_children():
            if i == 0:
                print "\t"*node.get_degree(), node.value, str(node.get_parents()), str(node.get_children())
            self.show_recursive_helper(ci)
            i += 1

    def __getitem__(self, key):
        return self.nodes[key]

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, key):
        return key in self.nodes

if __name__ == "__main__":
    tree = Tree()
    tree.add_node("Ash", "ash")
    tree.add_node("Pikachu", "pikachu", "Ash")
    tree.add_node("Bruno", "bruno")
    tree.add_node("Erika", "erika")
    tree.add_node("Harry", "harry")  # root node
    tree.add_node("Jane", "jane", "Harry")
    tree.add_node("Bill", "bill", "Harry")
    tree.add_node("Joe", "joe", "Jane")
    tree.add_node("Diane", "diane", "Jane")
    tree.add_node("George", "george", "Diane")
    tree.add_node("Mary", "mary", "Diane")
    tree.add_node("Jill", "jill", "George")
    tree.add_node("Carol", "carol", "Jill")
    tree.add_node("Carol", "carol", ["Bruno", "Erika"])
    tree.add_node("Grace", "grace", "Bill")
    tree.add_node("Mark", "mark", "Jane")

    tree.show_recursive()
    tree.json()
    print tree.get_roots_of_nodes("Carol")
    print tree.get_roots_of_nodes(["Carol", "Bill", "Pikachu"])