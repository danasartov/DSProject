# id1:
# name1:
# username1:
# id2:
# name2:
# username2:


"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.key is not None


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """

    def __init__(self, is_avl):
        self.root = None
        self.is_avl = is_avl

        # Create a single virtual node, which will be used as the left and right child of all leaf nodes.
        self.virtual_node = AVLNode(None, None)

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        node = self.root
        search_time = 0
        while node.value is not None:
            search_time += 1
            if node.key == key:
                return node, 0
            elif node.key > key:
                node = node.left
            else:
                node = node.right
        return None, -1

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int,int)
    @returns: a 4-tuple (x, search_time, rotations, height_changes), where x is the new node
    and the other 3 return values are as defined and explained in the assignment.
    """

    def insert(self, key, val):
        return None, -1, -1, -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        # if node is a leave
        if node.left.key is None and node.right.key is None:
            # if node is root
            if node.parent is None:
                self.root = None
            else: 
                if node.parent.left == node:
                    node.parent.left = self.virtual_node
                else:
                    node.parent.right = self.virtual_node
                del node

                # if tree is AVL, do rotations and height updates
                if self.is_avl:
                    A = node.parent
                    A_BF = A.left.height - A.right.height
                    while A != self.root:
                        A_left_son_BF = A.left.left.height - A.left.right.height
                        A_right_son_BF = A.right.left.height - A.right.right.height
                        if A_BF == 2:
                            if A_left_son_BF == -1:
                                self.left_rotation(A.left)
                                self.right_rotation(A)
                            else: 
                                self.right_rotation(A)
                        if A_BF == -2:
                            if A_right_son_BF == 1:
                                self.right_rotation(A.right)
                                self.left_rotation(A)
                            else: 
                                self.left_rotation(A)
        # if node has one son

        # if node has 2 sons



    def left_rotation(self, A):
        B = A.right
        # if A is root
        if A.parent is None: 
            self.root = B
        elif A.parent.left == A: # A is left son
            A.parent.left = B
        else: # A is right son
            A.parent.right = B
        A.right = B.left
        B.left = A

        # update heights
        A.height = max(A.left.height, A.right.height) + 1
        B.height = max(B.left.height, B.right.height) + 1

    def right_rotation(self, A): # A BF is +2
        B = A.left
        # if A is root
        if A.parent is None: 
            self.root = B
        elif A.parent.left == A: # A is left son
            A.parent.left = B
        else: # A is right son
            A.parent.right = B
        A.left = B.right
        B.right = A

        # update heights
        A.height = max(A.left.height, A.right.height) + 1
        B.height = max(B.left.height, B.right.height) + 1

            
                


                    


        return

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        return None

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return -1

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return None

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        return -1
