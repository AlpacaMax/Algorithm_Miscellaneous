class AVLTreeMap:
    class Item:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value


    class Node:
        def __init__(self, item=None):
            self.item = item
            self.left = None
            self.right = None
            self.parent = None
            self.height = 0
        
        def num_children(self):
            count = 0
            if (self.left is not None):
                count += 1
            if (self.right is not None):
                count += 1
            return count
        
        def disconnect(self):
            self.item = None
            self.right = None
            self.left = None
            self.parent = None
        
        def left_height(self):
            left_h = -1
            if (self.left is not None):
                left_h = self.left.height
            return left_h
        
        def right_height(self):
            right_h = -1
            if (self.right is not None):
                right_h = self.right.height
            return right_h
        
        def balance_val(self):
            return self.left_height() - self.right_height()

    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def is_empty(self):
        return len(self) == 0
    
    def __getitem__(self, key):
        node = self.find(key)
        if (node is not None):
            return node.item.value
        else:
            raise KeyError(str(key) + " not found")
    
    def find(self, key):
        curr = self.root
        while (curr is not None):
            if (curr.item.key == key):
                return curr
            elif (key < curr.item.key):
                curr = curr.left
            else:
                curr = curr.right
        return None
    
    def __setitem__(self, key, value):
        node = self.find(key)
        if (node is not None):
            node.item.value = value
        else:
            self.insert(key, value)
    
    def insert(self, key, value=None):
        new_item = AVLTreeMap.Item(key, value)
        new_node = AVLTreeMap.Node(new_item)

        if (self.is_empty() == True):
            self.root = new_node
            self.size = 1
        else:
            parent = self.root
            if (key < self.root.item.key):
                curr = self.root.left
            else:
                curr = self.root.right

            while (curr is not None):
                parent = curr
                if (key < curr.item.key):
                    curr = curr.left
                else:
                    curr = curr.right
            
            if (key < parent.item.key):
                parent.left = new_node
            else:
                parent.right = new_node

            new_node.parent = parent
            self.size += 1
        
        self.rebalance(new_node)

    def __delitem__(self, key):
        node = self.find(key)
        if (node is None):
            raise KeyError(str(key) + " is not found")
        else:
            self.delete_node(node)

    def delete_node(self, node_to_delete):
        item = node_to_delete.item
        num_children = node_to_delete.num_children()

        if (node_to_delete is self.root):
            if (num_children == 0):
                self.root = None
                node_to_delete.disconnect()
                self.size -= 1

            elif (num_children == 1):
                if (self.root.left is not None):
                    self.root = self.root.left
                else:
                    self.root = self.root.right
                self.root.parent = None
                node_to_delete.disconnect()
                self.size -= 1

            else: #num_children == 2
                max_of_left = self.subtree_max(node_to_delete.left)
                node_to_delete.item = max_of_left.item
                self.delete_node(max_of_left)

        else:
            if (num_children == 0):
                parent = node_to_delete.parent
                if (node_to_delete is parent.left):
                    parent.left = None
                else:
                    parent.right = None

                node_to_delete.disconnect()
                self.size -= 1
                self.rebalance(parent)

            elif (num_children == 1):
                parent = node_to_delete.parent
                if(node_to_delete.left is not None):
                    child = node_to_delete.left
                else:
                    child = node_to_delete.right

                if (node_to_delete is parent.left):
                    parent.left = child
                else:
                    parent.right = child
                child.parent = parent

                node_to_delete.disconnect()
                self.size -= 1
                self.rebalance(parent)

            else: #num_children == 2
                max_of_left = self.subtree_max(node_to_delete.left)
                node_to_delete.item = max_of_left.item
                self.delete_node(max_of_left)


        return item
    
    def subtree_max(self, curr_root):
        node = curr_root
        while (node.right is not None):
            node = node.right
        return node

    def rebalance(self, p):
        curr_node = p
        while (curr_node is not None):
            next_parent = curr_node.parent

            if (curr_node.balance_val() == 2):
                child = curr_node.left
                if (child.balance_val() >= 0):
                    self.right_rotate(curr_node)
                else:
                    self.left_rotate(child)
                    self.right_rotate(curr_node)
            elif (curr_node.balance_val() == -2):
                child = curr_node.right
                if (child.balance_val() <= 0):
                    self.left_rotate(curr_node)
                else:
                    self.right_rotate(child)
                    self.left_rotate(curr_node)
            
            self.recompute_height(curr_node)
            curr_node = next_parent

    def relink(self, parent, left_child, right_child):
        parent.left = left_child
        parent.right = right_child
        if (left_child is not None):
            left_child.parent = parent
        if (right_child is not None):
            right_child.parent = parent
    
    def left_rotate(self, root):
        parent = root.parent

        new_root = root.right
        new_left = root
        new_right = root.right.right
        new_left_left = root.left
        new_left_right = root.right.left

        is_left = True
        if (parent is not None and root is parent.right):
            is_left = False

        self.relink(new_left, new_left_left, new_left_right)
        self.relink(new_root, new_left, new_right)
        if (parent is None):
            self.root = new_root
            new_root.parent = None
        else:
            if (is_left):
                parent.left = new_root
                new_root.parent = parent
            else:
                parent.right = new_root
                new_root.parent = parent
        
        self.recompute_height(new_left)
        self.recompute_height(new_right)
        self.recompute_height(new_root)
    
    def right_rotate(self, root):
        parent = root.parent

        new_root = root.left
        new_left = root.left.left
        new_right = root
        new_right_left = root.right
        new_right_right = root.right.right

        is_left = True
        if (parent is not None and root is parent.right):
            is_left = False
        
        self.relink(new_right, new_right_left, new_right_right)
        self.relink(new_root, new_left, new_right)
        if (parent is None):
            self.root = new_root
            new_root.parent = None
        else:
            if (is_left):
                parent.left = new_root
                new_root.parent = parent
            else:
                parent.right = new_root
                new_root.parent = parent
        
        self.recompute_height(new_left)
        self.recompute_height(new_right)
        self.recompute_height(new_root)
        
    def recompute_height(self, node):
        node_left_h = node.left_height()
        node_right_h = node.right_height()
        
        node.height = 1 + max(node_left_h, node_right_h)
    
    def inorder(self):
        def subtree_inorder(root):
            if (root is None):
                return
            else:
                yield from subtree_inorder(root.left)
                yield root
                yield from subtree_inorder(root.right)
        yield from subtree_inorder(self.root)
    
    def preorder(self):
        def subtree_preorder(root):
            if (root is None):
                return
            else:
                yield root
                yield from subtree_preorder(root.left)
                yield from subtree_preorder(root.right)
        yield from subtree_preorder(self.root)
    
    def __iter__(self):
        for node in self.inorder():
            yield node.item.key

def main():
    avl = AVLTreeMap()
    for i in range(0, 10):
        avl[i] = i

    del avl[4]
    del avl[5]
    del avl[6]

    for node in avl.preorder():
        print(node.item.key)