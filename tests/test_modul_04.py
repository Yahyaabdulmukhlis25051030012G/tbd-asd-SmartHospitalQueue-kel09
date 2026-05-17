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

from dataclasses import dataclass
import random

# Pastikan class LLNode, LinkedListPasien, insertion_sort, 
# dan selection_sort milikmu ada di atas kode ini

# 1. Definisi Data Pasien untuk Testing
@dataclass
class Pasien:
    no_antrian: int
    nama: str
    waktu_tunggu: float

def test_sorting_terminal():
    print("="*50)
    print("🏥 PENGUJIAN ALGORITMA SORTING DATA PASIEN")
    print("="*50)

    # 2. Buat data dummy yang acak
    daftar_pasien = LinkedListPasien()
    
    # Sengaja kita masukkan secara acak (no_antrian dan waktu_tunggu tidak berurutan)
    data_dummy = [
        Pasien(no_antrian=3, nama="Budi", waktu_tunggu=15.5),
        Pasien(no_antrian=1, nama="Siti", waktu_tunggu=45.0),
        Pasien(no_antrian=4, nama="Andi", waktu_tunggu=5.2),
        Pasien(no_antrian=2, nama="Dewi", waktu_tunggu=30.0),
        Pasien(no_antrian=5, nama="Eko", waktu_tunggu=25.5)
    ]
    
    for p in data_dummy:
        daftar_pasien.append(p)

    # 3. Tampilkan Data Awal
    print("\n[📁] DATA AWAL (BELUM TERURUT):")
    for p in daftar_pasien.to_list():
        print(f" -> No. {p.no_antrian} | {p.nama:<5} | Menunggu: {p.waktu_tunggu} menit")

    # 4. Uji Insertion Sort (Descending berdasarkan Waktu Tunggu)
    # Biasanya dipakai untuk mencari siapa yang nunggunya paling lama untuk kompensasi/evaluasi
    print("\n[⏳] INSERTION SORT (Berdasarkan Waktu Tunggu - DESCENDING):")
    print("     (Ekspektasi: Siti -> Dewi -> Eko -> Budi -> Andi)")
    
    ll_sorted_waktu = insertion_sort_waktu_tunggu(daftar_pasien)
    
    for p in ll_sorted_waktu.to_list():
        print(f" -> No. {p.no_antrian} | {p.nama:<5} | Menunggu: {p.waktu_tunggu} menit")

    # 5. Uji Selection Sort (Ascending berdasarkan No Antrian)
    # Biasanya dipakai untuk merapikan kembali arsip berdasarkan nomor urut kedatangan
    print("\n[🔢] SELECTION SORT (Berdasarkan No Antrian - ASCENDING):")
    print("     (Ekspektasi: Siti -> Dewi -> Budi -> Andi -> Eko)")
    
    # Kita sorting dari data yang tadi sudah diubah urutannya
    ll_sorted_nomor = selection_sort_no_antrian(ll_sorted_waktu)
    
    for p in ll_sorted_nomor.to_list():
        print(f" -> No. {p.no_antrian} | {p.nama:<5} | Menunggu: {p.waktu_tunggu} menit")

    print("\n✅ PENGUJIAN SELESAI!")
    print("="*50)

if __name__ == "__main__":
    test_sorting_terminal()