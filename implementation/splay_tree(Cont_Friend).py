# Contengency freindly Splay tree implementation in Python
# Group:Cameron White, *enter names here*


#Import Semaphore for critical section handling
import threading

# data structure that represents a node in the tree
class Node:
    
    def  __init__(self,key,data):
        #data: the data that is stored
        #key: how the data will be referneced in the tree
        # left : left child
        # right: right child
        # lock: used to keep contengency, locks threads fcritical sections of code
        # remove: denotes if node was physically removed
        # dele:deonotes if node was removed lazily, used in lazy splaying
        #zig: marked if node was removed by zigRight rotation
        #Cnt: total number of operations  that had been performed on the node
        #leftCnt: left subtree count
        #rightCnt: right subtreee count
        #parent pointer
        self.data = data
        self.key = key
        self.left = None
        self.right = None
        self.lock = threading.Lock()
        self.remove = False
        self.dele = False
        self.zig = False
        self.Cnt = 0
        self.leftCnt = 0
        self.rightCnt = 0
        self.parent = None
        
class SplayTree_ContFriendly:
    #Note* tree does not allow duplicates
    def __init__(self):
        #root: the root node of BST   
        self.root = None
        result = False
        
    #######Basic Abstract Operations(Contention friendly)#############
    #returns true if inserted into tree
    def insert(self,key,value):
        result = False
        #if no nodes create root
        if self.root is None:
            self.root = Node(key,value)
            result = True
            return result
        cur = self.root
        #while the next node is not null, find next valid node
        while(True):
            nxt = self.getNext(cur,key)
            if(nxt is None):
                self._lock(cur)
        #######critical section##################
                if(self.isValid(cur,key)):
                    break
        ########critical section exit 1##########
                self._unlock(cur)
            else:
                cur = nxt
        #if key already exist, but is lazily deleted, make it reinstate its license(lol)
        if cur.key == key:
            if(cur.dele):
                cur.parent 
                cur.dele = False
                cur.Cnt += 1
                result = True
        #otherwise, create new leaf based on if the key is greater or less than the current node
        else:
            if cur.key > key:
                cur.left = Node(key,value)
                cur.left.parent = cur
            else:
                cur.right = Node(key,value)
                cur.right.parent = cur
            #set result to true
            result = True
        ########critical section exit 2##########
            
        self._unlock(cur)
        return result
    #returns true if deleted into tree
    def delete(self,key):
        cur = self.root
        result = False
        #while nxt is not none, find valid node to be deleted
        while True:
            nxt = self.getNext(cur,key)
            if nxt is None:
                self._lock(cur)
                if self.isValid(cur,key):
                    break
                self.unlock(cur)
            else:          
                cur = nxt
        #if the current node is the node to be deleted, lazily delete it
        if (cur.key == key):
            if not(cur.dele):
                cur.dele = True
                result = True
        self._unlock(cur)
        return result
              
    def find(self,key): 
        cur = self.root
        result = False
        while(self.getnext(cur,key) is not None):
            nxt = self.getnext(cur,key)
            cur = nxt
        if cur.key == key and not (cur.dele):
            result = True
            self._splayNose(cur,cur.left,cur.right)
            cur.Cnt += 1
            
        return result

    def getNext(self, node, key):
        rem = node.remove
        isZig = node.zig
        if(rem and isZig):
            nxt = node.right
        elif(rem):
            nxt = node.left
        elif(node.key == key):
            nxt = None
        elif(node.key > key):
            nxt = node.left
        else:
            nxt = node.right
        return nxt

    def isValid(self, node, key):
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
    #######Contention friendly Operations#########       
    def _removeNode(self, parent, x):
        removed = False
        if(parent.remove):
            return removed
        self._lock(parent)
        self._lock(x)
        if not x.dele:
            self._unlock(parent)
            self._unlock(child)
            return removed
        if (x.left and x.right is not None):
            self._unlock(parent)
            self._unlock(x)
            return removed
        elif(x.left is not None):
            child = x.left
        else:
            child =x.right
            x.left = parent
            x.right = parent
        x.remove = True
        removed = True
        self._unlock(parent)
        self._unlock(child)
        return removed
        
            
