class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Big-O: rata-rata O(log n), worst-case O(n)"""
        if not self.root:
            self.root = BSTNode(data)
            return
        self._insert(self.root, data)

    def _insert(self, node, data):
        if data.no_rm < node.data.no_rm:
            if not node.left:
                node.left = BSTNode(data)
            else:
                self._insert(node.left, data)
        else:
            if not node.right:
                node.right = BSTNode(data)
            else:
                self._insert(node.right, data)

    def search(self, no_rm):
        """Big-O: rata-rata O(log n), worst-case O(n)"""
        return self._search(self.root, no_rm)

    def _search(self, node, no_rm):
        if not node:
            return None
        if node.data.no_rm == no_rm:
            return node.data
        if no_rm < node.data.no_rm:
            return self._search(node.left, no_rm)
        return self._search(node.right, no_rm)

    def inorder(self):
        """Big-O: O(n)"""
        res = []
        self._inorder(self.root, res)
        return res

    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.data)
            self._inorder(node.right, res)