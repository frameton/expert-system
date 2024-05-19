from enum import Enum

class TokenType(Enum):
    ID = 1          # identifier, like variables, [A-Z] here
    QUESTION = 2    # ?
    EQUALS = 3      # =
    IFF = 4         # <=>
    IMPLIES = 5     # =>
    NOT = 6         # !
    XOR = 7         # ^
    OR = 8          # |
    AND = 9         # +
    RPAREN = 10     # )
    LPAREN = 11     # (
    EOF = 12        # end of file

class TokenPosition:
    def __init__(self, line, col):
        self.line = line
        self.col = col

class Token:
    def __init__(self, type: TokenType, value: str, position: TokenPosition):
        self.type = type
        self.value = value
        self.position = position

    def __str__(self):
        return f"{self.type}({self.value}) at {self.position.line}:{self.position.col}"




