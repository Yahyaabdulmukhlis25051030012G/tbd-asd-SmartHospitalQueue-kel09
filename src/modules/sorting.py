# =====================================================
# SORTING MODULE
# Implementasi Insertion Sort & Selection Sort
# langsung pada Linked List (bukan Python list biasa)
# Big-O: O(n²) untuk keduanya
# =====================================================

from src.data_structures.node import Node


class LinkedListPasien:
    """
    Linked List khusus untuk menyimpan daftar pasien selesai.
    Digunakan sebagai input sorting laporan harian.
    """
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, pasien):
        """Tambah pasien di akhir. Big-O: O(n)"""
        node = Node(pasien)
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
        """Konversi ke Python list untuk ditampilkan. Big-O: O(n)"""
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
    Insertion Sort berdasarkan waktu_tunggu DESCENDING
    (pasien tunggu terlama tampil pertama).
    Implementasi langsung pada Linked List.
    Big-O: O(n²) worst-case, O(n) jika sudah terurut.
    """
    if not ll.head or not ll.head.next:
        return ll

    sorted_head = None  # head linked list hasil sort

    cur = ll.head
    while cur:
        next_node = cur.next  # simpan node berikutnya
        cur.next = None

        # Sisipkan cur ke posisi yang tepat di sorted list
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
    Selection Sort berdasarkan no_antrian ASCENDING
    (nomor antrian terkecil tampil pertama).
    Implementasi langsung pada Linked List.
    Big-O: O(n²) selalu.
    """
    if not ll.head or not ll.head.next:
        return ll

    cur = ll.head
    while cur:
        # Cari node dengan no_antrian terkecil dari cur ke akhir
        min_node = cur
        check = cur.next
        while check:
            if check.data.no_antrian < min_node.data.no_antrian:
                min_node = check
            check = check.next

        # Tukar data (bukan pointer, lebih simpel di LL)
        cur.data, min_node.data = min_node.data, cur.data

        cur = cur.next

    return ll