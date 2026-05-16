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
prioritas: int # 1=KRITIS, 2=PRIORITAS, 3=REGULER
waktu_daftar: float # time.time()
waktu_tunggu: float = 0.0
@dataclass
class RekorMedis:
no_rm: int # kunci BST
nama: str
riwayat: List[str] # list tindakan

# ── Node untuk Linked List ─────────────────────────────────────────
class LLNode:
def __init__(self, data=None):
self.data = data
self.next: Optional['LLNode'] = None

# ── Priority Queue (implementasikan dari sini) ──────────────────────
class PriorityQueue:
"""Priority Queue berbasis Singly Linked List, terurut prioritas ASC."""
def __init__(self):
self.head: Optional[LLNode] = None
self._size: int = 0
def enqueue(self, pasien: Pasien) -> None:
"""Big-O waktu: O(n) sisipkan pada posisi prioritas."""
# TODO: implementasikan insertion berdasarkan prioritas
pass
def dequeue(self) -> Optional[Pasien]:
"""Big-O waktu: O(1) selalu ambil head."""
# TODO: implementasikan
pass
def peek(self) -> Optional[Pasien]:
"""Big-O waktu: O(1)."""
# TODO: implementasikan
pass
def is_empty(self) -> bool:
    return self._size == 0
def __len__(self) -> int:
return self._size

# ── Stack (implementasikan dari sini) ───────────────────────────────
class Stack:
"""Stack berbasis Singly Linked List, LIFO."""
def __init__(self):
self.top: Optional[LLNode] = None
self._size: int = 0
def push(self, tindakan: str) -> None:
"""Big-O waktu: O(1)."""
# TODO: implementasikan
pass
def pop(self) -> Optional[str]:
"""Big-O waktu: O(1)."""
# TODO: implementasikan
pass
def peek(self) -> Optional[str]:
# TODO: implementasikan
pass

# ── BST Node & BST (implementasikan dari sini) ─────────────────────
class BSTNode:
def __init__(self, rekord: RekorMedis):
self.rekord = rekord
self.left: Optional['BSTNode'] = None
self.right: Optional['BSTNode'] = None
class BSTRekamMedis:
def __init__(self):
self.root: Optional[BSTNode] = None
def insert(self, rekord: RekorMedis) -> None:
"""Big-O waktu: rata-rata O(log n), worst-case O(n)."""
# TODO: implementasikan secara rekursif atau iteratif
pass
def search(self, no_rm: int) -> Optional[RekorMedis]:
"""Big-O waktu: rata-rata O(log n), worst-case O(n)."""
# TODO: implementasikan
pass
def inorder(self) -> List[RekorMedis]:
"""Big-O waktu: O(n) menghasilkan rekam medis terurut."""
# TODO: implementasikan traversal inorder
pass

# ── Skeleton CLI (implementasikan dari sini) ─────────────────────────
def main():
queues = {poli: PriorityQueue() for poli in POLI}
dokter_stacks = {i: Stack() for i in range(len(POLI))}
bst_rm = BSTRekamMedis()
counter = 0
# TODO: implementasikan loop CLI
print('Smart Hospital Queue System Ketik BANTUAN untuk daftar perintah')
if __name__ == '__main__':
main()