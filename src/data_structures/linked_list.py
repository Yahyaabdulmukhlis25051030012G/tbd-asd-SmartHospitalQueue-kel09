class LLNode:
    __slots__ = 'data', 'next' 

    def __init__(self, data=None, next=None): 
        self.data = data
        self.next = next