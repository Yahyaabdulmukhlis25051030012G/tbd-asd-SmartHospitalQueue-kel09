from typing import Optional, List



class RekorMedis:
    def __init__(self, no_rm: int, nama: str, diagnosis: str):
        self.no_rm = no_rm
        self.nama = nama
        self.diagnosis = diagnosis

    def __repr__(self):
        return f"RM({self.no_rm}, {self.nama}, {self.diagnosis})"



class BSTNode:
    def __init__(self, rekord: RekorMedis):

        # Menyimpan data rekam medis
        self.rekord = rekord

        # Anak kiri dan kanan
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None



class BSTRekamMedis:
    def __init__(self):

        
        self.root: Optional[BSTNode] = None

    
    def insert(self, rekord: RekorMedis) -> None:

        
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

    
    def search(self, no_rm: int):

        return self._search_recursive(self.root, no_rm)

    def _search_recursive(self, node, no_rm):

        
        if node is None:
            return None

        
        if no_rm == node.rekord.no_rm:
            return node.rekord

        
        if no_rm < node.rekord.no_rm:
            return self._search_recursive(node.left, no_rm)

        
        return self._search_recursive(node.right, no_rm)

     
    def inorder(self):

        hasil = []

        self._inorder_recursive(self.root, hasil)

        return hasil

    def _inorder_recursive(self, node, hasil):

        if node:

            
            self._inorder_recursive(node.left, hasil)

            
            hasil.append(node.rekord)

            
            self._inorder_recursive(node.right, hasil)