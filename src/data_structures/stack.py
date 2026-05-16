# =====================================================
# STACK MODULE
# Stack berbasis Singly Linked List, LIFO
# Big-O: push O(1), pop O(1), peek O(1)
# =====================================================

from typing import Optional


class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None


class Stack:
    """Stack berbasis Singly Linked List, LIFO."""
    def __init__(self):
        self.top: Optional[LLNode] = None
        self._size: int = 0

    def push(self, tindakan: str) -> None:
        """Big-O waktu: O(1)"""
        node = LLNode(tindakan)
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self) -> Optional[str]:
        """Big-O waktu: O(1)"""
        if not self.top:
            return None
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self) -> Optional[str]:
        """Big-O waktu: O(1)"""
        return self.top.data if self.top else None

    def is_empty(self) -> bool:
        return self._size == 0

    def log_all(self) -> None:
        """Tampilkan semua tindakan dalam stack. Big-O: O(n)"""
        if self.is_empty():
            print("⚠️ Stack kosong")
            return
        cur = self.top
        print("📋 Riwayat tindakan (terbaru ke terlama):")
        while cur:
            print(f"  - {cur.data}")
            cur = cur.next

    def __len__(self) -> int:
        return self._size