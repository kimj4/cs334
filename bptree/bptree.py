# incomplete version
# could not finish due to time constraints and conflicting due dates
# across different classes
# insert_helper and insertHelper are two different prototypes where
# insertHelper more closely follows the pseudocode outline



class Node():
    def __init__(self, n):
        self.is_root = True
        self.is_leaf = True
        self.capacity = n
        self.num_keys = 0
        self.num_pointers = 0
        self.key_list = []
        # pointer_list stores either nodes or python values
        self.pointer_list = []

    def is_full(self):
        # if (self.num_keys == self.capacity ):
        #     return True
        # else:
        #     return False
        if (self.is_leaf):
            if (self.num_keys == self.capacity):
                return True
            else:
                return False
        else:
            if (self.num_keys == self.capacity - 1):
                return True
            else:
                return False


    def insert_key(self, key):
        position_to_insert = 0
        for i in range(len(self.key_list)):
            if (self.key_list[i] < key):
                position_to_insert = i + 1;
        self.key_list.insert(position_to_insert, key)
        self.num_keys = self.num_keys + 1
        return position_to_insert

    def insert_pointer(self, position, pointer):
        self.pointer_list.insert(position, pointer)
        # position_to_insert = 0
        # for i in range(len(self.pointer_list)):
        #     if self.pointer_list[i] < pointer:
        #         position_to_insert = i
        # self.pointer_list.insert(position_to_insert, pointer)
        # self.num_pointers = self.num_keys + 1
        # print "num pointers: %s" % self.num_pointers

    # def is_full(self):
    #     if (self.)


