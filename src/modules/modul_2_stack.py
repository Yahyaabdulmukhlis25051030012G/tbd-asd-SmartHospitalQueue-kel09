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