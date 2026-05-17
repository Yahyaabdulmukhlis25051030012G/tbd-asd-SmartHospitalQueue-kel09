# 🏥 Smart Hospital Queue & Record System
**TBP Kelompok 09 - Algoritma dan Struktur Data (ELT60213)**
**Program Studi S1 Teknik Elektro — Universitas Negeri Yogyakarta**

Sistem manajemen terintegrasi untuk efisiensi layanan rumah sakit, mencakup antrian prioritas pasien, pencatatan rekam medis berbasis pohon biner, dan log tindakan dokter dengan fitur pembatalan (*undo*).

## 👥 Anggota Kelompok & Pembagian Tugas
Sesuai dengan ketentuan proyek, setiap anggota bertanggung jawab atas modul spesifik yang diimplementasikan **"dari nol" tanpa library struktur data bawaan**:

| Nama | NIM | Modul Utama |
| --- | --- | --- |
| **Yahya Abdul Mukhlis** | 25051030012 | **BST** (Rekam Medis) + **Integrasi CLI** |
| **Sheiraya Senja Shofa** | 25051030006 | **Stack** (Undo Log) + **Sorting** (Laporan Harian) |
| **Rifqi Nadil Ulum A.** | 25051030031 | **Priority Queue** (Antrian Poli) + **Eksperimen** |

## 🚀 Fitur Utama Sistem
1. **Priority Queue (Multi-Poli)**: Mengelola antrian di 5 poli (Umum, Jantung, Ortopedi, Anak, Gigi) dengan prioritas KRITIS (1), PRIORITAS (2), dan REGULER (3).
2. **Stack Tindakan**: Menyimpan riwayat tindakan medis dokter per sesi dan mendukung operasi `pop()` untuk fitur *undo*.
3. **Binary Search Tree (BST)**: Penyimpanan rekam medis menggunakan nomor RM sebagai kunci untuk pencarian cepat $O(\log n)$.
4. **Modul Sorting**: Mengurutkan laporan harian pasien berdasarkan waktu tunggu (*descending*) menggunakan algoritma **Insertion Sort**.

## 🗂️ Struktur Folder
Proyek ini mengikuti struktur modular untuk mempermudah kolaborasi:
```text
├── AI_Log/             # Bukti penggunaan AI (Wajib)
├── docs/               # Laporan PDF dan Slide Presentasi
├── experiments/        # Skrip benchmark performa Big-O
├── src/
│   ├── data_structures/# Implementasi murni (Node, Stack, Queue, BST)
│   ├── modules/        # Logika bisnis (CLI, Sorting)
│   └── main.py         # Entry point aplikasi
├── tests/              # Unit testing dengan Pytest
└── requirements.txt    # Dependensi pustaka luar
```

## 🛠️ Instalasi
Pastikan Anda menggunakan **Python 3.11** atau versi terbaru. Karena perintah `pip` mungkin memerlukan awalan khusus di beberapa konfigurasi VS Code, gunakan perintah berikut:

1. **Clone Repositori**
   ```bash
   git clone https://github.com/Yahyaabdulmukhlis25051030012G/tbd-asd-SmartHospitalQueue-kel09.git
   cd tbd-asd-SmartHospitalQueue-kel09
   ```

2. **Instal Dependensi** (Numpy, Matplotlib, Pytest)
   ```bash
   py -m pip install -r requirements.txt
   ```
   *(Atau gunakan `python -m pip install...` jika perintah di atas tidak dikenali)*.

## 💻 Cara Menjalankan
Jalankan sistem utama melalui terminal VS Code dengan perintah:
```bash
python src/main.py
```

## 🧪 Pengujian (Unit Test)
Untuk memastikan setiap struktur data (Stack, Queue, BST) berjalan benar, jalankan pengujian otomatis menggunakan **pytest**:
```bash
pytest tests/
```

## 📊 Analisis Kompleksitas
Setiap perintah dalam sistem CLI ini akan menampilkan analisis Big-O secara real-time untuk memberikan transparansi mengenai efisiensi algoritma yang digunakan (misal: pendaftaran pasien dalam O(n) atau pencarian rekam medis dalam O(logn)).