from graphviz import Digraph
from algorithms.SearchTree import SearchTree
from algorithms.SearchTree import Node

def visualize_tree(tree: SearchTree):
    dot = Digraph()

    def add_nodes(node: Node):
        if node is None:
            return

        dot.node(str(id(node)), str(node.data))

        if node.left:
            dot.edge(str(id(node)), str(id(node.left.root)))
            add_nodes(node.left.root)

        if node.right:
            dot.edge(str(id(node)), str(id(node.right.root)))
            add_nodes(node.right.root)

    add_nodes(tree.root)

    dot.render("binary_tree", view=True, format="png")

#Right rotation test
tree = SearchTree(30)

tree.insert(20)
tree.insert(10)

#visualize_tree(tree)

#Left rotation test
tree = SearchTree(10)

tree.insert(20)
tree.insert(30)

#visualize_tree(tree)

#Left-Right rotation test
tree = SearchTree(30)

tree.insert(10)
tree.insert(20)

visualize_tree(tree)

#Right-Left rotation test
tree = SearchTree(10)

tree.insert(30)
tree.insert(20)

#visualize_tree(tree)

#Big tree test
import random
tree = SearchTree(50)

for v in random.sample(range(1,100), 25):
    tree.insert(v, balance=True)

visualize_tree(tree)