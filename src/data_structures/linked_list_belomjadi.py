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

if __name__ == "__main__":
    # 1. Buat node pertama (ekor antrean)
    node_belakang = LLNode("Pasien Budi")
    
    # 2. Buat node kedua dan hubungkan ke node pertama (kepala antrean)
    node_depan = LLNode("Pasien Andi", node_belakang)
    
    # 3. Verifikasi data menggunakan nama atribut yang benar
    print(f"Data di node depan: {node_depan.data}")
    print(f"Data di node berikutnya: {node_depan.next.data}")
    
    # 4. Tes apakah node belakang menunjuk ke None (akhir list)
    if node_belakang.next is None:
        print("Pengetesan LLNode Berhasil!")