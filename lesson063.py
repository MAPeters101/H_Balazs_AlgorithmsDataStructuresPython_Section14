
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

    def handle_violation(self, node):
        # Check the nodes from the node we have inserted up to root node
        while node is not None:
            node.height = max(self.calculate_height(node.left_node),
                              self.calculate_height(node.right_node)) + 1
            self.violation_helper()
            # Whenever we settle a violation (rotations) it may happen that it
            # violates the AVL properties in other part of the tree
            node = node.parent

    # Checks whether the subtree is balanced with root node = node
    def violation_helper(self, node):

        balance = self.calculate_balance(node)
        # OK, we know the tree is left heavy BUT it can be left-right heavy or left-left heavy
        if balance > 1:
            # left right heavy situation: left rotation on parent + right rotation on grandparent
            if self.calculate_balance(node.left_node) < 0:
                self.rotate_left(node.left_node)

            # this is the right rotation on grandparent ( if left-left heavy, that's a single right rotation)
            self.rotate_right(node)

        # OK, we know the tree is right heavy BUT it can be left-right heavy or right-right heavy
        if balance < -1:
            # right - left heavy so we need a right rotation before left rotation
            if self.calculate_balance(node.right_node) > 0:
                self.rotate_right(node.left_node)

            # left rotation
            self.rotate_left(node)

    def calc_height(self, node):
        # this is when the node is a NULL
        if node is None:
            return -1

        return node.height

    def calculate_balance(self, node):

        if node is None:
            return 0

        return self.calc_height(node.left_node) - self.calc_height(node.right_node)

    def traverse(self):
        if self.root is not None:
            self.traverse_in_order(self.root)

    def traverse_in_order(self, node):
        if node.left_node:
            self.traverse_in_order(node.left_node)

        l = ''
        r = ''
        p = ''

        if node.left_node is not None:
            l = node.left_node.data
        else:
            l = 'NULL'

        if node.right_node is not None:
            l = node.right_node.data
        else:
            l = 'NULL'

        if node.parent is not None:
            l = node.parent.data
        else:
            l = 'NULL'

        print("%s left: %s right: %s parent: %s height: %s" % (node.data, l, r, p, node.height))

        if node.right_node:
            self.traverse_in_order(node.right_node)

    def rotate_right(self, node):
        print("Rotating to the right on node ", node.data)

        temp_left_node = node.left_node
        t = temp_left_node.right_node

        temp_left_node.right_node = node
        node.left_node = t

        if t is not None:
            t.parent = node

        temp_parent = node.parent
        node.parent = temp_left_node
        temp_left_node.parent = temp_parent

        if temp_left_node.parent is not None and temp_left_node.parent.left_node == node:
            temp_left_node.parent.left_node = temp_left_node

        if temp_left_node.parent is not None and temp_left_node.parent.right_node == node:
            temp_left_node.parent.right_node = temp_left_node

        if node == self.root:
            self.root = temp_left_node

        node.height = max(self.calculate_height(node.left_node), self.calculate_height(node.right_node))
        temp_left_node.height = max(self.calculate_height(temp_left_node.left_node),
                                    self.calculate_height(temp_left_node.right_node)) + 1

    def rotate_left(self, node):
        print("Rotating to the left on node ", node.data)

        temp_right_node = node.right_node
        t = temp_right_node.left_node

        temp_right_node.left_node = node
        node.right_node = t

        if t is not None:
            t.parent = node

        temp_parent = node.parent
        node.parent = temp_right_node
        temp_right_node.parent = temp_parent

        if temp_right_node.parent is not None and temp_right_node.parent.left_node == node:
            temp_right_node.parent.left_node = temp_right_node

        if temp_right_node.parent is not None and temp_right_node.parent.right_node == node:
            temp_right_node.parent.right_node = temp_right_node

        if node == self.root:
            self.root = temp_right_node

        node.height = max(self.calculate_height(node.left_node), self.calculate_height(node.right_node))
        temp_right_node.height = max(self.calculate_height(temp_right_node.left_node),
                                    self.calculate_height(temp_right_node.right_node)) + 1




