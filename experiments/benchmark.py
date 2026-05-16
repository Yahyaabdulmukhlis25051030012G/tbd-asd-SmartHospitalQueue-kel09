# =====================================================
# BENCHMARK / EKSPERIMEN RUNTIME
# Mengukur waktu operasi untuk N = 50, 200, 500
# Sesuai panduan: seed = 42, wajib 3 ukuran dataset
# =====================================================

import time
import random
import numpy as np

# Setup seed wajib
np.random.seed(42)
random.seed(42)

# Import dari modul yang sudah dibuat
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_structures.queue import PriorityQueue
from src.data_structures.bst import BST
from src.data_structures.stack import Stack
from src.modules.modul_0_ll import Pasien, RekamMedis, POLI, PRIORITAS
from src.modules.sorting import LinkedListPasien, insertion_sort_waktu_tunggu, selection_sort_no_antrian


# =====================================================
# HELPER — Generate data dummy
# =====================================================
def generate_pasien(n):
    """Generate n pasien acak dengan seed tetap"""
    random.seed(42)
    pasien_list = []
    nama_list = [f"Pasien_{i}" for i in range(1, n + 1)]
    prioritas_list = list(PRIORITAS.values())

    for i in range(n):
        p = Pasien(
            no_antrian=i + 1,
            nama=nama_list[i],
            poli=random.choice(POLI),
            prioritas=random.choice(prioritas_list),
            waktu_daftar=time.time(),
            waktu_tunggu=random.uniform(0.5, 120.0)
        )
        pasien_list.append(p)
    return pasien_list


def generate_rekam_medis(n):
    """Generate n rekam medis acak"""
    random.seed(42)
    rm_list = []
    no_rm_pool = random.sample(range(1000, 9999), n)
    for i in range(n):
        rm_list.append(RekamMedis(
            no_rm=no_rm_pool[i],
            nama=f"Pasien_RM_{i}",
            riwayat=[]
        ))
    return rm_list


# =====================================================
# FUNGSI UKUR WAKTU
# =====================================================
def ukur_waktu(fungsi, *args):
    """Jalankan fungsi dan kembalikan waktu eksekusi dalam milidetik"""
    start = time.perf_counter()
    hasil = fungsi(*args)
    end = time.perf_counter()
    return (end - start) * 1000, hasil  # ms


# =====================================================
# BENCHMARK 1 — Priority Queue enqueue & dequeue
# =====================================================
def benchmark_priority_queue(n):
    pasien_list = generate_pasien(n)
    pq = PriorityQueue()

    # Enqueue semua pasien
    start = time.perf_counter()
    for p in pasien_list:
        pq.enqueue(p)
    waktu_enqueue = (time.perf_counter() - start) * 1000

    # Dequeue semua pasien
    start = time.perf_counter()
    while not pq.is_empty():
        pq.dequeue()
    waktu_dequeue = (time.perf_counter() - start) * 1000

    return waktu_enqueue, waktu_dequeue


# =====================================================
# BENCHMARK 2 — BST insert & search
# =====================================================
def benchmark_bst(n):
    rm_list = generate_rekam_medis(n)
    bst = BST()

    # Insert semua rekam medis
    start = time.perf_counter()
    for rm in rm_list:
        bst.insert(rm)
    waktu_insert = (time.perf_counter() - start) * 1000

    # Search 10 no_rm acak
    random.seed(42)
    sample = random.sample([rm.no_rm for rm in rm_list], min(10, n))
    start = time.perf_counter()
    for no_rm in sample:
        bst.search(no_rm)
    waktu_search = (time.perf_counter() - start) * 1000

    return waktu_insert, waktu_search


# =====================================================
# BENCHMARK 3 — Sorting (Insertion Sort & Selection Sort)
# =====================================================
def benchmark_sorting(n):
    pasien_list = generate_pasien(n)

    # Buat linked list pasien
    ll1 = LinkedListPasien()
    ll2 = LinkedListPasien()
    for p in pasien_list:
        ll1.append(p)
        ll2.append(p)

    # Insertion Sort
    start = time.perf_counter()
    insertion_sort_waktu_tunggu(ll1)
    waktu_insertion = (time.perf_counter() - start) * 1000

    # Selection Sort
    start = time.perf_counter()
    selection_sort_no_antrian(ll2)
    waktu_selection = (time.perf_counter() - start) * 1000

    return waktu_insertion, waktu_selection


