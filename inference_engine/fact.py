from typing import Self
from node import Node

class Fact(Node):
    def __init__(self, name, value: bool | None = None):
        super().__init__(name)
        self.value: bool | None = value

    def get_propositions(self) -> set[Self]:
        return { self }