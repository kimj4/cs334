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

    def has_space(self):
        if (self.num_keys < self.capacity):
            return True
        else:
            return False

    def insert_key(self, key):
        position_to_insert = 0
        for i in range(len(self.key_list)):
            if key_list[i] < key:
                position_to_insert = i;
        self.key_list.insert(position_to_insert, key)
        self.num_keys =+ 1

    def insert_pointer(self, pointer):
        position_to_insert = 0
        for i in range(len(self.pointer_list)):
            if pointer_list[i] < pointer:
                position_to_insert = i
        self.pointer_list.insert(position_to_insert, pointer)
        self.num_pointers =+ 1


class Bptree():
    """docstring for Bptree."""
    def __init__(self, n):
        # self.tree = {}
        self.n = n
        self.is_empty = True
        # self.root_key = "a"
        self.root = "a"

    def insert_helper(self, node, key, value):
        if (node.is_leaf):
            if node.has_space():
                node.insert_key(key)
                node.insert_pointer
                return None
            else:
                # split node
                # return pointer to the newly split node




    """Inserts a key-value pair into the tree."""
    def insert(self, key, value):
        if self.is_empty:
            print "a"
            self.root = Node(self.n)
            self.is_empty = False
        new_node = self.insert_helper(self.root, key, value)
        if new_node: # the node that was previously the root was split
            self.root = Node(self.n)




    """Returns the value associated with a particular key.
    Returns None if the key is not in the tree."""
    def getValue(self, key):
        pass

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
    b.insert(12,"hello")
    # b.insert(24,"bye")
    # print b.getValue(24)
    # b.printTree()



# {k1: ()}
