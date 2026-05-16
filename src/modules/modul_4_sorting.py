# =====================================================
# SORTING MODULE
# Insertion Sort & Selection Sort pada Linked List
# Big-O: O(n²)
# =====================================================

import numpy as np
import time
np.random.seed(42)

from typing import Optional


class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None


class LinkedListPasien:
    """Linked List untuk menyimpan daftar pasien selesai"""
    def __init__(self):
        self.head: Optional[LLNode] = None
        self._size: int = 0

    def append(self, pasien) -> None:
        """Tambah pasien di akhir. Big-O: O(n)"""
        node = LLNode(pasien)
        if not self.head:
            self.head = node
            self._size += 1
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node
        self._size += 1

    def to_list(self):
        """Konversi ke Python list. Big-O: O(n)"""
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def __len__(self):
        return self._size


def insertion_sort_waktu_tunggu(ll: LinkedListPasien) -> LinkedListPasien:
    """
    Insertion Sort berdasarkan waktu_tunggu DESCENDING.
    Implementasi langsung pada Linked List.
    Big-O: O(n²) worst-case, O(n) best-case (data hampir terurut)
    """
    if not ll.head or not ll.head.next:
        return ll

    sorted_head = None

    cur = ll.head
    while cur:
        next_node = cur.next
        cur.next = None

        if sorted_head is None or cur.data.waktu_tunggu > sorted_head.data.waktu_tunggu:
            cur.next = sorted_head
            sorted_head = cur
        else:
            temp = sorted_head
            while temp.next and temp.next.data.waktu_tunggu >= cur.data.waktu_tunggu:
                temp = temp.next
            cur.next = temp.next
            temp.next = cur

        cur = next_node

    result = LinkedListPasien()
    result.head = sorted_head
    result._size = ll._size
    return result


def selection_sort_no_antrian(ll: LinkedListPasien) -> LinkedListPasien:
    """
    Selection Sort berdasarkan no_antrian ASCENDING.
    Implementasi langsung pada Linked List.
    Big-O: O(n²) selalu
    """
    if not ll.head or not ll.head.next:
        return ll

    cur = ll.head
    while cur:
        min_node = cur
        check = cur.next
        while check:
            if check.data.no_antrian < min_node.data.no_antrian:
                min_node = check
            check = check.next

        cur.data, min_node.data = min_node.data, cur.data
        cur = cur.next

    return ll