# =====================================================
# BENCHMARK 4 — Stack push & pop
# =====================================================
def benchmark_stack(n):
    stack = Stack()
    tindakan_list = [f"Tindakan_{i}" for i in range(n)]

    # Push semua tindakan
    start = time.perf_counter()
    for t in tindakan_list:
        stack.push(t)
    waktu_push = (time.perf_counter() - start) * 1000

    # Pop semua tindakan
    start = time.perf_counter()
    while not stack.is_empty():
        stack.pop()
    waktu_pop = (time.perf_counter() - start) * 1000

    return waktu_push, waktu_pop


# =====================================================
# CETAK TABEL HASIL
# =====================================================
def cetak_tabel(judul, header, rows):
    print(f"\n{'='*65}")
    print(f"  {judul}")
    print(f"{'='*65}")
    print(f"  {header[0]:<8} {header[1]:<20} {header[2]:<20} {'Big-O'}")
    print(f"  {'-'*60}")
    for row in rows:
        print(f"  {row[0]:<8} {row[1]:<20} {row[2]:<20} {row[3]}")
    print(f"{'='*65}")


# =====================================================
# MAIN BENCHMARK
# =====================================================
def main():
    ukuran = [50, 200, 500]

    print("\n" + "="*65)
    print("   EKSPERIMEN RUNTIME — Smart Hospital Queue & Record System")
    print("   seed = 42 | satuan waktu = milidetik (ms)")
    print("="*65)

    # ── Tabel 1: Priority Queue ──────────────────────────────────
    rows_pq = []
    for n in ukuran:
        enq, deq = benchmark_priority_queue(n)
        rows_pq.append((
            f"N={n}",
            f"{enq:.4f} ms",
            f"{deq:.4f} ms",
            "enq O(n) / deq O(1)"
        ))
    cetak_tabel(
        "TABEL 1 — Priority Queue (enqueue & dequeue)",
        ["N", "Enqueue (ms)", "Dequeue (ms)", "Big-O"],
        rows_pq
    )

    # ── Tabel 2: BST ─────────────────────────────────────────────
    rows_bst = []
    for n in ukuran:
        ins, srch = benchmark_bst(n)
        rows_bst.append((
            f"N={n}",
            f"{ins:.4f} ms",
            f"{srch:.4f} ms",
            "O(log n) avg"
        ))
    cetak_tabel(
        "TABEL 2 — BST Rekam Medis (insert & search)",
        ["N", "Insert (ms)", "Search 10x (ms)", "Big-O"],
        rows_bst
    )

    # ── Tabel 3: Sorting ─────────────────────────────────────────
    rows_sort = []
    for n in ukuran:
        ins_sort, sel_sort = benchmark_sorting(n)
        rows_sort.append((
            f"N={n}",
            f"{ins_sort:.4f} ms",
            f"{sel_sort:.4f} ms",
            "O(n²)"
        ))
    cetak_tabel(
        "TABEL 3 — Sorting Laporan (Insertion Sort & Selection Sort)",
        ["N", "Insertion Sort (ms)", "Selection Sort (ms)", "Big-O"],
        rows_sort
    )

    # ── Tabel 4: Stack ───────────────────────────────────────────
    rows_stack = []
    for n in ukuran:
        push, pop = benchmark_stack(n)
        rows_stack.append((
            f"N={n}",
            f"{push:.4f} ms",
            f"{pop:.4f} ms",
            "O(1)"
        ))
    cetak_tabel(
        "TABEL 4 — Stack Riwayat Tindakan (push & pop)",
        ["N", "Push (ms)", "Pop (ms)", "Big-O"],
        rows_stack
    )

    print("\n✅ Eksperimen selesai! Salin tabel di atas ke laporan PDF.\n")


if __name__ == "__main__":
    main()