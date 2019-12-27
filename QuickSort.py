import random

def QuickSort(lst):
    def partition(lst, low, high):
        left = low
        mid_value = lst[high]
        while (lst[left] < mid_value):
            left += 1
        right = left

        while (right <= high):
            if (lst[right] < mid_value):
                lst[left], lst[right] = lst[right], lst[left]
                left += 1
            right += 1
        lst[high], lst[left] = lst[left], lst[high]
        return left
    
    def helper(lst, low, high):
        if (low < high):
            mid = partition(lst, low, high)
            helper(lst, low, mid - 1)
            helper(lst, mid + 1, high)
    
    if (len(lst) > 0):
        helper(lst, 0, len(lst) - 1)
                
if __name__ == '__main__':
    lst = [i for i in range(100)]
    random.shuffle(lst)
    QuickSort(lst)
    print(lst)