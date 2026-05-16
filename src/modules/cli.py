# =====================================================
# CLI MODULE
# Antarmuka Command Line Interface
# Big-O ditampilkan setiap operasi
# =====================================================

import time
import numpy as np
import random
from dataclasses import dataclass
from typing import Optional, List

from src.modules.sorting import (
    LinkedListPasien,
    insertion_sort_waktu_tunggu,
    selection_sort_no_antrian
)

np.random.seed(42)
random.seed(42)

POLI = ['Umum', 'Jantung', 'Ortopedi', 'Anak', 'Gigi']
PRIORITAS = {'KRITIS': 1, 'PRIORITAS': 2, 'REGULER': 3}


# =====================================================
# DATA CLASS
# =====================================================
@dataclass
class Pasien:
    no_antrian: int
    nama: str
    poli: str
    prioritas: int
    waktu_daftar: float
    waktu_tunggu: float = 0.0


@dataclass
class RekorMedis:
    no_rm: int
    nama: str
    riwayat: List[str]


# =====================================================
# NODE
# =====================================================
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None


# =====================================================
# PRIORITY QUEUE
# =====================================================
class PriorityQueue:
    """Priority Queue berbasis Singly Linked List, terurut prioritas ASC"""
    def __init__(self):
        self.head: Optional[LLNode] = None
        self._size: int = 0

    def enqueue(self, pasien: Pasien) -> None:
        """Big-O waktu: O(n) sisipkan pada posisi prioritas"""
        node = LLNode(pasien)

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

    def dequeue(self) -> Optional[Pasien]:
        """Big-O waktu: O(1) selalu ambil head"""
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data

    def peek(self) -> Optional[Pasien]:
        """Big-O waktu: O(1)"""
        return self.head.data if self.head else None

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size


# =====================================================
# STACK
# =====================================================
class Stack:
    """Stack berbasis Singly Linked List, LIFO"""
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

    def __len__(self) -> int:
        return self._size


