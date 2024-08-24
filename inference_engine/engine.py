from typing import Tuple

from inference_engine.fact import Fact
from inference_engine.op import Operator
from inference_engine.rule import Rule
from inference_engine.graph import Graph

class InferenceEngine():
    def __init__(self, rules: list[list], facts: list[str], goals: list[str], should_print_graph=False, should_output_resolution_steps=True):
        self.graph = Graph()
        self.graph.build(rules)
        self.facts = self.graph.facts

        self.should_output_resolution_steps = should_output_resolution_steps

        for fact in self.facts.values():
            if len(fact.parents) == 0:
                fact.value = False
            if fact.name in facts:
                fact.value = True

        self.goals = [self.facts[goal] for goal in goals]

        if should_print_graph:
            self.graph.print()

    def get_fact_node(self, token: str) -> Fact:
        if token not in self.facts:
            self.facts[token] = Fact(token)
        return self.facts[token]

    def infer_goals(self):
        goals_to_infer = [goal for goal in self.goals if goal.value is None]

        if len(goals_to_infer) == 0:
            self.output_resolution_step('No goals to infer')
            return

        inferred_goals_count = 0
        loop_count_without_improvement = 0

        while len(goals_to_infer) > 0 and loop_count_without_improvement < 3:
            self.output_resolution_step('Goals to infer', len(goals_to_infer))
            self.output_resolution_step('Attemps without improvement', loop_count_without_improvement)
            for goal in goals_to_infer:
                self.output_resolution_step('Infering goal', goal.name, '...')
                value, steps = self.__infer_fact(goal)
                if value is not None:
                    for step in steps:
                        self.output_resolution_step(step)
                    inferred_goals_count += 1
            if inferred_goals_count > 0:
                loop_count_without_improvement = 0
                inferred_goals_count = 0
            else:
                loop_count_without_improvement += 1
            goals_to_infer = [goal for goal in goals_to_infer if goal.value is None]

        if loop_count_without_improvement == 3:
            self.output_resolution_step('No more improvement')
        self.output_resolution_step('Inference done')

    def __infer_fact(self, fact: Fact) -> Tuple[bool | None, list]:

        steps = []
        if len(fact.parents) > 0:
            for parent in fact.parents:
                if isinstance(parent, Rule) and not parent.visited:
                    value, s = self.__infer_fact_from_rule(fact, parent)
                    if value is not None:
                        steps += ['Infering fact ' + fact.name] + s
                        break

        return fact.value, steps

    def __infer_fact_from_rule(self, goal: Fact, rule: Rule) -> Tuple[bool | None, list]:


        steps = ['Infering from rule ' + rule.name]
        rule.visited = True
        cond_value, cond_steps = self.__infer_conditions(rule.conditions)
        if cond_value is True:
            rule.conclusions.value = True
            if goal.value is None:
                conc_val, conc_steps = self.__infer_goal_from_conclusions(goal, rule.conclusions)
                if conc_val is not None:
                    steps += cond_steps + conc_steps + ['We can infer that ' + goal.name + ' is ' + str(conc_val)]
        rule.visited = False

        return goal.value, steps

    def __infer_conditions(self, conditions: Fact | Operator) -> Tuple[bool | None, list]:
        if conditions.value is not None:
            return conditions.value, ['We know that '  + conditions.name + ' is ' + str(conditions.value)]

        if isinstance(conditions, Fact):
            value, steps = self.__infer_fact(conditions)
            return conditions.value, steps


        node: Operator = conditions
        steps = ['Infering ' + node.name]
        try:
            if node.operator == '+':
                for child in node.children:
                    val, s = self.__infer_conditions(child)
                    steps += s
                    if val is False:
                        node.value = val
                        return val, s
                    if val is None:
                        node.value = None
                        return None, []
                node.value = True
                steps += ['All operands are True so ' + node.name + ' is True']
            elif node.operator == '|':
                containsNone = False
                for child in node.children:
                    val, s = self.__infer_conditions(child)
                    steps += s
                    if val is True:
                        node.value = True
                        return True, s + ['One operand is True so ' + node.name + ' is True']
                    if val is None:
                        containsNone = True
                node.value = None if containsNone else False
                steps = [] if containsNone else steps
            elif node.operator == '^':
                trueCount = 0
                for child in node.children:
                    val, s = self.__infer_conditions(child)
                    steps += s
                    if val is None:
                        node.value = None
                        return None, []
                    if val is True:
                        trueCount += 1
                node.value = trueCount % 2 == 1
            elif node.operator == '!':
                val, s = self.__infer_conditions(node.children[0])
                steps += s
                if val is None:
                    node.value = None
                    return None, []
                node.value = not val

            return node.value, steps
        except:
            node.value = None

            return None, []


    def __infer_goal_from_conclusions(self, goal: Fact, conclusions: Fact|Operator) -> Tuple[bool | None, list]:

        if isinstance(conclusions, Fact):
            if conclusions is goal:
                return goal.value, []
            else:
                raise Exception('Conclusions is a fact which is not the goal, this should not happen')

        node: Operator = conclusions
        steps = ['Infering ' + node.name]
        if node.operator == '+':
            # AND TRUE
            if node.value is True:
                operators_with_goal: list[Operator] = []
                for child in node.children:
                    child.value = True
                    if isinstance(child, Operator) and goal in child.facts:
                        operators_with_goal.append(child)

                if goal.value is not None:
                    return goal.value, [node.name + ' is True so all operands are True']

                operators_with_goal = sorted(operators_with_goal, key=lambda x: len(x.children))
                for operator in operators_with_goal:
                    val, s = self.__infer_goal_from_conclusions(goal, operator)
                    steps += s
                    if val is True:
                        return True, s
                return None, []
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
                    val, s = self.__infer_conditions(child)
                    steps += s
                    if val is None:
                        return None, []
                    if val is False:
                        return False, s
                if len(operators_with_goal) != 1:
                    raise Exception('There should be only one sub expression with the same goal')
                operators_with_goal[0].value = False
                val, s = self.__infer_goal_from_conclusions(goal, operators_with_goal[0])
                steps += s
                if val is False:
                    return False, steps
                return None, []

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
                    val, s = self.__infer_conditions(child)
                    steps += s
                    if val is not False:
                        return None, []
                if len(operators_with_goal) != 1:
                    raise Exception('There should be only one sub expression with the same goal')
                operators_with_goal[0].value = True
                val, s = self.__infer_goal_from_conclusions(goal, operators_with_goal[0])
                steps += s
                if val is True:
                    return True, steps
                return None, []
            # OR FALSE
            else:
                operators_with_goal: list[Operator] = []
                for child in node.children:
                    child.value = False
                    if (isinstance(child, Operator) and goal in child.facts) or child is goal:
                        operators_with_goal.append(child)

                if goal.value is not None:
                    return goal.value, [node.name + ' is False so all operands are False']

                operators_with_goal = sorted(operators_with_goal, key=lambda x: len(x.children))
                for operator in operators_with_goal:
                    val, s = self.__infer_goal_from_conclusions(goal, operator)
                    steps += s
                    if val is False:
                        return False, steps
                return None, []
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
                val, s = self.__infer_conditions(child)
                steps += s
                if val is True:
                    trueCount += 1
            if len(operators_with_goal) != 1:
                raise Exception('There should be only one sub expression with the same goal')

            if node.value is True and trueCount % 2 == 1:
                return None, []
            if node.value is False and trueCount % 2 == 0:
                return None, []

            operators_with_goal[0].value = node.value
            val, s = self.__infer_goal_from_conclusions(goal, operators_with_goal[0])
            steps += s
            if val is node.value:
                return node.value, steps
            return None, []
        # NOT
        elif node.operator == '!':
            node.children[0].value = not node.value
            val, s = self.__infer_goal_from_conclusions(goal, node.children[0])
            steps += s
            if val is None:
                return None, []
            return val, steps
        return None, []

    def print_facts(self):
        return self.facts.values()

    def output_resolution_step(self, *elements):
        if self.should_output_resolution_steps:
            for el in elements:
                print(el)


