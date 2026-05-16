# =====================================================
# TEST STACK
# Validasi Stack menggunakan numpy seed=42
# =====================================================

import numpy as np
import random
import time

np.random.seed(42)
random.seed(42)

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_structures.stack import Stack


def test_push_pop():
    print("\n[TEST 1] Push & Pop basic")
    s = Stack()
    s.push("Tindakan A")
    hasil = s.pop()
    assert hasil == "Tindakan A", f"GAGAL: expected 'Tindakan A', got {hasil}"
    print("✅ PASSED")


def test_lifo():
    print("\n[TEST 2] LIFO — yang terakhir masuk pertama keluar")
    s = Stack()
    s.push("Pertama")
    s.push("Kedua")
    s.push("Ketiga")
    assert s.pop() == "Ketiga", "GAGAL: harusnya Ketiga"
    assert s.pop() == "Kedua", "GAGAL: harusnya Kedua"
    assert s.pop() == "Pertama", "GAGAL: harusnya Pertama"
    print("✅ PASSED")


def test_pop_kosong():
    print("\n[TEST 3] Pop dari stack kosong harus return None")
    s = Stack()
    assert s.pop() is None, "GAGAL: harusnya None"
    print("✅ PASSED")


def test_peek():
    print("\n[TEST 4] Peek tidak menghapus elemen")
    s = Stack()
    s.push("Top")
    assert s.peek() == "Top", "GAGAL: harusnya Top"
    assert len(s) == 1, "GAGAL: ukuran harusnya 1"
    print("✅ PASSED")


def test_is_empty():
    print("\n[TEST 5] is_empty")
    s = Stack()
    assert s.is_empty() is True, "GAGAL: harusnya True"
    s.push("data")
    assert s.is_empty() is False, "GAGAL: harusnya False"
    print("✅ PASSED")


def test_undo_simulasi():
    print("\n[TEST 6] Simulasi undo tindakan dokter")
    s = Stack()
    s.push("Periksa Andi")
    s.push("Resep Andi")
    s.push("Rujuk Andi")
    dibatalkan = s.pop()
    assert dibatalkan == "Rujuk Andi", f"GAGAL: expected 'Rujuk Andi', got {dibatalkan}"
    assert s.peek() == "Resep Andi", "GAGAL: harusnya Resep Andi"
    print("✅ PASSED")


def test_banyak_operasi():
    print("\n[TEST 7] Push & Pop 500 operasi (seed=42)")
    s = Stack()
    data = [f"Tindakan_{i}" for i in range(500)]

    # Push semua
    start = time.perf_counter()
    for d in data:
        s.push(d)
    waktu_push = (time.perf_counter() - start) * 1000

    assert len(s) == 500, f"GAGAL: ukuran harusnya 500, got {len(s)}"

    # Pop semua
    start = time.perf_counter()
    hasil = []
    while not s.is_empty():
        hasil.append(s.pop())
    waktu_pop = (time.perf_counter() - start) * 1000

    assert len(hasil) == 500, "GAGAL: jumlah pop harusnya 500"
    assert hasil[0] == "Tindakan_499", f"GAGAL: LIFO, harusnya Tindakan_499"
    print(f"✅ PASSED | Push: {waktu_push:.4f}ms | Pop: {waktu_pop:.4f}ms")


def test_log_all():
    print("\n[TEST 8] Log semua tindakan")
    s = Stack()
    s.push("Tindakan 1")
    s.push("Tindakan 2")
    s.push("Tindakan 3")
    s.log_all()
    print("✅ PASSED")


if __name__ == "__main__":
    print("=" * 50)
    print("  UNIT TEST — Stack")
    print("=" * 50)

    test_push_pop()
    test_lifo()
    test_pop_kosong()
    test_peek()
    test_is_empty()
    test_undo_simulasi()
    test_banyak_operasi()
    test_log_all()

    print("\n" + "=" * 50)
    print("  SEMUA TEST PASSED ✅")
    print("=" * 50)