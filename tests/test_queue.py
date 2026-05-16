import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import pytest
from src.data_structures.queue import PriorityQueue

from dataclasses import dataclass

@dataclass
class Pasien:
    no_antrian: int
    nama: str
    poli: str
    prioritas: int
    waktu_daftar: float
    waktu_tunggu: float = 0.0

def buat_pasien(no, nama, prioritas):
    return Pasien(no, nama, "Umum", prioritas, time.time())

def test_enqueue_dequeue_basic():
    pq = PriorityQueue()
    p = buat_pasien(1, "Andi", 3)
    pq.enqueue(p)
    assert pq.dequeue().nama == "Andi"

def test_kritis_duluan():
    pq = PriorityQueue()
    pq.enqueue(buat_pasien(1, "Reguler", 3))
    pq.enqueue(buat_pasien(2, "Kritis", 1))
    assert pq.dequeue().nama == "Kritis"

def test_urutan_lengkap():
    pq = PriorityQueue()
    pq.enqueue(buat_pasien(1, "A", 3))  # REGULER
    pq.enqueue(buat_pasien(2, "B", 1))  # KRITIS
    pq.enqueue(buat_pasien(3, "C", 2))  # PRIORITAS
    urutan = []
    while not pq.is_empty():
        urutan.append(pq.dequeue().nama)
    assert urutan == ["B", "C", "A"]

def test_dequeue_kosong():
    pq = PriorityQueue()
    assert pq.dequeue() is None

def test_is_empty():
    pq = PriorityQueue()
    assert pq.is_empty() is True
    pq.enqueue(buat_pasien(1, "X", 3))
    assert pq.is_empty() is False