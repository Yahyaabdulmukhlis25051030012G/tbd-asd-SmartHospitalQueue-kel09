from dataclasses import dataclass
from typing import Optional, List

@dataclass
class RekorMedis:
    no_rm: int              # Kunci utama (Key) untuk BST
    nama: str
    riwayat: List[str]      # List tindakan medis dokter

class BSTNode:
    def __init__(self, rekord: RekorMedis):
        self.rekord = rekord
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BSTRekamMedis:
    def __init__(self):
        """Membuat pohon rekam medis yang awalnya kosong."""
        self.root: Optional[BSTNode] = None

    # 1. OPERASI INSERT
    def insert(self, rekord: RekorMedis) -> None:
        """
        Menyisipkan rekam medis baru ke dalam pohon.
        
        Analisis Kompleksitas Waktu:
        - Rata-rata: O(log n) - Jika pohon seimbang.
        - Terburuk (Worst-case): O(n) - Terjadi jika data (no_rm) dimasukkan 
          secara terurut (misal: 101, 102, 103), menyebabkan pohon menjadi 
          miring (linear) seperti Linked List [2, 4].
        """
        if self.root is None:
            self.root = BSTNode(rekord)
        else:
            self._insert_recursive(self.root, rekord)

    def _insert_recursive(self, node: BSTNode, rekord: RekorMedis):
        if rekord.no_rm < node.rekord.no_rm:
            if node.left is None:
                node.left = BSTNode(rekord)
            else:
                self._insert_recursive(node.left, rekord)
        elif rekord.no_rm > node.rekord.no_rm:
            if node.right is None:
                node.right = BSTNode(rekord)
            else:
                self._insert_recursive(node.right, rekord)

    # 2. OPERASI SEARCH
    def search(self, no_rm: int) -> Optional[RekorMedis]:
        """
        Mencari data rekam medis berdasarkan no_rm.
        
        Analisis Kompleksitas Waktu:
        - Rata-rata O(log n), Terburuk O(n) mengikuti tinggi pohon (h) [5, 6].
        """
        return self._search_recursive(self.root, no_rm)

    def _search_recursive(self, node: Optional[BSTNode], no_rm: int) -> Optional[RekorMedis]:
        if node is None or node.rekord.no_rm == no_rm:
            return node.rekord if node else None
        if no_rm < node.rekord.no_rm:
            return self._search_recursive(node.left, no_rm)
        return self._search_recursive(node.right, no_rm)

    # 3. OPERASI DELETE (Penyempurnaan Wajib)
    def delete(self, no_rm: int) -> None:
        """
        Menghapus data rekam medis berdasarkan no_rm.
        
        Analisis Kompleksitas Waktu: O(h), di mana h adalah tinggi pohon.
        Rata-rata O(log n), Terburuk O(n) [6, 7].
        """
        self.root = self._delete_recursive(self.root, no_rm)

    def _delete_recursive(self, node: Optional[BSTNode], no_rm: int) -> Optional[BSTNode]:
        if node is None:
            return None

        if no_rm < node.rekord.no_rm:
            node.left = self._delete_recursive(node.left, no_rm)
        elif no_rm > node.rekord.no_rm:
            node.right = self._delete_recursive(node.right, no_rm)
        else:
            # Case 1 & 2: Node dengan 0 atau 1 anak
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Case 3: Node dengan 2 anak
            # Cari pendahulu inorder (node terbesar di sub-pohon kiri) [8, 9]
            predecessor = self._max_value_node(node.left)
            node.rekord = predecessor.rekord
            # Hapus pendahulu tersebut
            node.left = self._delete_recursive(node.left, predecessor.rekord.no_rm)
        
        return node

    def _max_value_node(self, node: BSTNode) -> BSTNode:
        current = node
        while current.right is not None:
            current = current.right
        return current

    # 4. TRAVERSAL INORDER
    def inorder(self) -> List[RekorMedis]:
        """
        Menghasilkan list rekam medis yang terurut berdasarkan no_rm.
        Analisis Kompleksitas Waktu: O(n) karena mengunjungi setiap node [10, 11].
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[BSTNode], result: List[RekorMedis]):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.rekord)
            self._inorder_recursive(node.right, result)


# =====================================
# TEST PROGRAM BST REKAM MEDIS
# =====================================
if __name__ == "__main__":
    # Membuat object BST
    bst = BSTRekamMedis()

    # =================================
    # INSERT DATA
    # =================================
    bst.insert(RekorMedis(102, "Andi", ["Pemeriksaan Umum", "Pemberian Obat"]))
    bst.insert(RekorMedis(101, "Budi", ["Tes Darah"]))
    bst.insert(RekorMedis(105, "Citra", ["Rontgen", "Kontrol"]))
    bst.insert(RekorMedis(103, "Dina", ["Vaksinasi"]))
    bst.insert(RekorMedis(104, "Eko", ["Rawat Jalan"]))

    # =================================
    # MENAMPILKAN DATA TERURUT
    # =================================
    print("\n=== DATA REKAM MEDIS (INORDER) ===")
    for data in bst.inorder():
        print(f"No RM      : {data.no_rm}\nNama       : {data.nama}\nRiwayat    : {data.riwayat}\n")

    # =================================
    # SEARCH DATA
    # =================================
    print("\n=== SEARCH DATA ===")
    hasil = bst.search(103)

    if hasil:
        print("Data ditemukan:")
        print(f"No RM   : {hasil.no_rm}")
        print(f"Nama    : {hasil.nama}")
        print(f"Riwayat : {hasil.riwayat}")
    else:
        print("Data tidak ditemukan")

    # =================================
    # DELETE DATA
    # =================================
    print("\n=== DELETE DATA ===")
    bst.delete(102)

    print("Data setelah no_rm 102 dihapus:\n")
    for data in bst.inorder():
        print(f"No RM      : {data.no_rm}\nNama       : {data.nama}\nRiwayat    : {data.riwayat}\n")