from src.data_structures.node import Node

class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        """Big-O: O(1)"""
        node = Node(data)
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self):
        """Big-O: O(1)"""
        if not self.top:
            return None
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):
        """Big-O: O(1)"""
        return self.top.data if self.top else None

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size