import random

class MinHeap:
    class Item:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value

        def __lt__(self, other):
            return self.key < other.key
        
        def __gt__(self, other):
            return self.key > other.key
        
        def __repr__(self):
            return str((self.key, self.value))

    def __init__(self):
        self.data = []
    
    def __len__(self):
        return len(self.data)
    
    def is_empty(self):
        return len(self) == 0
    
    def parent(self, index):
        return (index - 1) // 2

    def left(self, index):
        return 2 * index + 1
    
    def right(self, index):
        return 2 * index + 2

    def has_left(self, index):
        return self.left(index) < len(self.data)

    def has_right(self, index):
        return self.right(index) < len(self.data)

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def upheap(self, index):
        i = index
        while (i != 0):
            parent_index = self.parent(i)
            if (self.data[parent_index] > self.data[i]):
                self.swap(parent_index, i)
            i = parent_index

    def downheap(self, index):
        i = index
        while (self.has_left(i) or self.has_right(i)):
            items = [self.data[i]]
            if (self.has_left(i)):
                items.append(self.data[self.left(i)])
            if (self.has_right(i)):
                items.append(self.data[self.right(i)])
            
            min_item = min(items)
            min_index = i
            if (self.has_left(i) and min_item is self.data[self.left(i)]):
                min_index = self.left(i)
            elif (self.has_right(i) and min_item is self.data[self.right(i)]):
                min_index = self.right(i)
            
            if (min_index == i):
                break
            else:
                self.swap(min_index, i)
                i = min_index

    def add(self, key, value=None):
        new_item = MinHeap.Item(key, value)
        self.data.append(new_item)
        self.upheap(len(self.data) - 1)

    def min(self):
        if (self.is_empty()):
            raise Exception("MinHeap is empty")

        return (self.data[0].key, self.data[0].value)

    def remove_min(self):
        if (self.is_empty()):
            raise Exception("MinHeap is empty")

        if (len(self.data) == 1):
            min_item = self.data.pop()
        else:
            min_item = self.data[0]
            self.data[0] = self.data.pop()
            self.downheap(0)
            
        return (min_item.key, min_item.value)

def main():
    a = [i for i in range(100)]
    random.shuffle(a)
    heap = MinHeap()
    for i in a:
        heap.add(i)
    print(heap.data)
    while (not heap.is_empty()):
        print(heap.remove_min()[0])