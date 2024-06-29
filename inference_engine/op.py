from fact import Fact
from node import Node

class Operator(Node):
    def __init__(self, operator, expression=None, is_in_conclusion=False):
        super().__init__('[' + self.__to_string(expression) + ']')
        self.operator = operator
        self.value: bool | None = None
        self.expression = expression
        self.is_in_conclusion = is_in_conclusion
        self.facts = set()

    def get_propositions(self) -> set[Fact]:
        return set([child.get_propositions() for child in self.children])

    def __to_string(self, expression, enclose=False):
        if isinstance(expression, list):
            encloseSub=True
            if len(expression) < 3:
                enclose = False
            if enclose:
                return '(' + ' '.join(self.__to_string(i, encloseSub) for i in expression) + ')'
            else:
                return ' '.join(self.__to_string(i, encloseSub) for i in expression)
        else:
            return str(expression)