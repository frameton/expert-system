from fact import Fact
from op import Operator
from rule import Rule
from graph import Graph

class InferenceEngine():
    def __init__(self, rules: list[list], facts: list[str], goals: list[str], print=False):
        # self.rules: list = []
        # self.facts: dict[str, Fact] = {fact: Fact(fact, value=True) for fact in facts}
        # self.goals: list[Fact] = [Fact(goal, None) for goal in goals]
        # self.facts.update({goal.name: goal for goal in self.goals})

        self.graph = Graph()
        self.graph.build(rules)
        self.facts = self.graph.facts
        self.indent = 0

        for fact in facts:
            self.facts[fact].value = True

        self.goals = [self.facts[goal] for goal in goals]

        if print:
            self.graph.print()

    # TODO : point fact to rule directly and infer conditions and after the conclusion
    # TODO : the function to infer the conclusion is different and should keep the goal in mind
    # TODO : if the goal is children of | or ^, all other node have to be False together for the goal to be True
    # TODO : maybe for each fact, sort the parents rules by the depth of the goal in a conclusion.



    def get_fact_node(self, token: str) -> Fact:
        if token not in self.facts:
            self.facts[token] = Fact(token)
        return self.facts[token]

    def infer_goals(self):
        inferred_goals_count = 0
        loop_count_without_improvment = 0
        goals_to_infer = [goal for goal in self.goals if goal.value is None]
        while len(goals_to_infer) > 0 and loop_count_without_improvment < 1:
            for goal in goals_to_infer:
                print('Infering goal:', goal.name)
                if self.__infer_fact(goal) is not None:
                    inferred_goals_count += 1
            if inferred_goals_count > 0:
                loop_count_without_improvment = 0
                inferred_goals_count = 0
            else:
                loop_count_without_improvment += 1
            goals_to_infer = [goal for goal in goals_to_infer if goal.value is None]

    def __infer_fact(self, fact: Fact) -> bool | None:
        self.indent += 1
        print(f'{self.indent * '#'} Infering fact:', fact.name)
        if len(fact.parents) > 0:
            for parent in fact.parents:
                if isinstance(parent, Rule) and not parent.visited:
                    self.__infer_fact_from_rule(fact, parent)
                    if fact.value is not None:
                        break
        else:
            print(f'{self.indent * '#'} Fact cannot be inferred from rules')
        self.indent -= 1
        return fact.value

    def __infer_fact_from_rule(self, goal: Fact, rule: Rule):
        self.indent += 1
        print(f'{self.indent * '#'} From rule :', rule.name)
        rule.visited = True
        if self.__infer_conditions(rule.conditions) is True:
            rule.conclusions.value = True
            if goal.value is None:
                val = self.__infer_goal_from_conclusions(goal, rule.conclusions)
        rule.visited = False
        self.indent -= 1
        return goal.value

    def __infer_conditions(self, conditions: Fact | Operator) -> bool | None:
        self.indent += 1
        print(f'{self.indent * '#'} Compute condition :', conditions.name)
        if conditions.value is not None:
            self.indent += 1
            print(f'{self.indent * '#'} Value :', conditions.value)
            self.indent -= 2
            return conditions.value

        if isinstance(conditions, Fact):
            self.__infer_fact(conditions)
            self.indent -= 1
            return conditions.value

        node: Operator = conditions
        try:
            if node.operator == '+':
                for child in node.children:
                    val = self.__infer_conditions(child)
                    if val in [False, None]:
                        node.value = val
                        return val
                node.value = True
            elif node.operator == '|':
                containsNone = False
                for child in node.children:
                    val = self.__infer_conditions(child)
                    if val is True:
                        node.value = True
                        return True
                    if val is None:
                        containsNone = True
                node.value = None if containsNone else False
            elif node.operator == '^':
                trueCount = 0
                for child in node.children:
                    val = self.__infer_conditions(child)
                    if val is None:
                        node.value = None
                        return None
                    if val is True:
                        trueCount += 1
                node.value = trueCount % 2 == 1
            elif node.operator == '!':
                val = self.__infer_conditions(node.children[0])
                if val is None:
                    node.value = None
                    return None
                node.value = not val

            self.indent += 1
            print(f'{self.indent * '#'} Value :', node.name)
            self.indent -= 2
            return node.value
        except:
            node.value = None
            self.indent += 1
            print(f'{self.indent * '#'} Error in computing :', node.name)
            self.indent -= 2
            return None


    def __infer_goal_from_conclusions(self, goal: Fact, conclusions: Fact|Operator):
        self.indent += 1
        print(f'{self.indent * '#'} Compute conclusion :', conclusions.name)

        if isinstance(conclusions, Fact):
            if conclusions is goal:
                self.indent += 1
                print(f'{self.indent * '#'} {goal.name} is {goal.value} :')
                self.indent -= 2
                return goal.value
            else:
                self.indent -= 1
                raise Exception('Conclusions is a fact which is not the goal, this should not happen')

        node: Operator = conclusions

        if node.operator == '+':
            # AND TRUE
            if node.value is True:

                operators_with_goal: list[Operator] = []
                for child in node.children:
                    child.value = True
                    if isinstance(child, Operator) and goal in child.facts:
                        operators_with_goal.append(child)

                if goal.value is not None:
                    return goal.value

                operators_with_goal = sorted(operators_with_goal, key=lambda x: len(x.children))
                for operator in operators_with_goal:
                    if self.__infer_goal_from_conclusions(goal, operator) is True:
                        return True
                return None
            # AND FALSE
            else:
                operators_with_goal: list[Operator] = []
                children_without_goal: list[Fact|Operator] = []
                for child in node.children:
                    if (isinstance(child, Operator) and goal in child.facts) or child is goal:
                        operators_with_goal.append(child)
                    else:
                        children_without_goal.append(child)
                for child in children_without_goal:
                    val = self.__infer_conditions(child)
                    if val is not True:
                        return None
                if len(operators_with_goal) != 1:
                    raise Exception('There should be only one operator with the goal')
                operators_with_goal[0].value = False
                val = self.__infer_goal_from_conclusions(goal, operators_with_goal[0])
                if val is False:
                    return False
                return None

        elif node.operator == '|':
            # OR TRUE
            if node.value is True:
                operators_with_goal: list[Operator] = []
                children_without_goal: list[Fact|Operator] = []
                for child in node.children:
                    if (isinstance(child, Operator) and goal in child.facts) or child is goal:
                        operators_with_goal.append(child)
                    else:
                        children_without_goal.append(child)
                for child in children_without_goal:
                    val = self.__infer_conditions(child)
                    if val is not False:
                        return None
                if len(operators_with_goal) != 1:
                    raise Exception('There should be only one operator with the goal')
                operators_with_goal[0].value = True
                val = self.__infer_goal_from_conclusions(goal, operators_with_goal[0])
                if val is True:
                    return True
                return None
            # OR FALSE
            else:
                operators_with_goal: list[Operator] = []
                for child in node.children:
                    child.value = False
                    if (isinstance(child, Operator) and goal in child.facts) or child is goal:
                        operators_with_goal.append(child)

                if goal.value is not None:
                    return goal.value

                operators_with_goal = sorted(operators_with_goal, key=lambda x: len(x.children))
                for operator in operators_with_goal:
                    if self.__infer_goal_from_conclusions(goal, operator) is False:
                        return False
                return None
        # XOR
        elif node.operator == '^':
            operators_with_goal: list[Operator] = []
            children_without_goal: list[Fact|Operator] = []
            for child in node.children:
                if (isinstance(child, Operator) and goal in child.facts) or child is goal:
                    operators_with_goal.append(child)
                else:
                    children_without_goal.append(child)
            trueCount = 0
            for child in children_without_goal:
                val = self.__infer_conditions(child)
                if val is True:
                    trueCount += 1
            if len(operators_with_goal) != 1:
                raise Exception('There should be only one operator with the goal')

            if node.value is True and trueCount % 2 == 1:
                return None
            if node.value is False and trueCount % 2 == 0:
                return None

            operators_with_goal[0].value = node.value
            val = self.__infer_goal_from_conclusions(goal, operators_with_goal[0])
            if val is node.value:
                return node.value
            return None
        # NOT
        elif node.operator == '!':
            node.children[0].value = not node.value
            val = self.__infer_goal_from_conclusions(goal, node.children[0])
            if val is None:
                return None
            return not val


    # def __dfs_infer(self, node, fact_to_infer:Fact|None=None, prev_node:Node|None=None):
    #     print('Infering: ', node.name, '...')
    #     if isinstance(node, Fact):
    #         print("\tit's a fact")
    #         if node.value is True:
    #             print("\t\tvalue is True, returning...")
    #             return True
    #         print("\tparents: ", [parent.name for parent in node.parents])
    #         # if node.name == 'C':
    #         #     print([parent.name for parent in node.parents if not parent.visited])
    #         for parent in node.parents:
    #             if not parent.visited:
    #                 val = self.__dfs_infer(parent, fact_to_infer=node, prev_node=node)
    #                 if val is not None:
    #                     node.value = val
    #                     return val
    #         return None
    #     elif isinstance(node, Operator):
    #         print("\tit's an expression")
    #         print("\t", node.name, node.operator, node.value, node.is_in_conclusion)
    #         if node.value is True:
    #             print("\t\tvalue is True, returning...")
    #             return True
    #         if node.operator == '+':
    #             return all(self.__dfs_infer(child, prev_node=node) for child in node.children)
    #         elif node.operator == '|':
    #             if fact_to_infer in node.children:
    #                 print("\t\tfact to infer in children")
    #                 if node.is_in_conclusion:
    #                     print("\t\tfact to infer in conclusion")
    #                     print([child.name for child in node.children if child is not fact_to_infer])
    #                     return all(self.__dfs_infer(child, prev_node=node) is False for child in node.children if child is not fact_to_infer)
    #                     # return True
    #                 else:
    #                     return None
    #             return any(self.__dfs_infer(child, prev_node=node) is True for child in node.children)
    #         elif node.operator == '^':
    #             return self.__dfs_infer(node.children[0], prev_node=node) != self.__dfs_infer(node.children[1], prev_node=node)
    #         elif node.operator == '!':
    #             if fact_to_infer is node.children[0] and node.is_in_conclusion:
    #                 return not self.__dfs_infer(node.children[0], prev_node=node)
    #             return not self.__dfs_infer(node.children[0], prev_node=node)
    #     elif isinstance(node, Rule):
    #         node.visited = True
    #         val = None
    #         if self.__dfs_infer(node.conditions, fact_to_infer=fact_to_infer, prev_node=node):
    #             val = self.__dfs_infer(node.conclusions, fact_to_infer=fact_to_infer, prev_node=node)
    #         node.visited = False
    #         return val
    #     return None


    def print_facts(self):
        for fact in self.facts.values():
            print(fact.name, ':', fact.value)

# if __name__ == '__main__':
#     rules = [
#         # [['A', '+', 'B'], '=>', 'D'],
#         # [['A', '+', 'B'], '=>', ['C', '+', 'D']],
#         [['A', '+', 'B'], '=>', ['C', '|', ['A', '|', 'D'], '|', ['D', '^', 'C']]],
#         # [['A', '+', 'B'], '=>', ['C', '^', 'D']],
#         ['B', '=>', ['!', 'C']]
#     ]
#     engine = InferenceEngine(
#         rules,
#         facts=['A', 'B'],
#         goals=['D'],
#         # print=True
#     )
#     engine.infer_goals()

#     engine.print_facts()

