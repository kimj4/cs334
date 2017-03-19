# nonleaf key_list and pointer_list
# n = 3
# key_list: [0, 1]
# pointer_list [<node1> <node2> <node3>]
# if key < key_list[0]:
#   node1
# if key < key_list[1]:
#   node2
# else:
#   node3




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
            if (self.num_pointers == self.capacity + 1):
                print self.capacity
                print "is_full evaluates true"
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
            if (self.key_list[i] < key):
                position_to_insert = i + 1;
        self.key_list.insert(position_to_insert, key)
        print "position to insert: %s" % position_to_insert
        self.num_keys = self.num_keys + 1  
        print "numkeys: %s" % self.num_keys

    def insert_pointer(self, pointer):
        position_to_insert = 0
        for i in range(len(self.pointer_list)):
            if self.pointer_list[i] < pointer:
                position_to_insert = i
        self.pointer_list.insert(position_to_insert, pointer)
        self.num_pointers = self.num_keys + 1
        print "num pointers: %s" % self.num_pointers

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
            print node.key_list
            node.insert_pointer(value)
            # print "before checking if full: %s" % node.key_list
            if node.is_full():
                print("insert_helper: node is full")
                if node.is_root:
                    print node.key_list
                    print node.pointer_list
                    leftNode = Node(self.n)
                    leftNode.is_root = False
                    leftNode.key_list = node.key_list[: self.n // 2]
                    # print "length of leftNode key_list: %s" % len(leftNode.key_list)
                    print leftNode.key_list


                    leftNode.pointer_list = node.pointer_list[  : self.n // 2]
                    rightNode = Node(self.n)
                    rightNode.is_root = False
                    rightNode.key_list = node.key_list[self.n // 2: ]
                    # print "length of rightNode key_list: %s" % len(rightNode.key_list)
                    print rightNode.key_list

                    rightNode.pointer_list = node.pointer_list[self.n // 2:]
                    newRoot = Node(self.n)
                    newRoot.is_leaf = False
                    newRoot.key_list.append(rightNode.key_list[0])
                    newRoot.pointer_list.append(leftNode)
                    newRoot.pointer_list.append(rightNode)
                    # special case split
                    return newRoot
                else:
                    # typcial case split
                    print "asdfasdfasdf "
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
            newEntry = self.insert_helper(node.pointer_list[traversal_idx], key, value)



            
            if newEntry == None:
                # child not split, nothing to do
                return None
            elif not node.is_full:
                # add new entry in appropriate slot
                node.insert_key(key)
<<<<<<< HEAD
                node.insert_pointer
                return None
            else:
                # split node
                # return pointer to the newly split node
=======
                node.insert_pointer(newEntry)
                return None
            else:
                # do an internal split
                pass


>>>>>>> 49cbb535fdeabc62a73088f20dff0653cbd24ca1




    """Inserts a key-value pair into the tree."""
    def insert(self, key, value):
        if self.is_empty:
            self.root = Node(self.n)
            self.is_empty = False
<<<<<<< HEAD
        new_node = self.insert_helper(self.root, key, value)
        if new_node: # the node that was previously the root was split
            self.root = Node(self.n)

=======
        new = self.insert_helper(self.root, key, value)
        if new:
            self.root = new
>>>>>>> 49cbb535fdeabc62a73088f20dff0653cbd24ca1


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
            return "(%s)" % node.key_list;
        else:
            build = ""
            build = build + str(node.key_list)
            for item in node.pointer_list:
                build = build + self.printTreeHelper(item)
            return build

if __name__ == "__main__":
    # b = bptree.Bptree(4)  # Each node contains 4 keys, which means 5 pointers
    b = Bptree(3)
    b.insert(0, "a")
    # print "after inserting a:"
    # print b.key_list  
    b.insert(1, "b")
    b.insert(2, "c")
    # print b.root.key_list
    # print b.root.pointer_list
    # print "left:"
    # print b.root.pointer_list[0].key_list
    # print "right"
    # print b.root.pointer_list[1].key_list
    b.insert(3, "d")

    # b.insert(4, "e")
    # b.insert(5, "f")
    # b.insert(6, "g")
    # print b.getValue(0)
    # print b.getValue(1)
    # print b.getValue(2)
    # print b.getValue(3)
    # print b.getValue(4)
    # print b.getValue(5)
    # print b.getValue(6)
    # print b.root.pointer_list   
    # b.printTree()
    b.printTree()



# {k1: ()}
