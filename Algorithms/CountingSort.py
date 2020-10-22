def CountingSort(lst, low, high):
    """
    Sort a list of integers within a certain range using counting sort(unstable)

    Parameters:
        lst: list = A list of integers
        low: int = the minimum value of the range
        high: int = the maximum value of the range
    """

    counter = [0] * (high - low + 1)

    for num in lst:
        counter[num - low] += 1
    
    index = 0
    for i in range(len(counter)):
        for rep in range(counter[i]):
            lst[index] = low + i
            index += 1