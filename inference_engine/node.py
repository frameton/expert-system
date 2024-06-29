
class Node:
    def __init__(self, name):
        self.name: str = name
        self.parents = []
        self.children = []