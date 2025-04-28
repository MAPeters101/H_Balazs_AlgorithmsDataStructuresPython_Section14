
class Node:

    def __init__(self, data, parent):
        self.data = data
        self.left_node = None
        self.right_node = None
        self.parent = parent
        self.height = 0


class AVLTree:

    def __init__(self):
        # We can access the root node exclusively
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data, None)
        else:
            self.insert_node(data, self.root)

    def insert_node(self, data, node):

        # We have to consider the left subtree
        if data < node.data:
            # We have to check if the left node is a None
            # When the left child is not a None
            if node.left_node:
                self.insert_node(data, node.left_node)
            else:
                node.left_node = Node(data, node)
                node.height = max(self.calc_height(node.left_node), self.calc_height(node.right_node) + 1)
        else:
            # We have to check if the right node is a None
            # When the right child is not a None
            if node.right_node:
                self.insert_node(data, node.right_node)
            else:
                node.right_node = Node(data, node)
                node.height = max(self.calc_height(node.left_node), self.calc_height(node.right_node) + 1)

        # After every insertion WE HAVE TO CHECK whether the AVL properties are violated
        self.handle_violation(node)





