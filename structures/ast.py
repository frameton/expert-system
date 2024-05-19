from structures.token import Token, TokenType
from __future__ import annotations


class Queries:
    def __init__(self, ids: list[Token]):
        if len(ids) < 1:
            raise ValueError("Queries must have at least one query")
        if not all(x.type == TokenType.ID for x in ids):
            raise ValueError("All queries must be of type ID")
        self.ids = ids

    def extract_ids(self) -> set[str]:
        return set(x.value for x in self.ids)


class Facts:
    def __init__(self, ids: list[Token]):
        if len(ids) < 1:
            raise ValueError("Facts must have at least one fact")
        if not all(x.type == TokenType.ID for x in ids):
            raise ValueError("All facts must be of type ID")
        self.ids = ids

    def extract_ids(self) -> set[str]:
        return set(x.value for x in self.ids)


class Atom:
    def __init__(self, value: Token | Xor):
        self.value = value

    def extract_ids(self) -> set[str]:
        if isinstance(self.value, Token):
            return {self.value.value}
        return self.value.extract_ids()


class Not:
    def __init__(self, value: Atom, operator: Token | None = None):
        if operator.type not in [None, TokenType.NOT]:
            raise ValueError("Invalid operator type")
        self.operator = operator
        self.value = value

    def extract_ids(self) -> set[str]:
        return self.value.extract_ids()

# * We could imagine a way to represent multiple negations to prevent the need for multiple Not nodes
# class Not:
#     def __init__(self, operator: Token, negations: int, atom: Atom):
#         self.operator = operator
#         self.negated = abs(negations) % 2 != 0 # ex: !!A => A
#         self.atom = atom


class And:
    def __init__(self, operator: Token, left, rights):
        if operator.type not in [None, TokenType.AND]:
            raise ValueError("Invalid operator type")
        self.operator = operator
        self.left = left
        self.rights = rights  # list of (operator, right) pairs

    def extract_ids(self) -> set[str]:
        return self.left.extract_ids().union(*(x.extract_ids() for x in self.rights))


class Or:
    def __init__(self, left: And, operator: Token | None = None, rights: list[And] = []):
        if operator.type not in [None, TokenType.XO]:
            raise ValueError("Invalid operator type")
        self.operator = operator
        self.left = left
        self.rights = rights  # list of (operator, right) pairs

    def extract_ids(self) -> set[str]:
        return self.left.extract_ids().union(*(x.extract_ids() for x in self.rights))


class Xor:
    def __init__(self, left: Or, operator: Token | None = None, rights: list[Or] = []):
        if operator.type not in [None, TokenType.XOR]:
            raise ValueError("Invalid operator type")
        self.operator = operator
        self.left = left
        self.rights = rights

    def extract_ids(self) -> set[str]:
        return self.left.extract_ids().union(*(x.extract_ids() for x in self.rights))


class Implication:
    def __init__(self, operator: Token, left: Xor, right: Xor):
        if operator.type not in [TokenType.IMPLIES, TokenType.IFF]:
            raise ValueError("Invalid operator type")
        self.operator = operator
        self.left = left
        self.right = right

    def extract_ids(self) -> set[str]:
        return self.left.extract_ids().union(self.right.extract_ids())


class Statement:
    def __init__(self, implication: Implication):
        self.implication = implication

    def extract_ids(self) -> set[str]:
        return self.implication.extract_ids()

class AST:
    def __init__(self, statements: list[Statement], facts: Facts, queries: Queries):
        self.statements = statements
        self.facts = facts
        self.queries = queries

    def extract_ids(self) -> set[str]:
        s = set()
        for statement in self.statements:
            s.update(statement.extract_ids())
        return s.union(self.facts.extract_ids(), self.queries.extract_ids())

















