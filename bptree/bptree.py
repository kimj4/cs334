# b+ tree structure brainstorm
#  dave says to use map
#   the key is the search-key value (no duplicates)
# {
#
# }
#  for n = 3
# insert 1: "a"
# {1: [1,"a"]}
# insert 2: "b"
# {1: [1, "a", 2, "b"]}
# insert 3: "c"
# {1: [1, "a, 2, "b", 3, "c"]} full node, need to split
# {2: [{1: "a"}, 2, {2: "b", 3: "c"}]}
# insert 4: "d"
# {2: [{1: "a"}, 2, {2: "b", 3: "c", 4: "d"}]} full node, need to split
# {2: [{1: "a"}, 2, {2: "b"}, 3, {3: "c", 4: "d"} ]}
# insert 5: "e"
# {2: [{1: "a"}, 2, {2: "b"}, 3, {3: "c", 4: "d", 5: "e"}]} split
# {2: [{1: "a"}, 2, {2: "b"}, 3, {3: "c"}, 4, {4: "d", 5: "e"}]} root full split
# {3: {}}

{
2: (1, 5)
}



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
        if (self.is_leaf):
            if (self.num_pointers == self.capacity):
                return True
            else:
                return False
        else:
            if (self.num_pointers == self.capacity + 1):
                return True
            else: 
                return False


    def insert_key(self, key):
        position_to_insert = 0
        for i in range(len(self.key_list)):
            if self.key_list[i] < key:
                position_to_insert = i;
        self.key_list.insert(position_to_insert, key)
        self.num_keys = self.num_keys +  1

    def insert_pointer(self, pointer):
        position_to_insert = 0
        for i in range(len(self.pointer_list)):
            if self.pointer_list[i] < pointer:
                position_to_insert = i
        self.pointer_list.insert(position_to_insert, pointer)
        self.num_pointers = self.num_keys + 1

    # def is_full(self):
    #     if (self.)


class Bptree():
    """docstring for Bptree."""
    def __init__(self, n):
        # self.tree = {}
        self.n = n
        self.is_empty = True
        # self.root_key = "a"
        self.root = "a"

    def insert_helper(self, node, key, value):
        # node is leaf
        if (node.is_leaf):
            # if node, insert key and value no matter what
            #  check for split case afterwards 
            node.insert_key(key)
            node.insert_pointer(value)
            print node.capacity
            print "number of pointers: %s" % node.num_pointers
            print "number of keys: %s" % node.num_keys
            if node.is_full():
                print("insert_helper: node is full")
                if node.is_root:
                    leftNode = Node(self.n)
                    leftNode.key_list = node.key_list[0: self.n // 2]
                    print node.pointer_list
                    print self.n // 2
                    print leftNode.key_list
                    leftNode.pointer_list = node.pointer_list[0: self.n // 2]
                    rightNode = Node(self.n)
                    rightNode.key_list = node.key_list[self.n // 2: -1]

                    rightNode.pointer_list = node.pointer_list[self.n // 2: -1]
                    newRoot = Node(self.n)
                    newRoot.key_list[0] = rightNode.key_list[0]
                    newRoot.pointer_list[0] = leftNode
                    newRoot.pointer_list[1] = rightNode
                    # special case split
                    pass
                else:
                    # typcial case split
                    pass
            else:
                # all work is done
                return None
        
        # node is internal
        else:
            # determine which subtree to look into 
            traversal_idx = 0
            for i in range(len(node.key_list)):
                if key < node.key_list[i]:
                    traversal_idx = i 
            newEntry = insert_helper(node.pointer_list[traversal_idx], key, value)



            
            if newEntry == None:
                # child not split, nothing to do
                return None
            elif not node.is_full:
                # add new entry in appropriate slot
                node.insert_key(key)
                node.insert_pointer(newEntry)
                return None
            else:
                # do an internal split
                pass






    """Inserts a key-value pair into the tree."""
    def insert(self, key, value):
        if self.is_empty:
            self.root = Node(self.n)
            self.is_empty = False
        self.insert_helper(self.root, key, value)


    def getValueHelper(self, node, key):
        if (node.is_leaf):
            if key not in node.key_list:
                return None
            else:
                pointer_idx = node.key_list.index(key)
                return node.pointer_list[pointer_idx]
        else:
            # pointer_idx = 0;
            i = 0
            while (key < node.key_list[i]):
                i += 1
            return self.getValueHelper(node.pointer_list[i], key)

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
        pass

if __name__ == "__main__":
    # b = bptree.Bptree(4)  # Each node contains 4 keys, which means 5 pointers
    b = Bptree(4)
    b.insert(0, "a")
    # print "after inserting a:"
    # print b.key_list  
    b.insert(1, "b")
    b.insert(2, "c")
    b.insert(3, "d")
    b.insert(4, "e")
    b.insert(5, "f")
    b.insert(6, "g")
    print b.getValue(0)
    print b.getValue(1)
    print b.getValue(2)
    print b.getValue(3)
    print b.getValue(4)
    print b.getValue(5)
    print b.getValue(6)
    print b.root.pointer_list   
    # b.printTree()



# {k1: ()}
