import numpy as np, time, random
from dataclasses import dataclass, field
from typing import Optional, List

np.random.seed(42)
random.seed(42)

POLI = ['Umum', 'Jantung', 'Ortopedi', 'Anak', 'Gigi']
PRIORITAS = {'KRITIS': 1, 'PRIORITAS': 2, 'REGULER': 3}

@dataclass
class Pasien:
    no_antrian: int
    nama: str
    poli: str
    prioritas: int      # 1=KRITIS, 2=PRIORITAS, 3=REGULER
    waktu_daftar: float # time.time()
    waktu_tunggu: float = 0.0

@dataclass
class RekorMedis:
    no_rm: int          # kunci BST
    nama: str
    riwayat: List[str]  # list tindakan

# ── Node untuk Linked List ─────────────────────────────────────────
class LLNode:
    __slots__ = 'data', 'next' 

    def __init__(self, data=None, next=None): 
        self.data = data
        self.next = next

# ── Priority Queue ─────────────────────────────────────────────────

class PriorityQueue:
    """Priority Queue berbasis Singly Linked List, terurut prioritas ASC."""
    def __init__(self):
        self.head: Optional[LLNode] = None
        self._size: int = 0

    def enqueue(self, pasien: Pasien) -> None:
        """
        Big-O waktu: O(n) sisipkan pada posisi prioritas.
        Logika: Mencari posisi berdasarkan angka prioritas (1=KRITIS, 2=PRIORITAS, 3=REGULER).
        Mendukung tie-break FIFO untuk prioritas yang sama.
        """
        new_node = LLNode(pasien)
        
        # Kasus 1: Antrean kosong atau pasien baru lebih prioritas (angka lebih kecil) dari head
        if self.head is None or pasien.prioritas < self.head.data.prioritas:
            new_node.next = self.head
            self.head = new_node
        else:
            # Kasus 2: Iterasi (link hopping) untuk mencari posisi penyisipan yang tepat
            # Gunakan '<=' agar pasien baru dengan prioritas sama diletakkan di BELAKANG 
            # pasien lama (memenuhi aturan tie-break FIFO) [2, 3].
            current = self.head
            while current.next is not None and current.next.data.prioritas <= pasien.prioritas:
                current = current.next
            
            # Hubungkan node baru ke dalam rantai linked list
            new_node.next = current.next
            current.next = new_node
            
        self._size += 1

    def dequeue(self) -> Optional[Pasien]:
        """
        Big-O waktu: O(1) selalu ambil head.
        Logika: Menghapus dan mengembalikan data dari node terdepan (head) [2, 4].
        """
        if self.is_empty():
            return None
        
        # Simpan data pasien yang akan keluar
        pasien_keluar = self.head.data
        # Geser head ke node berikutnya (pointer hopping) [5, 6]
        self.head = self.head.next
        self._size -= 1
        return pasien_keluar

    def peek(self) -> Optional[Pasien]:
        """
        Big-O waktu: O(1).
        Logika: Melihat data pada head tanpa menghapusnya [7, 8].
        """
        if self.is_empty():
            return None
        return self.head.data

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size