# =====================================================
# BST
# =====================================================
class BSTNode:
    def __init__(self, rekord: RekorMedis):
        self.rekord = rekord
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BSTRekamMedis:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, rekord: RekorMedis) -> None:
        """Big-O waktu: rata-rata O(log n), worst-case O(n)"""
        if not self.root:
            self.root = BSTNode(rekord)
            return
        self._insert(self.root, rekord)

    def _insert(self, node: BSTNode, rekord: RekorMedis) -> None:
        if rekord.no_rm < node.rekord.no_rm:
            if not node.left:
                node.left = BSTNode(rekord)
            else:
                self._insert(node.left, rekord)
        else:
            if not node.right:
                node.right = BSTNode(rekord)
            else:
                self._insert(node.right, rekord)

    def search(self, no_rm: int) -> Optional[RekorMedis]:
        """Big-O waktu: rata-rata O(log n), worst-case O(n)"""
        return self._search(self.root, no_rm)

    def _search(self, node: Optional[BSTNode], no_rm: int) -> Optional[RekorMedis]:
        if not node:
            return None
        if node.rekord.no_rm == no_rm:
            return node.rekord
        if no_rm < node.rekord.no_rm:
            return self._search(node.left, no_rm)
        return self._search(node.right, no_rm)

    def inorder(self) -> List[RekorMedis]:
        """Big-O waktu: O(n)"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[BSTNode], result: list) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.rekord)
            self._inorder(node.right, result)


# =====================================================
# FUNGSI CLI
# =====================================================
def tampilkan_menu():
    print("\n===== SMART HOSPITAL SYSTEM =====")
    print("MENU:")
    print("1. DAFTAR PASIEN")
    print("2. PANGGIL PASIEN")
    print("3. UNDO")
    print("4. TAMBAH REKAM MEDIS")
    print("5. CARI REKAM MEDIS")
    print("6. LIHAT REKAM MEDIS")
    print("7. LAPORAN HARI")
    print("8. KELUAR")


def daftar_pasien(queues, counter):
    print("\n--- DAFTAR PASIEN ---")
    nama = input("Nama pasien: ")
    poli = input(f"Poli {POLI}: ")
    prior = input("Prioritas (KRITIS/PRIORITAS/REGULER): ").upper()

    if poli not in POLI:
        print("❌ Poli tidak valid")
        return counter
    if prior not in PRIORITAS:
        print("❌ Prioritas tidak valid")
        return counter

    p = Pasien(counter, nama, poli, PRIORITAS[prior], time.time())
    queues[poli].enqueue(p)
    counter += 1
    print(f"✅ Pasien didaftarkan | Big-O enqueue: O(n)")
    return counter


def panggil_pasien(queues, stacks, selesai):
    print("\n--- PANGGIL PASIEN ---")
    poli = input(f"Poli {POLI}: ")

    if poli not in POLI:
        print("❌ Poli tidak valid")
        return

    p = queues[poli].dequeue()
    if p:
        p.waktu_tunggu = time.time() - p.waktu_daftar
        selesai.append(p)
        stacks[poli].push(f"Periksa {p.nama}")
        print(f"📢 Dipanggil: {p.nama} | Big-O dequeue: O(1)")
    else:
        print("⚠️ Antrian kosong")


def undo_tindakan(stacks):
    print("\n--- UNDO ---")
    poli = input(f"Poli {POLI}: ")

    if poli not in POLI:
        print("❌ Poli tidak valid")
        return

    hasil = stacks[poli].pop()
    if hasil:
        print(f"↩️ Undo: {hasil} | Big-O pop: O(1)")
    else:
        print("⚠️ Tidak ada tindakan untuk di-undo")


def tambah_rekam_medis(bst):
    print("\n--- TAMBAH REKAM MEDIS ---")
    try:
        no_rm = int(input("No RM: "))
        nama = input("Nama: ")
        bst.insert(RekorMedis(no_rm, nama, []))
        print(f"💾 Rekam medis disimpan | Big-O insert BST: O(log n)")
    except ValueError:
        print("❌ No RM harus berupa angka")


def cari_rekam_medis(bst):
    print("\n--- CARI REKAM MEDIS ---")
    try:
        no_rm = int(input("No RM: "))
        res = bst.search(no_rm)
        if res:
            print(f"🔍 Ditemukan: {res.nama} | Big-O search BST: O(log n)")
        else:
            print("❌ Tidak ditemukan")
    except ValueError:
        print("❌ No RM harus berupa angka")


def lihat_rekam_medis(bst):
    print("\n--- DATA REKAM MEDIS ---")
    data = bst.inorder()
    if not data:
        print("⚠️ Kosong")
    else:
        print(f"{'No RM':<10} {'Nama'}")
        print("-" * 30)
        for d in data:
            print(f"{d.no_rm:<10} {d.nama}")
    print("Big-O inorder: O(n)")


def laporan_hari(selesai):
    print("\n--- LAPORAN HARI ---")

    if not selesai:
        print("⚠️ Belum ada pasien selesai hari ini")
        return

    ll = LinkedListPasien()
    for p in selesai:
        ll.append(p)

    print("\nUrut berdasarkan:")
    print("  a. Waktu tunggu terlama (Insertion Sort)")
    print("  b. Nomor antrian (Selection Sort)")
    sub = input("Pilih (a/b): ").lower()

    if sub == "a":
        ll_sorted = insertion_sort_waktu_tunggu(ll)
        print(f"\n📋 Laporan - Waktu Tunggu Terlama | Big-O: O(n²)")
        print(f"{'No':<5} {'Nama':<20} {'Poli':<12} {'Prioritas':<10} {'Tunggu (s)'}")
        print("-" * 60)
        for p in ll_sorted.to_list():
            print(f"{p.no_antrian:<5} {p.nama:<20} {p.poli:<12} {p.prioritas:<10} {p.waktu_tunggu:.4f}")

    elif sub == "b":
        ll_sorted = selection_sort_no_antrian(ll)
        print(f"\n📋 Laporan - No Antrian | Big-O: O(n²)")
        print(f"{'No':<5} {'Nama':<20} {'Poli':<12} {'Prioritas':<10} {'Tunggu (s)'}")
        print("-" * 60)
        for p in ll_sorted.to_list():
            print(f"{p.no_antrian:<5} {p.nama:<20} {p.poli:<12} {p.prioritas:<10} {p.waktu_tunggu:.4f}")
    else:
        print("❌ Pilihan tidak valid")


def jalankan_cli():
    """Fungsi utama CLI"""
    queues = {poli: PriorityQueue() for poli in POLI}
    stacks = {poli: Stack() for poli in POLI}
    bst = BSTRekamMedis()
    selesai = []
    counter = 1

    while True:
        tampilkan_menu()
        pilihan = input("\nPilih menu (1-8): ")

        if pilihan == "1":
            counter = daftar_pasien(queues, counter)
        elif pilihan == "2":
            panggil_pasien(queues, stacks, selesai)
        elif pilihan == "3":
            undo_tindakan(stacks)
        elif pilihan == "4":
            tambah_rekam_medis(bst)
        elif pilihan == "5":
            cari_rekam_medis(bst)
        elif pilihan == "6":
            lihat_rekam_medis(bst)
        elif pilihan == "7":
            laporan_hari(selesai)
        elif pilihan == "8":
            print("👋 Sistem ditutup")
            break
        else:
            print("❌ Pilihan tidak valid")