########Rotates#############################################
    def _ZigRotate(self, parent, x, l):
        ret = False
        if parent.remove:
            return ret
        if x is None:
            return ret
        if l is None:
            return ret
        self._lock(parent)
        self._lock(x)
        self._lock(l)
        lRight = l.right
        xRight = x.right

        p = Node(x.key,x.value)
        p.left = lRight
        p.right = xRight
        l.right = temp
        if x == parent.left:
            parent.left = l
        else:
            parent.right = l
        x.remove = True
        x.zig = True

        l.parent = parent
        x.parent = l
        
        self.unlock(l)
        self.unlock(x)
        self.unlock(parent)
        ret = True
        return ret
    
    def _ZigZagRotate(self, grand, parent, x, r):
        ret = False
        if grand.remove:
            return ret
        if parent is None:
            return ret
        if x is None:
                return ret
        if r is None:
                return ret
        self.lock(grand)
        self.lock(parent)
        self.lock(x)
        self.lock(r)
            
        xLeft = x.left
        rLeft = r.left
        rRight = r.right
        pRight = parent.right

        temp = Node(x.key,x.value)
        temp.left = xLeft
        temp.right = rLeft
        r.left = temp

        ptemp = Node(parent.key,parent.value)
        ptemp.left = rRight
        ptemp.right = parent.Right
            
        r.right = ptemp
            
        if parent == grand.left:
            grand.left = r
        else:
            grand.right = r
                
        x.remove = True
        parent.remove = True
        ret = True
        self.unlock(r)
        self.unlock(x)
        self.unlock(parent)
        self.unlock(grand)
        return ret


###################Background Operations###################
    def _longSplayDFS(self, x):
        if x is None:
            return
        self._longSplayDFS(x.left)
        self._longSplayDFS(x.right)
        if x.left is not None and x.left.dele:
            self._removeNode(x,x.left)
            
        if x.right is not None and x.right.dele:
            self._removeNode(x,x.right)
            
        self._propagateCounter(x)
        if x.left is None or x.right is None:
            self._splayNode(parent,x,x.left,x.right)
            '''Note* create find_parent alg'''
        else:
            return

    def _propogateCounter(self,x):
        if x.left is None:
            x.leftCnt = x.left.leftCnt + x.left.rightCnt  + x.left.Cnt
        else:
            x.leftCnt = 0

    def _backGroundLongSplay(self):
        while True:
            self._longSplayDFS(self.root)
    
    #called by find and insert(not currently implemented)
    def _splayNode(parent, l, n, r):
        nPlusLeftCnt = l.Cnt + l.leftCnt
        pPlusRightCnt = parent.Cnt + parent.rightCnt
        nRightCnt = l.rightCnt
        if nPlusRightCnt >= pPlusRightCount:
            grand = parent.parent
            self._ZigZagRotate(grand, parent, l)
            parent.leftCnt = l.right.rightCnt
            l.rightCnt = l.right.leftCnt
            l.right.rightCnt = l.right.rightCnt + pPlusRightCnt
            l.rightCnt = l.rightCnt + nRightCnt
        elif(nPlusLeftCnt > pPlusRightCnt):
            grand = parent.parent
            self.zigRotate(grand,parent,l)
            parent.leftCnt = l.rightCnt
            l.rightCnt = l.rightCnt + pPlusRightCnt

################critical section handling###################
    def _lock(self,n):
        n.lock.acquire()
    def _unlock(self,n):
        n.lock.release()     
############################################################
        ''' hell nawl I aint made for this G
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
'''
################Test Main########################
x = SplayTree_ContFriendly()
print(x.insert(3,'w'))
print(x.insert(4,'q'))
print(x.insert(5,'y'))
print(x.delete(5))
print(x.delete(5))
print(x.delete(4))
print(x.insert(4,'q'))
