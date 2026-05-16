from typing import Optional, List, Tuple

# ── Node untuk Linked List dalam Adjacency List ─────────────────────
class EdgeNode:
    """Node untuk menyimpan informasi tetangga dan bobot (biaya/jarak)."""
    __slots__ = 'dest', 'weight', 'next'

    def __init__(self, dest: str, weight: int = 1):
        self.dest = dest      # ID/Nama Poli tujuan
        self.weight = weight  # Bobot rujukan (misal: urgensi atau jarak)
        self.next: Optional['EdgeNode'] = None

# ── Struktur Data Graph ───────────────────────────────────────────
class ReferralGraph:
    """Graph untuk memodelkan alur rujukan antar poli rumah sakit."""
    
    def __init__(self, directed: bool = True):
        # Dictionary yang memetakan nama poli ke head dari linked list tetangga
        self.adj = {} 
        self.is_directed = directed

    def add_poli(self, nama_poli: str) -> None:
        """Menambahkan node poli baru. Big-O: O(1)."""
        if nama_poli not in self.adj:
            self.adj[nama_poli] = None

    def add_referral(self, u: str, v: str, weight: int = 1) -> None:
        """
        Menambahkan alur rujukan dari poli u ke poli v.
        Big-O: O(1) karena penyisipan dilakukan di head linked list [4].
        """
        self.add_poli(u)
        self.add_poli(v)
        
        # Tambah v sebagai tetangga u (di bagian depan/head)
        new_node = EdgeNode(v, weight)
        new_node.next = self.adj[u]
        self.adj[u] = new_node
        
        # Jika tidak berarah, lakukan sebaliknya
        if not self.is_directed:
            new_node_rev = EdgeNode(u, weight)
            new_node_rev.next = self.adj[v]
            self.adj[v] = new_node_rev

    def get_referral_options(self, poli: str) -> List[Tuple[str, int]]:
        """
        Mengambil semua opsi rujukan dari poli tertentu.
        Big-O: O(deg(u)) atau linear terhadap jumlah rujukan poli tersebut [4].
        """
        options = []
        current = self.adj.get(poli)
        while current:
            options.append((current.dest, current.weight))
            current = current.next
        return options