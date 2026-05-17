import time
import numpy as np
from typing import List
from dataclasses import dataclass

# =================================================================
# DEFINISI STRUKTUR DATA OBJEK
# =================================================================
@dataclass
class Pasien:
    no_antrian: int
    nama: str
    poli: str
    prioritas: int          # 1=KRITIS, 2=PRIORITAS, 3=REGULER
    waktu_daftar: float
    waktu_tunggu: float = 0.0

@dataclass
class RekamMedis:
    no_rm: int
    nama: str
    riwayat_penyakit: list

# =================================================================
# IMPORTS DARI REPOSITORI BRANCH DEV
# =================================================================
from src.data_structures.queue import PriorityQueue
from src.data_structures.stack import Stack
from src.data_structures.bst import BSTRekamMedis

# FIX 1: Import nama fungsi asli & kelas Linked List dari modul_4_sorting
from src.modules.modul_4_sorting import insertion_sort_waktu_tunggu, LinkedListPasien

# =================================================================
# KONSTANTA & PARAMETER SISTEM
# =================================================================
POLI = ["Umum", "Jantung", "Ortopedi", "Anak", "Gigi"]
PRIORITAS_MAP = {1: "KRITIS", 2: "PRIORITAS", 3: "REGULER"}

def tampilkan_menu_utama():
    print("\n" + "="*55)
    print("🏥  SMART HOSPITAL QUEUE SYSTEM (CLI INTERAKTIF)  🏥")
    print("="*55)
    print("[1] Daftarkan Pasien Baru (Enqueue)")
    print("[2] Panggil Pasien Berikutnya (Dequeue)")
    print("[3] Batalkan Catatan/Tindakan Terakhir Dokter (Undo)")
    print("[4] Tambah Data Rekam Medis Baru (BST Insert)")
    print("[5] Cari Rekam Medis Pasien (BST Search)")
    print("[6] Tampilkan Semua Rekam Medis Terdaftar (BST Inorder)")
    print("[7] Cetak Laporan Evaluasi Waktu Tunggu Pasien (Sorting)")
    print("[8] Keluar")
    print("-" * 55)

