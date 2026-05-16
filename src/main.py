import time
import numpy as np
import random

from src.data_structures.queue import PriorityQueue
from src.data_structures.stack import Stack
from src.data_structures.bst import BST
from src.modules.sorting import LinkedListPasien, insertion_sort_waktu_tunggu, selection_sort_no_antrian

np.random.seed(42)
random.seed(42)

POLI = ['Umum', 'Jantung', 'Ortopedi', 'Anak', 'Gigi']
PRIORITAS = {'KRITIS': 1, 'PRIORITAS': 2, 'REGULER': 3}

from dataclasses import dataclass
from typing import List

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
        print("7. LAPORAN HARI")
        print("8. KELUAR")

        pilihan = input("\nPilih menu (1-8): ")

        # =========================
        # DAFTAR
        # =========================
        if pilihan == "1":
            print("\n--- DAFTAR PASIEN ---")
            nama = input("Nama pasien: ")
            poli = input(f"Poli {POLI}: ")
            prior = input("Prioritas (KRITIS/PRIORITAS/REGULER): ").upper()

            if poli not in POLI:
                print("❌ Poli tidak valid")
                continue
            if prior not in PRIORITAS:
                print("❌ Prioritas tidak valid")
                continue

            p = Pasien(counter, nama, poli, PRIORITAS[prior], time.time())
            queues[poli].enqueue(p)
            counter += 1
            print(f"✅ Pasien didaftarkan | Big-O enqueue: O(n)")

        # =========================
        # PANGGIL
        # =========================
        elif pilihan == "2":
            print("\n--- PANGGIL PASIEN ---")
            poli = input(f"Poli {POLI}: ")

            if poli not in POLI:
                print("❌ Poli tidak valid")
                continue

            p = queues[poli].dequeue()
            if p:
                p.waktu_tunggu = time.time() - p.waktu_daftar
                selesai.append(p)
                stacks[poli].push(f"Periksa {p.nama}")
                print(f"📢 Dipanggil: {p.nama} | Big-O dequeue: O(1)")
            else:
                print("⚠️ Antrian kosong")

        # =========================
        # UNDO
        # =========================
        elif pilihan == "3":
            print("\n--- UNDO ---")
            poli = input("Poli: ")

            if poli not in POLI:
                print("❌ Poli tidak valid")
                continue

            hasil = stacks[poli].pop()
            if hasil:
                print(f"↩️ Undo: {hasil} | Big-O pop: O(1)")
            else:
                print("⚠️ Tidak ada tindakan untuk di-undo")

        # =========================
        # TAMBAH RM
        # =========================
        elif pilihan == "4":
            print("\n--- TAMBAH REKAM MEDIS ---")
            no_rm = int(input("No RM: "))
            nama = input("Nama: ")
            bst.insert(RekamMedis(no_rm, nama, []))
            print(f"💾 Rekam medis disimpan | Big-O insert BST: O(log n)")

        # =========================
        # CARI RM
        # =========================
        elif pilihan == "5":
            print("\n--- CARI REKAM MEDIS ---")
            no_rm = int(input("No RM: "))
            res = bst.search(no_rm)
            if res:
                print(f"🔍 Ditemukan: {res.nama} | Big-O search BST: O(log n)")
            else:
                print("❌ Tidak ditemukan")

        # =========================
        # LIHAT RM
        # =========================
        elif pilihan == "6":
            print("\n--- DATA REKAM MEDIS ---")
            data = bst.inorder()
            if not data:
                print("⚠️ Kosong")
            else:
                for d in data:
                    print(f"No RM: {d.no_rm} | Nama: {d.nama}")
            print("Big-O inorder: O(n)")

        # =========================
        # LAPORAN HARI
        # =========================
        elif pilihan == "7":
            print("\n--- LAPORAN HARI ---")

            if not selesai:
                print("⚠️ Belum ada pasien selesai hari ini")
                continue

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

        # =========================
        # KELUAR
        # =========================
        elif pilihan == "8":
            print("👋 Sistem ditutup")
            break

        else:
            print("❌ Pilihan tidak valid")

if __name__ == "__main__":
    main()