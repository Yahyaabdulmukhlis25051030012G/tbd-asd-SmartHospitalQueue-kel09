#===== Random Seed ===============================
import time
import random
import numpy as np

from dataclasses import dataclass
from typing import List

np.random.seed(42)
random.seed(42)

#===== DATA =====================================

POLI = ['Umum', 'Jantung', 'Ortopedi', 'Anak', 'Gigi']

PRIORITAS = {
    'KRITIS': 1,
    'PRIORITAS': 2,
    'REGULER': 3
}


@dataclass
class Pasien:
    no_antrian: int
    nama: str
    poli: str
    prioritas: int
    waktu_daftar: float
    waktu_tunggu: float = 0.0


@dataclass
class RekamMedis:
    no_rm: int
    nama: str
    riwayat: List[str]

#===== NODE ===================================

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

#==== PRIORITY QUEUE ==========================

class PriorityQueue:

    def __init__(self):
        self.head = None
        self._size = 0

    def enqueue(self, pasien):

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

        if not self.head:
            return None

        data = self.head.data
        self.head = self.head.next

        self._size -= 1

        return data

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self._size

#===== STACK ================================

class Stack:

    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):

        node = Node(data)

        node.next = self.top
        self.top = node

        self._size += 1

    def pop(self):

        if not self.top:
            return None

        data = self.top.data
        self.top = self.top.next

        self._size -= 1

        return data

    def is_empty(self):
        return self.top is None

    def __len__(self):
        return self._size
    
#===== BST ==============================

class BSTNode:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:

    def __init__(self):
        self.root = None

    # Big-O: O(log n)
    def insert(self, data):

        if not self.root:
            self.root = BSTNode(data)
            return

        self._insert(self.root, data)

    def _insert(self, node, data):

        if data.no_rm < node.data.no_rm:

            if not node.left:
                node.left = BSTNode(data)

            else:
                self._insert(node.left, data)

        else:

            if not node.right:
                node.right = BSTNode(data)

            else:
                self._insert(node.right, data)

    # Big-O: O(log n)
    def search(self, no_rm):
        return self._search(self.root, no_rm)

    def _search(self, node, no_rm):

        if not node:
            return None

        if node.data.no_rm == no_rm:
            return node.data

        if no_rm < node.data.no_rm:
            return self._search(node.left, no_rm)

        return self._search(node.right, no_rm)

    # Big-O: O(n)
    def inorder(self):

        result = []

        self._inorder(self.root, result)

        return result

    def _inorder(self, node, result):

        if node:

            self._inorder(node.left, result)

            result.append(node.data)

            self._inorder(node.right, result)

#===== INSERTION SORT ===========================

def insertion_sort(data):

    for i in range(1, len(data)):

        key = data[i]

        j = i - 1

        while j >= 0 and data[j].waktu_tunggu > key.waktu_tunggu:

            data[j + 1] = data[j]

            j -= 1

        data[j + 1] = key

    return data

#===== BENCHMARK =========================

class DummyPasien:
    def __init__(self, prioritas):
        self.prioritas = prioritas


def benchmark_queue(n):

    q = PriorityQueue()

    start = time.time()

    for _ in range(n):

        pasien = DummyPasien(
            random.randint(1, 3)
        )

        q.enqueue(pasien)

    while not q.is_empty():
        q.dequeue()

    end = time.time()

    return end - start

#===== MAIN SYSTEM ========================

def main():

    queues = {p: PriorityQueue() for p in POLI}

    stacks = {p: Stack() for p in POLI}

    bst = BST()

    selesai = []

    counter = 1

    print("\n===== SMART HOSPITAL SYSTEM =====")

    while True:

        print("\nMENU")
        print("1. DAFTAR PASIEN")
        print("2. PANGGIL PASIEN")
        print("3. UNDO")
        print("4. TAMBAH REKAM MEDIS")
        print("5. CARI REKAM MEDIS")
        print("6. LIHAT REKAM MEDIS")
        print("7. LAPORAN HARIAN")
        print("8. BENCHMARK")
        print("9. KELUAR")

        pilihan = input("Pilih menu (1-9): ")

#===== DAFTAR PASIEN =======================

        if pilihan == "1":

            print("\n--- DAFTAR PASIEN ---")

            nama = input("Nama pasien: ")

            poli = input(f"Poli {POLI}: ")

            prior = input(
                "Prioritas (KRITIS / PRIORITAS / REGULER): "
            ).upper()

            if poli not in POLI:
                print("Poli tidak valid")
                continue

            if prior not in PRIORITAS:
                print("Prioritas tidak valid")
                continue

            pasien = Pasien(
                counter,
                nama,
                poli,
                PRIORITAS[prior],
                time.time()
            )

            queues[poli].enqueue(pasien)

            counter += 1

            print("Pasien berhasil didaftarkan")

#===== PANGGIL PASIEN ===========================

        elif pilihan == "2":

            print("\n--- PANGGIL PASIEN ---")

            poli = input(f"Masukkan poli {POLI}: ")

            if poli not in POLI:
                print("Poli salah")
                continue

            pasien = queues[poli].dequeue()

            if pasien:

                pasien.waktu_tunggu = (
                    time.time() - pasien.waktu_daftar
                )

                selesai.append(pasien)

                stacks[poli].push(
                    f"Periksa {pasien.nama}"
                )

                print("Dipanggil:", pasien.nama)

            else:
                print("Antrian kosong")

#===== UNDO ===========================

        elif pilihan == "3":

            print("\n--- UNDO ---")

            poli = input("Masukkan poli: ")

            if poli not in POLI:
                print("❌ Poli salah")
                continue

            undo = stacks[poli].pop()

            if undo:
                print("↩️", undo)

            else:
                print("⚠️ Tidak ada data undo")


#===== MENAMBAH REKAM MEDIS ========================

        elif pilihan == "4":

            print("\n--- TAMBAH REKAM MEDIS ---")

            no_rm = int(input("No RM: "))

            nama = input("Nama: ")

            rm = RekamMedis(no_rm, nama, [])

            bst.insert(rm)

            print("💾 Rekam medis disimpan")

#===== MENCARI REKAM MEDIS =======================

        elif pilihan == "5":

            print("\n--- CARI REKAM MEDIS ---")

            no_rm = int(input("No RM: "))

            result = bst.search(no_rm)

            if result:
                print("Ditemukan:", result.nama)

            else:
                print("Tidak ditemukan")

#===== LIHAT REKAM MEDIS =====================

        elif pilihan == "6":

            print("\n--- DATA REKAM MEDIS ---")

            data = bst.inorder()

            if not data:
                print("Kosong")

            else:

                for d in data:
                    print(d.no_rm, d.nama)

#===== LAPORAN HARIAN ======================
        elif pilihan == "7":

            print("\n--- LAPORAN HARIAN ---")

            if not selesai:

                print("Belum ada pasien selesai")

            else:

                laporan = insertion_sort(selesai)

                for p in laporan:

                    print(
                        f"{p.nama} | "
                        f"{p.poli} | "
                        f"Waktu Tunggu: "
                        f"{p.waktu_tunggu:.2f} detik"
                    )

#===== BENCHMARK ==========================

        elif pilihan == "8":

            print("\n--- BENCHMARK QUEUE ---")

            for n in [50, 200, 500]:

                runtime = benchmark_queue(n)

                print(
                    f"N={n} -> "
                    f"{runtime:.6f} detik"
                )

#===== KELUAR =============================

        elif pilihan == "9":

            print("Sistem ditutup")

            break

        else:
            print("Pilihan tidak valid")

#===== RUN PROGRAM ========================

if __name__ == "__main__":
    main()