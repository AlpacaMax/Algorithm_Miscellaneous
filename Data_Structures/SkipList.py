import random

class SkipList:
    class Item:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value
        
        def __repr__(self):
            return "({}, {})".format(self.key, self.value)

    class Node:
        def __init__(self, item=None, prev=None, next=None, above=None, below=None):
            self.item = item
            self.next = next
            self.prev = prev
            self.above = above
            self.below = below
        
        def disconnect(self):
            self.__init__(self)
    
    def __init__(self):
        self.header = SkipList.Node()
        self.trailer = SkipList.Node()
        self.header.next = self.trailer
        self.trailer.prev = self.header

        self.g_header = SkipList.Node()
        self.g_trailer = SkipList.Node()
        self.g_header.next = self.g_trailer
        self.g_trailer.prev = self.g_header
        self.header.below = self.g_header
        self.g_header.above = self.header
        self.trailer.below = self.g_trailer
        self.g_trailer.above = self.trailer

        self.size = 0
        self.height = 1

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def find(self, key):
        cursor = self.header
        while (cursor.below is not None):
            cursor = cursor.below
            while (cursor.next.item is not None and key >= cursor.next.item.key):
                cursor = cursor.next

        return cursor
    
    def insert(self, key, value=None):
        node = self.find(key)
        if (node.item is not None and node.item.key == key):
            node.item.value = value
        else:
            cursor = self.add_after(node, key, value)
            self.size += 1
            index = 1
            while (self.flip()):
                index += 1
                if (index > self.height):
                    self.add_level_below(self.header, self.trailer)
                
                cursor = self.add_above(cursor, key)
    
    def add_level_below(self, header, trailer):
        above_header = header
        above_trailer = trailer
        below_header = header.below
        below_trailer = trailer.below

        new_header = SkipList.Node(above=above_header, below=below_header)
        new_trailer = SkipList.Node(above=above_trailer, below=below_trailer)
        new_header.next = new_trailer
        new_trailer.prev = new_header

        above_header.below = new_header
        below_header.above = new_header
        above_trailer.below = new_trailer
        below_trailer.above = new_trailer

        self.height += 1

    def __getitem__(self, key):
        node = self.find(key)
        if (node.item is None or node.item.key != key):
            raise KeyError(str(key) + " does not exist!")

        return node.item.value

    def __setitem__(self, key, value):
        node = self.find(key)
        if (node.item is not None and node.item.key == key):
            node.item.value = value
        else:
            self.insert(key, value)

    def __delitem__(self, key):
        node = self.find(key)
        if (node.item is None or node.item.key != key):
            raise KeyError(str(key) + " does not exist!")
        
        cursor = node
        while (cursor is not None):
            node_to_delete = cursor
            cursor = cursor.above
            self.delete_node(node_to_delete)

        self.size -= 1

    def __iter__(self):
        cursor = self.g_header.next
        while (cursor is not self.g_trailer):
            yield cursor.item.key
            cursor = cursor.next

    def add_after(self, node, key, value=None):
        prev_node = node
        next_node = node.next
        new_item = SkipList.Item(key, value)
        new_node = SkipList.Node(item=new_item, next=next_node, prev=prev_node)
        prev_node.next = new_node
        next_node.prev = new_node
        return new_node
    
    def add_above(self, node, key, value=None):
        cursor = node.prev
        while (cursor.above is None):
            cursor = cursor.prev
        
        cursor = cursor.above
        below_node = node
        above_node = self.add_after(cursor, key, value)
        
        below_node.above = above_node
        above_node.below = below_node
        return above_node
    
    def delete_node(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

        item = node.item
        node.disconnect()
        return item

    def flip(self):
        return random.random() > 0.5
     
    def display(self):
        header = self.header
        while (header.below is not None):
            header = header.below

        cursor = header
        while (header is not None):
            while (cursor is not None):
                print(cursor.item, end='-')
                cursor = cursor.above
            print()
            header = header.next
            cursor = header

if __name__ == "__main__":
    sl = SkipList()
    for i in range(10):
        sl[i] = i
    
    for i in sl:
        print(i)