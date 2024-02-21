# Contengency freindly Splay tree implementation in Python
# Group:Cameron White, *enter names here*

# data structure that represents a node in the tree
class Node:
    
    def  __init__(self,key,data):
        #data: the data that is stored
        #key: how the data will be referneced in the tree
        # left : left child
        # right: right child
        # lock: used to keep contengency
        # remove: denotes if node was physically removed
        # dele:deonotes if node was removed lazily, used in lazy splaying
        #zig: marked if node was removed by zigRight rotation
        #Cnt: total number of operations  that had been performed on the node
        #leftCnt: left subtree count
        #rightCnt: right subtreee count
        self.data = data
        self.key = key
        self.left = None
        self.right = None
        self.lock = False
        self.remove = False
        self.dele = False
        self.zig = False
        self.Cnt = 0
        self.leftCnt = 0
        self.rightCnt = 0
        
class SplayTree_ContFriendly:

    def __init__(self):
        #root: the root node of BST   
        self.root = None
        result = False
        
    #######Contention friendly Operations#############
    
    def _insert(self,key,value):
        if self.root is None:
            self.root = Node(key,value)
        cur = self.root
        while(True):
            nxt = self._getNext(cur,key)
            if(nxt is None):
                self.lock(cur)
                if(self.isValid(cur,key)):
                    self.unlock(cur)
                    break
            else:
                cur = nxt
        if cur.key == key:
            if(cur.dele):
                cur.dele = False
                result = True
        else:
            if cur.key > key:
                cur.left = Node(key,value)
            else:
                cur.right = Node(key,value)
            result = True
        self.unlock(cur)
        return result
    
    def _delete(self,key ):
        cur = self.root
        result = False
        while(cur is not None):
            nxt = self._getnext(cur,key)
            if nxt is None:
                lock(cur)
                if (isValid(cur,key)):
                    break
                unlock(cur)
            else:
                cur = nxt
        if (cur.key == key):
            if not (cur.dele):
                cur.dele = True
                result = True
            unlock(cur)
        return result
              
    def _find(self,key): 
        cur = self.root
        result = False
        while(nxt == self._getnext(cur,key) is not None):
            cur = nxt
        if cur.key == key and not (cur.dele):
            result = True
            Splay(cur,cur.left,cur.right)
            cur.selfCnt += 1
            
        return result
    
    #######Basic Abstract Operations######   
    def _getNext(self, node, key):
        rem = node.remove
        isZig = node.zig
        if(rem and isZig):
            nxt = node.right
        elif(rem):
            nxt = node.left
        elif(node.key == key):
            nxt = None
        elif(node.key > key):
            nxt = node.right
        else:
            nxt = node.left
        return nxt

    def _isValid(self, node, key):
        if(node.remove):
            return False
        elif(node.key == key):
            return True
        elif(node.key > key):
            nxt = node.right
        else:
            nxt = node.left
        if(nxt is None):
            return True
        return False
            
    # rotate left at node x
    def __left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def __right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x
        
        y.parent = x.parent;
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        y.right = x
        x.parent = y

    # Splaying operation. It moves x to the root of the tree
    def __splay(self, x):
        while x.parent != None:
            if x.parent.parent == None:
                if x == x.parent.left:
                    # zig rotation
                    self.__right_rotate(x.parent)
                else:
                    # zag rotation
                    self.__left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # zig-zig rotation
                self.__right_rotate(x.parent.parent)
                self.__right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # zag-zag rotation
                self.__left_rotate(x.parent.parent)
                self.__left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # zig-zag rotation
                self.__left_rotate(x.parent)
                self.__right_rotate(x.parent)
            else:
                # zag-zig rotation
                self.__right_rotate(x.parent)
                self.__left_rotate(x.parent)

    def __pre_order_helper(self, node):
        if node != None:
            sys.stdout.write(node.data + " ")
            self.__pre_order_helper(node.left)
            self.__pre_order_helper(node.right)

    def __in_order_helper(self, node):
        if node != None:
            self.__in_order_helper(node.left)
            sys.stdout.write(node.data + " ")
            self.__in_order_helper(node.right)

    def __post_order_helper(self, node):
        if node != None:
            self.__post_order_helper(node.left)
            self.__post_order_helper(node.right)
            print(node.data + " ", end="")

    # Pre-Order traversal
    # Node->Left Subtree->Right Subtree
    def preorder(self):
        self.__pre_order_helper(self.root)

    # In-Order traversal
    # Left Subtree -> Node -> Right Subtree
    def inorder(self):
        self.__in_order_helper(self.root)

    # Post-Order traversal
    # Left Subtree -> Right Subtree -> Node
    def postorder(self):
        self.__post_order_helper(self.root)

    # search the tree for the key k
    # and return the corresponding node
    def search_tree(self, k):
        x = self.__search_tree_helper(self.root, k)
        if x != None:
            self.__splay(x)

    # find the node with the minimum key
    def minimum(self, node):
        while node.left != None:
            node = node.left
        return node

    # find the node with the maximum key
    def maximum(self, node):
        while node.right != None:
            node = node.right
        return node

    # find the successor of a given node
    def successor(self, x):
        # if the right subtree is not null,
        # the successor is the leftmost node in the
        # right subtree
        if x.right != None:
            return self.minimum(x.right)

        # else it is the lowest ancestor of x whose
        # left child is also an ancestor of x.
        y = x.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y

    # find the predecessor of a given node
    def predecessor(self, x):
        # if the left subtree is not null,
        # the predecessor is the rightmost node in the 
        # left subtree
        if x.left != None:
            return self.maximum(x.left)

        y = x.parent
        while y != None and x == y.left:
            x = y
            y = y.parent
        return y


