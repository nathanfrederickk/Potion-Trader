""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
It currently rehashes the primary cluster to handle deletion.
"""
__author__ = 'Brendon Taylor, modified by Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'

from referential_array import ArrayR
from typing import TypeVar, Generic
from potion import Potion
T = TypeVar('T')


class LinearProbePotionTable(Generic[T]):
    """
    Linear Probe Potion Table

    This potion table does not support deletion.

    attributes:
        count: number of elements in the hash table
        table: used to represent our internal array
        table_size: current size of the hash table
    """
    
    def __init__(self, max_potions: int, good_hash: bool = True, tablesize_override: int = -1) -> None:
        """
        Constructor
        
        :param max_potions: maximum number of elements that will be added to the hash table
        :param good_hash: boolean value for using either a good or a bad hash
        :param tablesize_override: choice of table size
        :complexity: O(1)
        """
        # Statistic setting
        self.conflict_count = 0
        self.probe_max = 0
        self.probe_total = 0
        self.count = 0
        self.hash_key = True if good_hash else False
        
        if tablesize_override != -1:
            self.table_size = tablesize_override
        else:
            # select a reasonable choice for tablesize_override, given the value of max_potion
            self.table_size = max_potions
        self.table = [None for _ in range(self.table_size)]
            
    def hash(self, potion_name: str) -> int:
        """
        It is an instance method which hashes a potion name and returns the hash value computed by 
        either a good_hash function or a bad_hash function based on hash_key
        
        :param potion_name: Name of the potion
        :return: Unique key
        :complexity: O(1)
        """
        if self.hash_key:
            return Potion.good_hash(potion_name, self.table_size)
        else:
            return Potion.bad_hash(potion_name, self.table_size)

    def statistics(self) -> tuple:
        """
        It is an instance method which returns a tuple consists of conflict_count, probe_total and 
        probe_max, where conflict_count is the total number of conflicts, probe_total is the total
        distance probed throughout the execution of the code and probe_max is the length of the longest 
        probe chain throughout the execution of the code.

        :return: a tuple
        :complexity: O(1)
        """
        return self.conflict_count, self.probe_total, self.probe_max

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        :complexity: O(1)
        """
        return self.count

    def __linear_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using linear probing
        :complexity best: O(K) first position is empty
                          where K is the size of the key
        :complexity worst: O(K + N) when we've searched the entire table
                           where N is the table_size
        :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash
        conflict = False  # to determine if there is a conflict
        probe_counter = 0  # to determine the number of probe happening

        if is_insert and self.is_full():
            raise KeyError(key)

        for _ in range(len(self.table)):  # start traversing
            if conflict and probe_counter == 1:
                self.conflict_count += 1
            if probe_counter > self.probe_max:
                self.probe_max = probe_counter
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    return position
                else:
                    raise KeyError(key)  # raise error if the key is not in the table
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is an existing key in that position but not the key that we want, try next
                position = (position + 1) % len(self.table)
                self.probe_total += 1   # adds one to the total probe counter
                conflict = True         # there is a conflict
                probe_counter += 1 

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table
        :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
        Get the item at a certain key
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :raises KeyError: when the item doesn't exist
        """
        position = self.__linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
        Set an (key, data) pair in our hash table
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :see: #self.__contains__(key: str)
        """
        if len(self) == len(self.table) and key not in self:
            raise ValueError("Cannot insert into a full table.")
        position = self.__linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1
        self.table[position] = (key, data)

    def initalise_with_tablesize(self, tablesize: int) -> None:
        """
        Initialise a new array, with table size given by tablesize.
        Complexity: O(n), where n is len(tablesize)
        """
        self.count = 0
        self.table = ArrayR(tablesize)

    def is_empty(self):
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
        Returns whether the hash table is full
        :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
        Utility method to call our setitem method
        :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
