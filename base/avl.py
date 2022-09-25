""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is 
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_left_counter(self, current: AVLTreeNode) -> int:
        """
            Get the number of all the nodes on the left side of current
            starting from current.left. If current is None or current.left is None,
            it returns 0.
            :complexity: O(1)
        """
        if current is not None and current.left is not None:
            return current.left_counter
        return 0

    def get_right_counter(self, current: AVLTreeNode) -> int:
        """
            Get the number of all the nodes on the right side of current
            starting from current.right. If current is None or current.right is None,
            it returns 0.
            :complexity: O(1)
        """
        if current is not None and current.right is not None:
            return current.right_counter
        return 0

    def get_total_counter(self, current: AVLTreeNode) -> int:
        """
            Get the number of all the nodes below current starting from
            current.left and current.right. If current is None, it will return 
            0.
            :complexity: O(1)
        """
        if current is not None:
            return self.get_left_counter(current) + self.get_right_counter(current)
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """
        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
            returns the new root of the subtree.
            :Complexity: O(Compk * N), where N is the depth of the tree, CompK 
                         is the complexity of comparing the keys
        """
        if current is None:     # base case at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')

        self.update_height(current)
        self.update_counter(current)
        return self.rebalance(current)

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion,
            performs sub-tree rotation whenever it becomes unbalanced.
            returns the new root of the subtree.
            :Complexity: O(Compk * N), where N is the depth of the tree, CompK 
                         is the complexity of comparing the keys
        """
        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left_counter -= 1
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right_counter -= 1
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        self.update_height(current)
        self.update_counter(current)
        return self.rebalance(current)
    
    def update_height(self, current: AVLTreeNode) -> None:
        """
            Get the height of the AVL tree
            :complexity: O(1)
        """
        if current is None:
            return 
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """

        if current.right is not None:
            child = current.right
            current.right, child.left = child.left, current
            self.update_height(current)
            self.update_counter(current)
            self.update_height(child)
            self.update_counter(child)
            return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        if current.left is not None:
            child = current.left
            current.left, child.right = child.right, current
            self.update_height(current)
            self.update_counter(current)
            self.update_height(child)
            self.update_counter(child)
            return child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:  # right-left >= 2 means right subtree has more node so right subtree need to roate to left side (left rotate)
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:  # right-left <= 2 means left subtree has more node so left subtree need to roate to right side (right rotate)
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def update_counter(self, current: AVLTreeNode) -> None:
        """
            Updates the current.right_counter and current.left_counter.
            :complexity: O(1)
        """
        if current is not None:
            if current.right is not None:
                current.right_counter = self.get_total_counter(current.right) + 1
            if current.left is not None:
                current.left_counter = self.get_total_counter(current.left) + 1

    def kth_largest(self, k: int) -> AVLTreeNode:
        """
            Returns the kth largest element in the tree.
            k=1 would return the largest.
            :complexity: O(log(N)), where N is the total number of nodes in the tree.
        """
        return self.kth_largest_helper(self.root, k)

    def kth_largest_helper(self, root: AVLTreeNode, k: int) -> AVLTreeNode:
        """
            Recursive function to help find the kth largest
            element in the tree. K = 1 would return the largest element
            in the AVLTree.
            :complexity: O(log(N)), where N is the total number of nodes in the tree.
        """
        if k == self.get_right_counter(root) + 1:
            return root
        elif k < self.get_right_counter(root) + 1:
            if root.right is None:
                return root
            return self.kth_largest_helper(root.right, k)
        else:   # k > self.get_right_counter(root) + 1
            if root.left is None:
                return root
            return self.kth_largest_helper(root.left, k - root.right_counter - 1)

# **kth_largest() reference from: https://www.enjoyalgorithms.com/blog/kth-largest-element-in-bst
       
