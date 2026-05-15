import time
from dataclasses import dataclass
from typing import Optional, List


# =====================================================
# DATA
# =====================================================
POLI = ['Umum', 'Jantung', 'Ortopedi', 'Anak', 'Gigi']
PRIORITAS = {'KRITIS': 1, 'PRIORITAS': 2, 'REGULER': 3}


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


# =====================================================
# NODE
# =====================================================
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


# =====================================================
# PRIORITY QUEUE
# =====================================================
class PriorityQueue:
    def __init__(self):
        self.head = None

    def enqueue(self, pasien):
        node = Node(pasien)

        if self.head is None or pasien.prioritas < self.head.data.prioritas:
            node.next = self.head
            self.head = node
            return

        cur = self.head
        while cur.next and cur.next.data.prioritas <= pasien.prioritas:
            cur = cur.next

        node.next = cur.next
        cur.next = node

    def dequeue(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        return data


# =====================================================
# STACK
# =====================================================
class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        node = Node(data)
        node.next = self.top
        self.top = node

    def pop(self):
        if not self.top:
            return None
        data = self.top.data
        self.top = self.top.next
        return data


# =====================================================
# BST
# =====================================================
class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

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

    def inorder(self):
        res = []
        self._inorder(self.root, res)
        return res

    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.data)
            self._inorder(node.right, res)


# =====================================================
# MAIN SYSTEM (INTERAKTIF MENU STEP BY STEP)
# =====================================================
def main():
    queues = {p: PriorityQueue() for p in POLI}
    stacks = {p: Stack() for p in POLI}
    bst = BST()

    selesai = []
    counter = 1

    print("\n===== SMART HOSPITAL SYSTEM =====")

    while True:

        print("\nMENU:")
        print("1. DAFTAR PASIEN")
        print("2. PANGGIL PASIEN")
        print("3. UNDO")
        print("4. TAMBAH REKAM MEDIS")
        print("5. CARI REKAM MEDIS")
        print("6. LIHAT REKAM MEDIS")
        print("7. KELUAR")

        pilihan = input("Pilih menu (1-7): ")

        # =========================
        # DAFTAR
        # =========================
        if pilihan == "1":
            print("\n--- DAFTAR PASIEN ---")
            nama = input("Nama pasien: ")
            poli = input(f"Poli {POLI}: ")
            prior = input("Prioritas (KRITIS / PRIORITAS / REGULER): ").upper()

            if poli not in POLI:
                print("❌ Poli tidak valid")
                continue

            if prior not in PRIORITAS:
                print("❌ Prioritas tidak valid")
                continue

            p = Pasien(counter, nama, poli, PRIORITAS[prior], time.time())
            queues[poli].enqueue(p)
            counter += 1

            print("✅ Pasien berhasil didaftarkan")

        # =========================
        # PANGGIL
        # =========================
        elif pilihan == "2":
            print("\n--- PANGGIL PASIEN ---")
            poli = input(f"Masukkan poli {POLI}: ")

            if poli not in POLI:
                print("❌ Poli salah")
                continue

            p = queues[poli].dequeue()

            if p:
                p.waktu_tunggu = time.time() - p.waktu_daftar
                selesai.append(p)
                stacks[poli].push(f"Periksa {p.nama}")
                print("📢 Dipanggil:", p.nama)
            else:
                print("⚠️ Antrian kosong")

        # =========================
        # UNDO
        # =========================
        elif pilihan == "3":
            print("\n--- UNDO ---")
            poli = input("Masukkan poli: ")
            print("↩️", stacks[poli].pop())

        # =========================
        # TAMBAH RM
        # =========================
        elif pilihan == "4":
            print("\n--- TAMBAH REKAM MEDIS ---")
            no_rm = int(input("No RM: "))
            nama = input("Nama: ")

            bst.insert(RekamMedis(no_rm, nama, []))
            print("💾 Rekam medis disimpan")

        # =========================
        # CARI RM
        # =========================
        elif pilihan == "5":
            print("\n--- CARI REKAM MEDIS ---")
            no_rm = int(input("No RM: "))

            res = bst.search(no_rm)
            if res:
                print("🔍 Ditemukan:", res.nama)
            else:
                print("❌ Tidak ditemukan")

        # =========================
        # LIHAT RM
        # =========================
        elif pilihan == "6":
            print("\n--- DATA REKAM MEDIS ---")
            data = bst.inorder()

            if not data:
                print("Kosong")
            else:
                for d in data:
                    print(d.no_rm, d.nama)

        # =========================
        # KELUAR
        # =========================
        elif pilihan == "7":
            print("👋 Sistem ditutup")
            break

        else:
            print("❌ Pilihan tidak valid")


if __name__ == "__main__":
    main()