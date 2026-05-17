from typing import Optional, List

class LLNode:
    """Ringan (Lightweight) Node untuk menghemat memori [13]."""
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None

class Stack:
    """
    Implementasi Stack (LIFO) berbasis Singly Linked List untuk log tindakan.
    
    Analisis Big-O:
    - Waktu: push/pop O(1) karena hanya manipulasi pointer di head [9, 14].
    - Ruang: O(k) di mana k adalah jumlah tindakan yang dicatat [3].
    
    Analisis Lanjutan (Wajib Laporan No. 3):
    Kelemahan Linked List adalah penggunaan memori yang bersifat 'unbounded'. 
    Jika ada 20 dokter dengan 50 tindakan/sesi, total ada 1.000 node di memori [3].
    Sebagai alternatif, Circular Buffer (array-based) lebih efisien memori karena 
    memiliki kapasitas tetap, namun Stack Linked List lebih fleksibel [5, 6].
    """
    def __init__(self):
        self.top: Optional[LLNode] = None
        self._size: int = 0

    def push(self, tindakan: str) -> None:
        """O(1) - Menambah catatan medis dengan validasi [9, 15]."""
        if not isinstance(tindakan, str):
            raise ValueError("Log tindakan harus berupa teks deskripsi.")
            
        new_node = LLNode(tindakan)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self) -> Optional[str]:
        """O(1) - Menghapus log terakhir untuk fitur UNDO_DOKTER [9, 16]."""
        if self.is_empty():
            return None
        res = self.top.data
        self.top = self.top.next
        self._size -= 1
        return res

    def is_empty(self) -> bool:
        return self.top is None

    def log_all(self) -> List[str]:
        """O(n) - Menampilkan seluruh riwayat per-sesi dokter [9]."""
        history = []
        curr = self.top
        while curr:
            history.append(curr.data)
            curr = curr.next
        return history
    
    # Pastikan class LLNode dan Stack yang kamu buat ada di atas kode ini

def test_stack_terminal():
    # Inisialisasi Stack untuk satu sesi dokter
    stack_riwayat = Stack()
    
    while True:
        print("\n" + "="*40)
        print("🏥 SISTEM RIWAYAT TINDAKAN DOKTER (STACK)")
        print("="*40)
        print("1. Tambah Tindakan Medis (Push)")
        print("2. Batalkan Tindakan Terakhir (Undo / Pop)")
        print("3. Tampilkan Semua Riwayat (Log All)")
        print("4. Cek Status Riwayat (Cek Kosong & Ukuran)")
        print("5. Keluar")
        print("-" * 40)
        
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == '1':
            tindakan = input("Masukkan nama tindakan (misal: 'Cek tensi 120/80'): ")
            try:
                stack_riwayat.push(tindakan)
                print(f"✅ [SUCCESS] Tindakan '{tindakan}' berhasil dicatat ke Stack.")
            except ValueError as e:
                print(f"❌ [ERROR] {e}")
                
        elif pilihan == '2':
            popped = stack_riwayat.pop()
            if popped:
                print(f"⏪ [UNDO SUCCESS] Tindakan '{popped}' telah dibatalkan.")
            else:
                print("⚠️ [FAILED] Riwayat kosong, tidak ada tindakan yang bisa di-undo.")
                
        elif pilihan == '3':
            riwayat = stack_riwayat.log_all()
            if riwayat:
                print("\n📋 --- Riwayat Tindakan (Terbaru ke Terlama) ---")
                for i, log in enumerate(riwayat, 1):
                    print(f"   {i}. {log}")
            else:
                print("ℹ️ [INFO] Riwayat masih kosong.")
                
        elif pilihan == '4':
            if stack_riwayat.is_empty():
                print("ℹ️ [INFO] Stack saat ini KOSONG.")
            else:
                print(f"ℹ️ [INFO] Stack terisi dengan {stack_riwayat._size} catatan tindakan.")
                
        elif pilihan == '5':
            print("👋 Keluar dari sistem pengujian Stack...")
            break
            
        else:
            print("❌ [ERROR] Pilihan tidak valid. Silakan ketik angka 1-5.")

# Blok ini memastikan testing hanya jalan kalau file ini dijalankan langsung di terminal
if __name__ == "__main__":
    test_stack_terminal()