class Bptree():
    """docstring for Bptree."""
    def __init__(self, n):
        self.n = n
        self.is_empty = True
        self.root = None


    def insertHelper(self, N, K, P):
        if N.is_leaf:
            ki = N.insert_key(K)
            N.insert_pointer(ki,P)
            if not N.is_full():
                return None
            else:
                N2 = Node(self.n)
                N2.is_leaf = True
                N2.is_root = False
                N2.key_list = N.key_list[self.n // 2:]
                N2.num_keys = len(N2.key_list)
                N2.pointer_list = N.pointer_list[self.n // 2:]
                N2.num_pointers = len(N2.pointer_list)

                N.key_list = N.key_list[:self.n // 2]
                N.num_keys = len(N.key_list)
                N.pointer_list = N.pointer_list[:self.n // 2]
                N.num_pointers = len(N.pointer_list)

                newNode = Node(self.n)
                newNode.is_leaf = False
                newNode.insert_key(N2.key_list[0])
                newNode.insert_pointer(0, N)
                newNode.insert_pointer(1, N2)
                if N.is_root:
                    N.is_root = False
                    newNode.is_root = True
                    self.root = newNode
                    return None
                else:
                    newNode.is_root = False
                    return (newNode.key_list[0], newNode);
        else:
            newNodeIdx = -1
            for i in range(len(N.key_list)):
                if K < N.key_list[i]:
                    newNodeIdx = i
            if newNodeIdx == -1:
                newNodeIdx = len(N.key_list) - 1;
            newEntry = self.insertHelper(N.pointer_list[newNodeIdx], K, P)

            if newEntry == None:
                return None
            elif len(N.key_list) + 1 < self.n:
                ki = N.insert_key(newEntry[0])
                N.insert_pointer(ki, newEntry[1])
                return None
            else:
                ki = N.insert_key(newEntry[0])
                N.insert_pointer(ki, newEntry[1])

                N2 = Node(self.n)
                N2.is_leaf = False
                N2.is_root = False
                N2.key_list = N.key_list[(self.n // 2) + 1:]
                N2.num_keys = len(N2.key_list)
                N2.pointer_list = N.pointer_list[self.n // 2:]
                N2.num_pointers = len(N2.pointer_list)

                Kp = N.key_list[(self.n // 2) + 1]

                N.key_list = N.key_list[:self.n // 2]
                N.num_keys = len(N.key_list)
                N.pointer_list = N.pointer_list[:self.n // 2]
                N.num_pointers = len(N.pointer_list)

                newEntry = (Kp, N2)
                if N.is_root:
                    newNode = Node(self.n)
                    newNode.is_leaf = False
                    newNode.insert_key(N2.key_list[0])
                    newNode.insert_pointer(0, N)
                    newNode.insert_pointer(1, N2)
                    self.root =  newNode
                return newEntry


    def insert_helper(self, node, key, value):
        # node is leaf
        if (node.is_leaf):

            # if node, insert key and value no matter what
            #  check for split case afterwards
            keyPosition = node.insert_key(key)
            node.insert_pointer(keyPosition + 1, value)
            if node.is_full():
                print("insert_helper: node is full")
                if node.is_root:
                    print "\ninsert_helper: root case leaf split"

                    leftNode = Node(self.n)
                    leftNode.is_root = False
                    leftNode.is_leaf = True
                    leftNode.key_list = node.key_list[: self.n // 2]
                    leftNode.num_keys = len(leftNode.key_list)
                    leftNode.pointer_list = node.pointer_list[  : self.n // 2]
                    leftNode.num_pointers = len(leftNode.pointer_list)

                    print "rightNode: %s" % leftNode.key_list
                    print "leftNode.key_list length: %s" % len(leftNode.key_list)

                    rightNode = Node(self.n)
                    rightNode.is_root = False
                    rightNode.is_leaf = True
                    rightNode.key_list = node.key_list[self.n // 2: ]
                    rightNode.num_keys = len(rightNode.key_list)
                    rightNode.pointer_list = node.pointer_list[self.n // 2:]
                    rightNode.num_pointers = len(rightNode.pointer_list)

                    print "rightNode: %s" % rightNode.key_list
                    print "rightNode.key_list length: %s" % len(rightNode.key_list)

                    newRoot = Node(self.n)
                    newRoot.is_leaf = False
                    newRoot.key_list.append(rightNode.key_list[0])
                    newRoot.num_keys = len(newRoot.key_list)
                    newRoot.pointer_list.append(leftNode)
                    newRoot.pointer_list.append(rightNode)
                    newRoot.num_pointers = len(newRoot.pointer_list)

                    print "newRoot.key_list: %s" % newRoot.key_list;
                    self.root = newRoot
                    return None
                else:
                    # typcial case split
                    print "\ninsert_helper: typical case leaf split "
                    # the current node is kept, but halved
                    newRight = Node(self.n)
                    newRight.is_root = False
                    newRight.is_leaf = True
                    newRight.key_list = node.key_list[self.n // 2 :]
                    newRight.num_keys = len(newRight.key_list)




                    node.key_list = node.key_list[: self.n // 2]
                    node.num_keys = len(node.key_list)

                    newRight.pointer_list = node.pointer_list[self.n // 2 :]
                    newRight.num_pointers = len(newRight.pointer_list)

                    node.pointer_list = node.pointer_list[: self.n // 2]
                    node.num_pointers = len(node.pointer_list)


                    newEntry = Node(self.n)
                    newEntry.is_root = False
                    newEntry.is_leaf = False
                    newEntry.insert_key(newRight.key_list[0])
                    newEntry.insert_pointer(0, newRight)
                    # newEntry.key_list = node.key_list[self.n // 2 :]
                    # newEntry.num_keys = len(newEntry.key_list)


                    # newEntry.pointer_list = node.pointer_list[self.n // 2 :]
                    # newEntry.num_pointers = len(newEntry.pointer_list)

                    print "newEntry.key_list: %s" % newEntry.key_list
                    print "node.key_list: %s" % node.key_list
                    return newEntry
            else:
                # all work is done
                return None

        # node is internal
        else:
            print "\ninsert_helper: looking at an internal node ..."
            # determine which subtree to look into
            print "key to be inserted: %s" % key
            print "node.key_list: %s" % node.key_list
            newNodeIdx = -1
            for i in range(len(node.key_list)):
                if key < node.key_list[i]:
                    newNodeIdx = i
            if newNodeIdx == -1:
                newNodeIdx = len(node.key_list) - 1;
            newEntry = self.insert_helper(node.pointer_list[newNodeIdx], key, value)


            # print "node num keys: %s" % node.num_keys
            # print "newEntry.key_list: %s" % newEntry.key_list
            if newEntry == None:
                print "\nnewEntry == None\n"
                # child not split, nothing to do
                return None
            elif not node.is_full():
                print "\ncurrent node has space\n"
                print "node.key_list: %s" % node.key_list
                print "node.num_keys: %s" % node.num_keys
                # add new entry in appropriate slot
                keyPosition = node.insert_key(newEntry.key_list[0])
                node.insert_pointer(keyPosition + 1, newEntry)
                return None
            else:
                print "internal node split"
                npp = node.insert_key(key)
                node.insert_pointer(npp, value)
                newEntry = Node(self.n)
                newEntry.is_root = False
                newEntry.is_leaf = False
                keyPosition = newEntry.insert_key(node.key_list[self.n // 2])
                print "newEntry.key_list: %s" % newEntry.key_list


                newRight = Node(self.n)
                newRight.is_root = False
                newEntry.is_leaf = False
                newRight.key_list = node.key_list[(self.n // 2) + 1 :]
                newRight.num_keys = len(newRight.key_list)
                newRight.pointer_list = node.pointer_list[(self.n // 2) :]
                newRight.num_pointers = len(newRight.pointer_list)

                node.key_list = node.key_list[: (self.n // 2)]
                node.num_keys = len(node.key_list)
                node.pointer_list = node.pointer_list[:(self.n // 2)]
                node.num_pointers = len(node.pointer_list)

                if node.is_root:
                    node.is_root = False
                    newEntry.is_root = True
                    newEntry.insert_pointer(0, node)
                    newEntry.insert_pointer(1, newRight)
                    print "newEntry.pointer_list[0].key_list: %s" % newEntry.pointer_list[0].key_list
                    print "newEntry.pointer_list[1].key_list: %s" % newEntry.pointer_list[1].key_list
                    print "newEntry.pointer_list[0].pointer_list: %s" % newEntry.pointer_list[0].pointer_list
                    print "newEntry.pointer_list[1].pointer_list: %s" % newEntry.pointer_list[1].pointer_list
                    self.root = newEntry
                    return None
                else:
                    newEntry.insert_pointer(0,newRight)
                    return newEntry

                # newEntry.key_list = node.key_list[self.n // 2 :]
                # newEntry.num_keys = len(newEntry.key_list)
                # node.key_list = node.key_list[: self.n // 2]
                # node.num_keys = len(node.key_list)
                # newEntry.pointer_list = node.pointer_list[self.n // 2 :]
                # newEntry.num_pointers = len(newEntry.pointer_list)
                # node.pointer_list = node.pointer_list[: self.n // 2]
                # node.num_pointers = len(node.pointer_list)
                # print "newEntry.key_list: %s" % newEntry.key_list
                # print "node.key_list: %s" % node.key_list
                # return newEntry
                # do an internal split
                # pass

    """Inserts a key-value pair into the tree."""
    def insert(self, key, value):
        if self.is_empty:
            self.root = Node(self.n)
            self.root.is_root = True
            self.root.is_leaf = True
            self.is_empty = False
        # new = self.insert_helper(self.root, key, value)
        # if new:
        #     print "ERROR: return value from insert_helper is not None"
        self.insertHelper(self.root, key, value)


    def getValueHelper(self, node, key):
        if (node.is_leaf):
            if key not in node.key_list:
                return None
            else:
                pointer_idx = node.key_list.index(key)
                return node.pointer_list[pointer_idx]
        else:
            # pointer_idx = 0;
            idx = 0
            for i in range(len(node.key_list)):
                if key < node.key_list[i]:
                    idx = i
            return self.getValueHelper(node.pointer_list[idx], key)
            # i = 0
            # while (key < node.key_list[i]):
            #     i += 1
            # return self.getValueHelper(node.pointer_list[i], key)

    """Returns the value associated with a particular key.
    Returns None if the key is not in the tree."""
    def getValue(self, key):
        return self.getValueHelper(self.root, key)




    """Prints out a text version of the tree to the screen.
    The easiest way I found to do this was to rotate the tree vertically,
    showing the root on the left hand side of the terminal window,
    expanding to the right, and indenting further for deeper levels.
    Doing a recursive depth-first traversal of the tree made this pretty easy."""
    def printTree(self):
        print self.printTreeHelper(self.root)

    def printTreeHelper(self, node):
        if node.is_leaf:
            # return "(%s)" % node.key_list;
            return "|(%s) (%s)|" % (node.key_list, node.pointer_list)
        else:
            build = ""
            build = build + str(node.key_list)
            for item in node.pointer_list:
                build = build + "\n" + self.printTreeHelper(item)
            return build

if __name__ == "__main__":
    b = Bptree(3)

    b.insert(0, "a")
    print "==================="
    b.printTree()
    print "==================="

    b.insert(1, "b")
    print "==================="
    b.printTree()
    print "==================="

    b.insert(2, "c")
    print "==================="
    b.printTree()
    print "==================="

    b.insert(3, "d")
    print "==================="
    b.printTree()
    print "==================="

    b.insert(4, "e")
    b.insert(5, "f")
    b.insert(6, "g")
    print "==================="
    b.printTree()
    print "==================="
