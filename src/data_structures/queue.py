from src.data_structures.node import Node

class PriorityQueue:
    def __init__(self):
        self.head = None
        self._size = 0

    def enqueue(self, pasien):
        """Big-O: O(n) insertion berdasarkan prioritas"""
        node = Node(pasien)

        if self.head is None or pasien.prioritas < self.head.data.prioritas:
            node.next = self.head
            self.head = node
            self._size += 1
            return

        cur = self.head
        while cur.next and cur.next.data.prioritas <= pasien.prioritas:
            cur = cur.next

        node.next = cur.next
        cur.next = node
        self._size += 1

    def dequeue(self):
        """Big-O: O(1) ambil dari head"""
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data

    def peek(self):
        """Big-O: O(1)"""
        return self.head.data if self.head else None

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size