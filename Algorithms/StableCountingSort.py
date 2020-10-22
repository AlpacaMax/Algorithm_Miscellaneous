def StableCountingSort(lst, low, high, key):
    """
    Sort a list of integers within a certain range using counting sort(stable)

    Parameters:
        lst: list = A list of integers
        low: int = the minimum value of the range
        high: int = the maximum value of the range
        key: func|method = A function or method which accepts an element of lst
                           as parameter and returns a key to use for sorting purposes
    
    Return:
        list = A sorted list
    """

    counter = [0] * (high - low + 1)
    order_maintain = [None] * (high - low + 1)

    for num in lst:
        counter[key(num) - low] += 1

    current = 0
    for i in range(len(counter)):
        current += counter[i]
        order_maintain[i] = current

    result = [0] * len(lst)
    for i in range(len(lst) - 1, -1, -1):
        elem = lst[i]
        index = order_maintain[key(elem) - low] - 1
        result[index] = elem
        order_maintain[key(elem) - low] -= 1
    
    return result