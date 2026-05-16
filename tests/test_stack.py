import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.data_structures.stack import Stack

def test_push_pop():
    s = Stack()
    s.push("Tindakan A")
    assert s.pop() == "Tindakan A"

def test_lifo():
    s = Stack()
    s.push("Pertama")
    s.push("Kedua")
    s.push("Ketiga")
    assert s.pop() == "Ketiga"
    assert s.pop() == "Kedua"
    assert s.pop() == "Pertama"

def test_pop_kosong():
    s = Stack()
    assert s.pop() is None

def test_is_empty():
    s = Stack()
    assert s.is_empty() is True
    s.push("data")
    assert s.is_empty() is False

def test_undo_simulasi():
    s = Stack()
    s.push("Periksa Andi")
    s.push("Resep Andi")
    dibatalkan = s.pop()
    assert dibatalkan == "Resep Andi"