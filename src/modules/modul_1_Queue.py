import time
from dataclasses import dataclass
from typing import Optional

# 1. Definisi Data Pasien (Sesuai Parameter Sistem)
@dataclass
class Pasien:
    no_antrian: int
    nama: str
    poli: str
    prioritas: int          # 1=KRITIS, 2=PRIORITAS, 3=REGULER
    waktu_daftar: float     # Menggunakan time.time()
    waktu_tunggu: float = 0.0

# 2. Node untuk Linked List
class LLNode:
    def __init__(self, data: Pasien = None):
        self.data = data
        self.next: Optional['LLNode'] = None

# 3. Struktur Data Priority Queue
class PriorityQueue:
    """
    Priority Queue berbasis Singly Linked List dengan pengurutan prioritas menaik (ASC).
    Pasien KRITIS (1) akan selalu berada di depan antrean.
    """
    def __init__(self):
        self.head: Optional[LLNode] = None
        self._size: int = 0

    def enqueue(self, pasien: Pasien) -> None:
        """
        Menambahkan pasien ke antrean berdasarkan tingkat prioritas.
        Analisis Big-O: O(n) worst-case karena harus mencari posisi yang tepat (geser prioritas).
        """
        new_node = LLNode(pasien)
        
        # Kasus 1: Antrean kosong atau prioritas pasien lebih tinggi (angka lebih kecil) dari head
        if self.head is None or pasien.prioritas < self.head.data.prioritas:
            new_node.next = self.head
            self.head = new_node
        else:
            # Kasus 2: Cari posisi sisip (tie-break menggunakan prinsip FIFO)
            curr = self.head
            while curr.next is not None and curr.next.data.prioritas <= pasien.prioritas:
                curr = curr.next
            
            new_node.next = curr.next
            curr.next = new_node
            
        self._size += 1

    def dequeue(self) -> Optional[Pasien]:
        """
        Mengambil pasien dari urutan terdepan.
        Analisis Big-O: O(1) karena hanya menghapus head.
        """
        if self.is_empty():
            return None
        
        target_pasien = self.head.data
        self.head = self.head.next
        self._size -= 1
        return target_pasien

    def peek(self) -> Optional[Pasien]:
        """Melihat pasien terdepan tanpa menghapusnya. Big-O: O(1)."""
        return self.head.data if self.head else None

    def is_empty(self) -> bool:
        """Mengecek apakah antrean kosong. Big-O: O(1)."""
        return self._size == 0

    def __len__(self) -> int:
        """Mengembalikan jumlah pasien dalam antrean. Big-O: O(1)."""
        return self._size
