import time
import random
import matplotlib.pyplot as plt
from dataclasses import dataclass

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.queue import PriorityQueue
from data_structures.stack import Stack
from data_structures.bst import BSTRekamMedis

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
    riwayat_penyakit: list

POLI = ["Umum", "Jantung", "Ortopedi", "Anak", "Gigi"]

def generate_dummy_data(N: int):
    """Fungsi pembantu untuk membuat data pasien dan rekam medis tiruan."""
    pasien_list = []
    rm_list = []
    for i in range(1, N + 1):
        # Buat Pasien
        p = Pasien(
            no_antrian=i,
            nama=f"Pasien_{i}",
            poli=random.choice(POLI),
            prioritas=random.choices([1, 2, 3], weights=[10, 30, 60], k=1)[0], # 10% Kritis, 30% Prioritas, 60% Reguler
            waktu_daftar=time.time()
        )
        pasien_list.append(p)
        
        # Buat Rekam Medis
        rm = RekamMedis(
            no_rm=1000 + i,
            nama=f"Pasien_{i}",
            riwayat_penyakit=[random.choice(["Demam", "Batuk", "Hipertensi", "Diabetes", "Sakit Gigi"])]
        )
        rm_list.append(rm)
        
    return pasien_list, rm_list

def run_benchmark():
    print("="*60)
    print("🚀 PENGUJIAN RUNTIME ALGORITMA & STRUKTUR DATA")
    print("="*60)
    
    ukuran_N = [50, 200, 500]
    hasil_runtime = {"N": [], "Enqueue": [], "Dequeue": [], "InsertBST": [], "SearchBST": []}

    print(f"{'N':<5} | {'Enqueue (O(n))':<15} | {'Dequeue (O(1))':<15} | {'Insert BST (O(log n))':<20} | {'Search BST (O(log n))'}")
    print("-" * 85)

    for N in ukuran_N:
        random.seed(42) # Set seed agar data konsisten per ukuran
        pasien_list, rm_list = generate_dummy_data(N)
        
        # 1. Setup Struktur Data
        queue = PriorityQueue()
        bst = BSTRekamMedis()
        
        # 2. Uji Enqueue (Total waktu memasukkan N pasien)
        start = time.perf_counter()
        for p in pasien_list:
            queue.enqueue(p)
        waktu_enqueue = time.perf_counter() - start
        
        # 3. Uji Dequeue (Total waktu mengeluarkan N pasien)
        start = time.perf_counter()
        while not queue.is_empty():
            queue.dequeue()
        waktu_dequeue = time.perf_counter() - start
        
        # 4. Uji Insert BST (Total waktu memasukkan N RM)
        start = time.perf_counter()
        for rm in rm_list:
            bst.insert(rm)
        waktu_insert_bst = time.perf_counter() - start
        
        # 5. Uji Search BST (Mencari N data acak)
        search_targets = [random.randint(1001, 1000 + N) for _ in range(N)]
        start = time.perf_counter()
        for target in search_targets:
            bst.search(target)
        waktu_search_bst = time.perf_counter() - start

        # Simpan Hasil
        hasil_runtime["N"].append(N)
        hasil_runtime["Enqueue"].append(waktu_enqueue)
        hasil_runtime["Dequeue"].append(waktu_dequeue)
        hasil_runtime["InsertBST"].append(waktu_insert_bst)
        hasil_runtime["SearchBST"].append(waktu_search_bst)

        print(f"{N:<5} | {waktu_enqueue:.6f} detik  | {waktu_dequeue:.6f} detik  | {waktu_insert_bst:.6f} detik       | {waktu_search_bst:.6f} detik")

    # === TAMPILKAN GRAFIK TREN RUNTIME ===
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(hasil_runtime["N"], hasil_runtime["Enqueue"], marker='o', label='Enqueue PQ (O(n))')
        plt.plot(hasil_runtime["N"], hasil_runtime["Dequeue"], marker='s', label='Dequeue PQ (O(1))')
        plt.plot(hasil_runtime["N"], hasil_runtime["InsertBST"], marker='^', label='Insert BST (O(log n))')
        plt.plot(hasil_runtime["N"], hasil_runtime["SearchBST"], marker='x', label='Search BST (O(log n))')
        
        plt.title("Perbandingan Runtime Berdasarkan Jumlah N Pasien (Skala Hospital Queue)")
        plt.xlabel("Jumlah N")
        plt.ylabel("Waktu (Detik)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig("hasil_benchmark.png") # Simpan ke gambar untuk dimasukkan ke laporan
        print("\n📊 Grafik tren telah disimpan sebagai 'hasil_benchmark.png'.")
        # plt.show() # Uncomment ini jika ingin grafiknya langsung pop-up di layar
    except ImportError:
        print("\n⚠️ Library matplotlib tidak terinstall. Lewati pembuatan grafik tren.")

def run_500_random_events():
    """Simulasi operasional rumah sakit dengan 500 event acak."""
    print("\n" + "="*60)
    print("🎲 SIMULASI 500 EVENT ACAK (SEED=42) & VALIDASI STRUKTUR")
    print("="*60)
    
    random.seed(42) # Wajib sesuai spesifikasi
    
    queues = {poli: PriorityQueue() for poli in POLI}
    stacks = {poli: Stack() for poli in POLI}
    bst_rm = BSTRekamMedis()
    
    counter_pasien = 1
    counter_rm = 1000
    
    event_counts = {"DAFTAR": 0, "PANGGIL": 0, "INSERT_RM": 0, "SEARCH_RM": 0}

    # Jalankan 500 Iterasi Event Acak
    for _ in range(500):
        # Tentukan jenis event dengan probabilitas tertentu
        # 40% Daftar, 30% Panggil, 20% Insert RM, 10% Cari RM
        jenis_event = random.choices(["DAFTAR", "PANGGIL", "INSERT_RM", "SEARCH_RM"], weights=[40, 30, 20, 10], k=1)[0]
        event_counts[jenis_event] += 1
        
        poli_acak = random.choice(POLI)
        
        if jenis_event == "DAFTAR":
            p = Pasien(counter_pasien, f"Pasien_{counter_pasien}", poli_acak, random.randint(1, 3), time.time())
            queues[poli_acak].enqueue(p)
            counter_pasien += 1
            
        elif jenis_event == "PANGGIL":
            dipanggil = queues[poli_acak].dequeue()
            if dipanggil:
                stacks[poli_acak].push(f"Memeriksa {dipanggil.nama}")
                
        elif jenis_event == "INSERT_RM":
            rm = RekamMedis(counter_rm, f"Pasien_RM_{counter_rm}", ["Keluhan Umum"])
            bst_rm.insert(rm)
            counter_rm += 1
            
        elif jenis_event == "SEARCH_RM":
            if counter_rm > 1000:
                bst_rm.search(random.randint(1000, counter_rm - 1))

    # =========================================================
    # VALIDASI & KONFIRMASI (Sesuai Buku Panduan)
    # =========================================================
    print(f"✅ Total Event Dieksekusi: 500 (Daftar: {event_counts['DAFTAR']}, Panggil: {event_counts['PANGGIL']}, Insert: {event_counts['INSERT_RM']}, Search: {event_counts['SEARCH_RM']})")
    
    print("\n[1] VALIDASI STRUKTUR PRIORITY QUEUE PER POLI (Sisa Antrean)")
    for poli in POLI:
        print(f"    - Poli {poli:<10}: {len(queues[poli])} pasien menunggu.")
        
    print("\n[2] VALIDASI STRUKTUR STACK PER DOKTER (Total Log Riwayat)")
    for poli in POLI:
        print(f"    - Dokter {poli:<8}: {stacks[poli]._size if hasattr(stacks[poli], '_size') else 'Tercatat'} pasien telah diperiksa.")
        
    print("\n[3] VALIDASI ISI BST (Rekam Medis)")
    all_data_bst = bst_rm.inorder()
    print(f"    - Total Data RM yang masuk ke Tree: {len(all_data_bst)} dokumen.")
    if all_data_bst:
        print(f"    - RM terkecil di root kiri: {all_data_bst[0].no_rm}")
        print(f"    - RM terbesar di root kanan: {all_data_bst[-1].no_rm}")

if __name__ == "__main__":
    run_benchmark()
    run_500_random_events()