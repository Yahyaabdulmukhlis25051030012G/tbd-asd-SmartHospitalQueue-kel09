from typing import Optional, List, Tuple


# ── Node untuk Linked List dalam Adjacency List ─────────────────────
class EdgeNode:
    """Node untuk menyimpan informasi tetangga dan bobot."""

    __slots__ = ("dest", "weight", "next")

    def __init__(self, dest: str, weight: int = 1):
        self.dest = dest
        self.weight = weight
        self.next: Optional['EdgeNode'] = None


# ── Struktur Data Graph ─────────────────────────────────────────────
class ReferralGraph:
    """Graph untuk memodelkan alur rujukan antar poli rumah sakit."""

    def __init__(self, directed: bool = True):
        self.adj = {}
        self.is_directed = directed

    def add_poli(self, nama_poli: str) -> None:
        """Menambahkan poli baru."""
        if nama_poli not in self.adj:
            self.adj[nama_poli] = None

    def add_referral(self, u: str, v: str, weight: int = 1) -> None:
        """Menambahkan alur rujukan dari poli u ke poli v."""
        self.add_poli(u)
        self.add_poli(v)

        new_node = EdgeNode(v, weight)
        new_node.next = self.adj[u]
        self.adj[u] = new_node

        if not self.is_directed:
            new_node_rev = EdgeNode(u, weight)
            new_node_rev.next = self.adj[v]
            self.adj[v] = new_node_rev

    def get_referral_options(self, poli: str) -> List[Tuple[str, int]]:
        """Mengambil semua opsi rujukan dari poli tertentu."""
        options = []
        current = self.adj.get(poli)

        while current:
            options.append((current.dest, current.weight))
            current = current.next

        return options


# ── Unit Test ───────────────────────────────────────────────────────
def test_graph_referral():
    print("=== Menjalankan Test Graph Alur Rujukan ===")

    g = ReferralGraph(directed=True)

    print("Menambahkan alur: Umum -> Jantung, Umum -> Anak, Jantung -> ICU")

    g.add_referral("Umum", "Jantung", weight=5)
    g.add_referral("Umum", "Anak", weight=2)
    g.add_referral("Jantung", "ICU", weight=10)

    # Tes apakah poli terdaftar
    assert "Umum" in g.adj, "Gagal: Poli Umum tidak terdaftar"

    # Tes rujukan dari Poli Umum
    rujukan_umum = g.get_referral_options("Umum")

    print(f"Opsi rujukan dari Umum: {rujukan_umum}")

    assert len(rujukan_umum) == 2, (
        "Gagal: Umum harusnya punya 2 rujukan"
    )

    # Tes rujukan Jantung ke ICU
    rujukan_jantung = g.get_referral_options("Jantung")

    if rujukan_jantung:
        nama_tujuan = rujukan_jantung[0][0]

        assert nama_tujuan == "ICU", (
            f"Gagal: Diharapkan ICU, tapi mendapat {nama_tujuan}"
        )

        print(f"✅ Rujukan Jantung ke: {nama_tujuan} berhasil diproses.")
    else:
        assert False, "Gagal: Daftar rujukan Jantung kosong"

    print("\n" + "=" * 40)
    print("HASIL: TEST GRAPH RUJUKAN LULUS 100%")
    print("=" * 40)


if __name__ == "__main__":
    test_graph_referral()