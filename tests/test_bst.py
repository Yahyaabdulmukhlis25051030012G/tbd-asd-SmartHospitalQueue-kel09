import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.data_structures.bst import BST
from dataclasses import dataclass
from typing import List

@dataclass
class RekamMedis:
    no_rm: int
    nama: str
    riwayat: List[str]

def buat_rm(no_rm, nama):
    return RekamMedis(no_rm, nama, [])

def test_insert_search():
    bst = BST()
    bst.insert(buat_rm(100, "Andi"))
    assert bst.search(100).nama == "Andi"

def test_search_tidak_ada():
    bst = BST()
    bst.insert(buat_rm(100, "Andi"))
    assert bst.search(999) is None

def test_inorder_terurut():
    bst = BST()
    for no in [300, 100, 200, 500, 400]:
        bst.insert(buat_rm(no, f"Pasien_{no}"))
    hasil = [r.no_rm for r in bst.inorder()]
    assert hasil == sorted(hasil)

def test_bst_kosong():
    bst = BST()
    assert bst.search(1) is None
    assert bst.inorder() == []