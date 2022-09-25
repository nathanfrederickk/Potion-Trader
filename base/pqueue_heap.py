""" Heap implemented using an array"""

from typing import Generic
from referential_array import ArrayR, T


class Heap(Generic[T]):
    MIN_CAPACITY = 1

    def __init__(self, max_size: int) -> None:
        self.length = 0
        self.the_array = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)

    def __len__(self) -> int:
        return self.length

    def is_full(self) -> bool:
        return self.length + 1 == len(self.the_array)

    def add(self, element: T) -> bool:
        """
        Combined into one method
        More efficient but less readable
        """
        has_space_left = not self.is_full()

        if has_space_left:
            self.length += 1
            k = self.length
            while k > 1 and element > self.the_array[k // 2]:
                self.the_array[k] = self.the_array[k // 2]
                k = k // 2

            self.the_array[k] = element

        return has_space_left

    def largest_child(self, k: int) -> int:
        """
        Returns the index of the largest child of k.
        pre: 2*k <= self.length (at least one child)
        """
        if 2 * k == self.length or self.the_array[2 * k] > self.the_array[2 * k + 1]:
            return 2*k
        else:
            return 2*k+1

    def sink(self, k: int) -> None:
        """ Make the element at index k sink to the correct position """
        while 2*k <= self.length:
            child = self.largest_child(k)
            if self.the_array[k] >= self.the_array[child]:
                break
            self.the_array[child], self.the_array[k] = self.the_array[k], self.the_array[child]
            k = child

    def create_heap(self, max_size: int, an_array: ArrayR[T] = None) -> None:
        """
        If elements are known in advance, they are in an_array
        Assume that max_size=len(an_array) if given
        """
        self.the_array = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)
        self.length = max_size

        if an_array is not None:
            # copy an_array to self.the_array (shift by 1)
            for i in range(self.length):
                self.the_array[i+1] = an_array[i]

            # heapify every parent
            for i in range(max_size//2, 0, -1):
                self.sink(i)
                
    def get_max(self) -> T:
        if self.length == 0:
            raise ValueError('No elems')
        self.swap(1, self.length)
        res = self.the_array[self.length]
        self.length -= 1
        self.sink(1)
        return (res, self.length)
    
    def swap(self, i, j):
        self.the_array[i], self.the_array[j] = self.the_array[j], self.the_array[i]