
from typing import Self


class Id:
    def __init__(self, name: str, value: bool | None = None):
        self.name = name
        self.value = value
        self.parents = []

    def __str__(self):
        return self.name + (f"={self.value}" if self.value is not None else "=Unknown")

class Node:
    def __init__(self):
        self.operator = None
        self.children = []
        self.parent = None

class InferenceEngine():
    def __init__(self, rules: list[list], facts: list[str], to_infer: list[str]):
        self.rules = rules

        self.knowledge_base = {item: Id(item, None) for item in extractIdentifiers(rules)}
        self.to_infer = []

        for token in facts:
            if token.isalpha():
                self.identifiers[token].value = True
                self.knowledge_base.append(self.identifiers[token])
            else:
                raise ValueError("All tokens in knowledge_base must be alphabetical")

        for token in to_infer:
            if token.isalpha():
                self.to_infer.append(self.identifiers[token])
            else:
                raise ValueError("All tokens in to_infer must be alphabetical")

        self.graph = self.build_graph(rules, None)


    def build_graph(self, expression: list | str, parent: Node | None) -> Node:
        node = Node()
        node.parent = parent
        for element in expression:
            if isinstance(element, list):
                node.children.append(self.build_graph(element, node))
            elif isinstance(element, str):
                if element.isalpha():
                    id = self.knowledge_base[element]
                    id.parents.append(node)
                    node.children.append(id)
                else:
                    node.operator = element
        return node

    def infer(self):
        while not all(id.value is not None for id in self.to_infer):
            for id in self.to_infer:
                if id.value is None:
                    # self.infer_id(id)
                    pass

def extractIdentifiers(nested_list: list) -> set[str]:
    identifiers = set()
    for element in nested_list:
        if isinstance(element, list):
            identifiers.add(extractIdentifiers(element))
        elif isinstance(element, str) and element.isalpha():
            identifiers.add(element)
    return identifiers