def main():
    # Inisialisasi struktur data per-poliklinik
    queues = {poli: PriorityQueue() for poli in POLI}
    stacks = {poli: Stack() for poli in POLI}
    bst_rm = BSTRekamMedis()
    
    # List python biasa untuk menampung pasien sementara setelah selesai diperiksa
    pasien_selesai_list = [] 
    counter_antrian = 1
    
    print("Sistem Berhasil Diinisialisasi dengan 5 Poliklinik.")

    while True:
        tampilkan_menu_utama()
        pilihan = input("Pilih Menu (1-8): ").strip()

        # =========================================================
        # MENU 1: ENQUEUE PASIEN BARU
        # =========================================================
        if pilihan == "1":
            print("\n--- REGISTRASI PASIEN BARU ---")
            nama = input("Masukkan Nama Pasien: ").strip()
            
            print("\nPilih Poliklinik Tujuan:")
            for idx, p in enumerate(POLI, 1):
                print(f"[{idx}] Poli {p}")
            try:
                pilihan_poli = int(input("Pilih Poli (1-5): "))
                if pilihan_poli < 1 or pilihan_poli > 5:
                    print("❌ Pilihan poliklinik tidak valid!")
                    continue
                poli_target = POLI[pilihan_poli - 1]
            except ValueError:
                print("❌ Input harus berupa angka!")
                continue

            print("\nTingkat Urgensi Medis (Triase):")
            print("[1] KRITIS (Serangan jantung, sesak berat, pendarahan)")
            print("[2] PRIORITAS (Lansia, ibu hamil, difabel)")
            print("[3] REGULER (Keluhan umum, kontrol rutin)")
            try:
                prioritas = int(input("Pilih Tingkat Prioritas (1-3): "))
                if prioritas not in [1, 2, 3]:
                    print("❌ Prioritas salah! Otomatis diset ke REGULER (3).")
                    prioritas = 3
            except ValueError:
                print("❌ Input harus berupa angka! Otomatis diset ke REGULER (3).")
                prioritas = 3

            pasien_baru = Pasien(
                no_antrian=counter_antrian,
                nama=nama,
                poli=poli_target,
                prioritas=prioritas,
                waktu_daftar=time.time()
            )
            queues[poli_target].enqueue(pasien_baru)
            print(f"\n💾 [SUKSES] {nama} masuk antrean Poli {poli_target} | No. Antrean: {counter_antrian}")
            counter_antrian += 1

        # =========================================================
        # MENU 2: DEQUEUE PASIEN (PANGGIL PASIEN)
        # =========================================================
        elif pilihan == "2":
            print("\n--- PANGGIL PASIEN KE RUANGAN DOKTER ---")
            print("Pilih Poliklinik:")
            for idx, p in enumerate(POLI, 1):
                print(f"[{idx}] Poli {p} (Sisa Antrean: {len(queues[p])})")
            
            try:
                pilihan_poli = int(input("Pilih Poli (1-5): "))
                poli_target = POLI[pilihan_poli - 1]
            except (ValueError, IndexError):
                print("❌ Pilihan poliklinik tidak valid!")
                continue

            pasien_dipanggil = queues[poli_target].dequeue()
            
            if pasien_dipanggil:
                waktu_sekarang = time.time()
                pasien_dipanggil.waktu_tunggu = waktu_sekarang - pasien_dipanggil.waktu_daftar
                
                print(f"\n📢 [PANGGILAN] No. Antrean {pasien_dipanggil.no_antrian}: {pasien_dipanggil.nama}")
                print(f"    Silakan menuju ke Ruang Poli {pasien_dipanggil.poli} ({PRIORITAS_MAP[pasien_dipanggil.prioritas]})")
                print(f"    Waktu tunggu: {pasien_dipanggil.waktu_tunggu:.2f} detik")

                log_tindakan = f"Memeriksa Pasien No.{pasien_dipanggil.no_antrian} ({pasien_dipanggil.nama})"
                stacks[poli_target].push(log_tindakan)
                
                # Simpan ke list selesai
                pasien_selesai_list.append(pasien_dipanggil)
            else:
                print(f"ℹ️ Antrean Poli {poli_target} kosong.")

        # =========================================================
        # MENU 3: UNDO LOG TINDAKAN DOKTER (STACK POP)
        # =========================================================
        elif pilihan == "3":
            print("\n--- FITUR UNDO CATATAN MEDIS DOKTER ---")
            print("Pilih Poliklinik Dokter:")
            for idx, p in enumerate(POLI, 1):
                print(f"[{idx}] Poli {p}")
            
            try:
                pilihan_poli = int(input("Pilih Poli (1-5): "))
                poli_target = POLI[pilihan_poli - 1]
            except (ValueError, IndexError):
                print("❌ Pilihan salah!")
                continue

            log_dibatalkan = stacks[poli_target].pop()
            if log_dibatalkan:
                print(f"\n↩️ [UNDO BERHASIL] Berhasil membatalkan: '{log_dibatalkan}'")
            else:
                print("⚠️ Tidak ada catatan tindakan dokter yang bisa dibatalkan.")

        # =========================================================
        # MENU 4: TAMBAH DATA REKAM MEDIS (BST INSERT)
        # =========================================================
        elif pilihan == "4":
            print("\n--- ARSIP REKAM MEDIS BARU (BST INSERT) ---")
            try:
                no_rm = int(input("Masukkan Nomor Rekam Medis (Angka Unik): "))
                nama = input("Masukkan Nama Lengkap Pasien: ").strip()
                penyakit = input("Diagnosis Penyakit (pisahkan dengan koma): ").split(",")
                
                riwayat_list = [p.strip() for p in penyakit]
                data_rm = RekamMedis(no_rm, nama, riwayat_list)
                
                bst_rm.insert(data_rm)
                print(f"💾 [SUKSES] Data rekam medis No. {no_rm} disimpan ke database BST.")
            except ValueError:
                print("❌ Nomor Rekam Medis harus berupa angka!")

        # =========================================================
        # MENU 5: CARI REKAM MEDIS PASIEN (BST SEARCH)
        # =========================================================
        elif pilihan == "5":
            print("\n--- PENCARIAN REKAM MEDIS PASIEN (BST SEARCH) ---")
            try:
                cari_no = int(input("Masukkan Nomor Rekam Medis yang dicari: "))
                start_time = time.time()
                hasil = bst_rm.search(cari_no)
                end_time = time.time()
                
                if hasil:
                    print(f"\n🔍 [DITEMUKAN] Data Pasien RM #{cari_no}")
                    print(f"    Nama Pasien : {hasil.nama}")
                    print(f"    Riwayat Medis: {', '.join(hasil.riwayat_penyakit)}")
                    print(f"    Waktu Pencarian BST: {(end_time - start_time) * 1000:.4f} ms")
                else:
                    print(f"❌ Data Rekam Medis #{cari_no} tidak ditemukan.")
            except ValueError:
                print("❌ Input No. RM harus berupa angka!")

        # =========================================================
        # MENU 6: LIHAT SEMUA REKAM MEDIS (BST INORDER TRAVERSAL)
        # =========================================================
        elif pilihan == "6":
            print("\n--- DAFTAR ARSIP REKAM MEDIS SEBAGAI TREE (INORDER) ---")
            all_rm = bst_rm.inorder()
            
            if all_rm:
                print(f"{'No RM':<10} | {'Nama Pasien':<20} | {'Riwayat Penyakit'}")
                print("-" * 55)
                for rm in all_rm:
                    print(f"{rm.no_rm:<10} | {rm.nama:<20} | {', '.join(rm.riwayat_penyakit)}")
            else:
                print("ℹ️ Database rekam medis kosong.")

        # =========================================================
        # MENU 7: LAPORAN EVALUASI PASIEN SELESAI (SORTING MODULE)
        # =========================================================
        elif pilihan == "7":
            print("\n--- LAPORAN EVALUASI HARIAN (SORTING WAKTU TUNGGU) ---")
            if not pasien_selesai_list:
                print("⚠️ Belum ada pasien yang selesai dilayani hari ini.")
                continue
            
            # FIX 2: Konversi python list biasa ke LinkedListPasien (Struktur data buatanmu)
            ll_pasien = LinkedListPasien()
            for p in pasien_selesai_list:
                ll_pasien.append(p)
            
            # Jalankan sorting menggunakan fungsi asli dari modul kelompokmu
            ll_terurut = insertion_sort_waktu_tunggu(ll_pasien)
            
            # Konversi kembali ke list Python agar mudah diloop menggunakan .to_list()
            laporan_terurut = ll_terurut.to_list()
            
            print("\n📋 Urutan Pasien Menunggu Paling Lama (Descending):")
            print(f"{'No Antrean':<12} | {'Nama Pasien':<18} | {'Poliklinik':<12} | {'Waktu Tunggu'}")
            print("-" * 65)
            for p in laporan_terurut:
                print(f"{p.no_antrian:<12} | {p.nama:<18} | {p.poli:<12} | {p.waktu_tunggu:.2f} detik")

        # =========================================================
        # MENU 8: KELUAR
        # =========================================================
        elif pilihan == "8":
            print("\n👋 Mematikan sistem Smart Hospital Queue. Terima kasih!")
            break
            
        else:
            print("❌ Opsi salah! Silakan masukkan angka dari 1 sampai 8.")

if __name__ == "__main__":
    main()