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
                return node, search_time
            elif node.key > key:
                node = node.left
            else:
                node = node.right
        return None, search_time + 1

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
        if self.root is None:
            new_node = AVLNode(key, val)
            new_node.left = self.virtual_node
            new_node.right = self.virtual_node
            new_node.parent = None
            new_node.height = 0
            self.root = new_node
            return new_node, 1, 0, 0
        
        parent = None
        node = self.root
        search_time = 0
        rotations=0
        height_changes=0
        while node.is_real_node():
            parent = node
            search_time += 1 
            if key < node.key:
                node = node.left
            else:
                node = node.right
        search_time += 2
        
        new_node = AVLNode(key, val)
        new_node.left = self.virtual_node
        new_node.right = self.virtual_node
        new_node.parent = parent 
        new_node.height = 0

        if key< parent.key:
            parent.left=new_node
        else:
            parent.right=new_node
        if not self.is_avl:
            return new_node, search_time, 0,0
        
        curr=parent
        while curr is not None and curr.is_real_node():
            old_height=curr.height
            new_height=max(curr.left.height, curr.right.height)+1
            bf=curr.left.height-curr.right.height
            
            if abs(bf)<2:
                if old_height==new_height:
                    break
                else:
                    curr.height=new_height
                    height_changes+=1
                    curr=curr.parent
            else:
                if bf==2:
                    child_bf=curr.left.left.height-curr.left.right.height
                    if child_bf>=0:
                        self.right_rotation(curr)
                        rotations+=1
                    else:
                        self.left_rotation(curr.left)
                        self.right_rotation(curr)
                        rotations+=2
                else:
                    child_bf=curr.right.left.height-curr.right.right.height
                    if child_bf<=0:
                        self.left_rotation(curr)
                        rotations+=1
                    else:
                        self.right_rotation(curr.right)
                        self.left_rotation(curr)
                        rotations+=2
                break
        return new_node, search_time,rotations,height_changes
        
            
            
        
        

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
                del node
            else: 
                parent = node.parent
                if parent.left == node: # node is left son
                    parent.left = self.virtual_node
                else:
                    parent.right = self.virtual_node
                del node

                # if tree is AVL, do rotations and height updates
                if self.is_avl:
                    self.balance_up(parent)
        
        # if node has one right son
        if node.left.key is None and node.right.key is not None:
            if node.parent is None: # if node is root
                self.root = node.right
                del node
            else:
                parent = node.parent
                if parent.left == node: # node is left son
                    parent.left = node.right
                else: # node is right son
                    parent.right = node.right
                del node

                # if tree is AVL, do rotations and height updates
                if self.is_avl:
                    self.balance_up(parent)

        # if node has one left son           
        if node.left.key is not None and node.right.key is None:
            if node.parent is None: # if node is root
                self.root = node.left
                del node
            else:
                parent = node.parent
                if parent.left == node: # node is left son
                    parent.left = node.left
                else: # node is right son
                    parent.right = node.left
                del node

                # if tree is AVL, do rotations and height updates
                if self.is_avl:
                    self.balance_up(parent) 
                    

        # if node has 2 sons
        if node.left.key is not None and node.right.key is not None:
            successor = successor = node.right
            while successor.left.key is not None:
                successor = successor.left

            node.key = successor.key
            node.value = successor.value

            successor_parent = successor.parent 
            # delete the successor node, which has one right son at most
            if successor.right.key is not None: # successor has one right son,
                                                # and successor is the left son of its parent, since it is the leftmost node in the right subtree of node
                successor.parent.left = successor.right
                del successor

            if successor.right.key is None: # successor is a leaf
                successor.parent.left = self.virtual_node
                del successor
                
            # if tree is AVL, do rotations and height updates
            if self.is_avl:    
                self.balance_up(successor_parent)



        
    def balance_up(self, A, until_root = True):
        while A != self.root:
            A_BF = A.left.height - A.right.height

            if (A_BF in [-1,0,1]) and not until_root: # A BF is ok and we don't want to continue up to root
                return
            
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
            A = A.parent

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
        result_lst=[]
        self.order_rec(self.root,result_lst)
        return result_lst
    
    def order_rec(self,node,result_list):
        if node is None or not node.is_real_node():
            return
        
        self.order_rec(node.left,result_list)
        result_list.append((node.key,node.value))
        self.order_rec(node.right,result_list)

    """returns the number of items in dictionary 
    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.size_rec(self.root)
    
    def size_rec(self,node):
        if node is None or not node.is_real_node():
            return 0
        return self.size_rec(node.left)+self.size_rec(node.right)+1

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        if self.root() is None:
            return -1
        if self.is_avl:
            return self.root().height
        return self.get_height_rec(self.root)
        

    def get_height_rec(self, node):
        if not node.is_real_node():
            return -1
        left_h= self.get_height_rec(node.left)
        right_h=self.get_height(node.right)
        return max(left_h,right_h)+1