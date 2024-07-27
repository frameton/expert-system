from inference_engine.node import Node
from inference_engine.fact import Fact
from inference_engine.op import Operator

class Rule(Node):
    def __init__(self, expression: list, conditions:Fact | Operator=Fact(''), conclusions:Fact | Operator=Fact('')):
        super().__init__('[' + self.__to_string(expression) + ']')
        self.expression = expression

        self.conditions: Fact | Operator = conditions
        self.facts_in_conditions = set()

        self.conclusions: Fact | Operator = conclusions
        self.facts_in_conclusions = set()

        self.visited: bool = False

    def __to_string(self, expression, enclose=False):
        if isinstance(expression, list):
            encloseSub=True
            if len(expression) < 3:
                enclose = False
            elif any(i in ['=>', '<=>'] for i in expression):
                encloseSub = False

            if enclose:
                return '(' + ' '.join(self.__to_string(i, encloseSub) for i in expression) + ')'
            else:
                return ' '.join(self.__to_string(i, encloseSub) for i in expression)
        else:
            return str(expression)