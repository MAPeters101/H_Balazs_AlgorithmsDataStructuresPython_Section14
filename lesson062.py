
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

    def remove(self, data):
        if self.root:
            self.remove_node(data, self.root)

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

    def remove_node(self, data, node):

        if node is None:
            return

        if data < node.data:
            self.remove_node(data, node.left_node)
        elif data > node.data:
            self.remove_node(data, node.right_node)
        else:
            # We found the node we want to remove
            # Case 1:) If the node is a leaf node
            if node.left_node is None and node.Right_node is None:
                print("Removing a leaf node...%d" % node.data)
                parent = node.parent

                if parent is not None and parent.left_node == node:
                    parent.left_node = None
                if parent is not None and parent.right_node == node:
                    parent.right_node = None

                if parent is None:
                    self.root = None

                del node

                # After every removal WE HAVE TO CHECK whether the AVL properties are violated
                self.handle_violation(parent)

            # Case 2:) If the node has a single child
            if node.left_node is None and node.right_node is not None:  # node!!!
                print("Removing a node with single right child...%d" % node.data)
                parent = node.parent

                if parent is not None:
                    if parent.left_node == node:
                        parent.left_node = node.right_node
                    if parent.right_node == node:
                        parent.right_node = node.right_node
                else:
                    self.root = node.right_node

                node.right_node.parent = parent
                del node

                # After every removal WE HAVE TO CHECK whether the AVL properties are violated
                self.handle_violation(parent)

            if node.right_node is None and node.left_node is not None:  # node!!!
                print("Removing a node with single left child...%d" % node.data)
                parent = node.parent

                if parent is not None:
                    if parent.left_node == node:
                        parent.left_node = node.left_node
                    if parent.right_node == node:
                        parent.right_node = node.right_node
                else:
                    self.root = node.left_node

                node.left_node.parent = parent
                del node

                # After every removal WE HAVE TO CHECK whether the AVL properties are violated
                self.handle_violation(parent)
            # Case 3: The node has 2 children
            else:
                print('Removing node with two children....')

                predecessor = self.get_predecessor(node.left_node)

                temp = predecessor.data
                predecessor.data = node.data
                node.data = temp

                self.remove(data.predecessor)

    def get_predecessor(self, node):
        if node.right_node:
            return self.get_predecessor(node.right_node)

        return node

    def calc_height(self, node):
        # this is when the node is a NULL
        if node is None:
            return -1

        return node.height

    def calculate_balance(self, node):

        if node is None:
            return 0

        return self.calc_height(node.left_node) - self.calc_height(node.right_node)
