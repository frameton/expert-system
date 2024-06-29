from copy import copy
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from op import Operator
from node import Node
from rule import Rule
from fact import Fact

class Graph():
    def __init__(self):
        self.rules: list[Rule] = []
        self.facts: dict[str, Fact] = dict()
        self.graph: Node = Node('Root')

    def build(self, rules: list[list]):
        graph = Node('Root')
        rules = sorted(rules, key=lambda x: len(x[2]))
        for rule in rules:
            conditions, operator, conclusions = rule
            rule_node = Rule(rule)

            rule_node.conditions = self.process_expressions(conditions)
            rule_node.facts_in_conditions = {rule_node.conditions} if isinstance(rule_node.conditions, Fact) else copy(rule_node.conditions.facts)

            rule_node.conclusions = self.process_expressions(conclusions)
            rule_node.facts_in_conclusions = {rule_node.conclusions} if isinstance(rule_node.conclusions, Fact) else copy(rule_node.conclusions.facts)

            for fact in rule_node.facts_in_conclusions:
                fact.parents.append(rule_node)

            self.rules.append(rule_node)
            graph.children.append(rule_node)

            if operator == '<=>':
                rule_node = Rule(rule)
                rule_node.conditions = self.process_expressions(conclusions)
                rule_node.facts_in_conditions = {rule_node.conditions} if isinstance(rule_node.conditions, Fact) else copy(rule_node.conditions.facts)

                rule_node.conclusions = self.process_expressions(conditions)
                rule_node.facts_in_conclusions = {rule_node.conclusions} if isinstance(rule_node.conclusions, Fact) else copy(rule_node.conclusions.facts)

                for fact in rule_node.facts_in_conclusions:
                    fact.parents.append(rule_node)

                self.rules.append(rule_node)
                graph.children.append(rule_node)

        self.graph = graph
        self.facts = dict(sorted(self.facts.items(), key=lambda x: x[0]))

    def process_expressions(self, conditions) -> Fact | Operator:
        if isinstance(conditions, list):
            operator = Operator(next((item for item in conditions if item in ['+', '|', '^', '!']), None), conditions)
            operator.children = [self.process_expressions(c) for c in conditions if c not in ['+', '|', '^', '!']]
            for child in operator.children:
                if isinstance(child, Fact):
                    operator.facts.add(child)
                else:
                    operator.facts = operator.facts.union(child.facts)
            print([c.name for c in operator.facts])
            return operator
        else:
            fact = self.get_fact(conditions)
            return fact

    def get_fact(self, token: str) -> Fact:
        if token not in self.facts:
            self.facts[token] = Fact(token)
        return self.facts[token]

    def print(self):
        node = self.graph
        if node is None:
            return
        G = nx.DiGraph()
        G.add_node(node.name)
        self.__dfs(node, G)
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True, arrows=True, font_size=8)
        plt.show()

    def __dfs(self, node, graph) -> list[list[str]]:
        current_level: list[str] = []
        sub_levels: list[list[str]] = []
        if isinstance(node, Rule):
            children = [c for c in [node.conditions, node.conclusions] if c is not None]
        else:
            children = node.children
        for child in children:
            graph.add_edge(node.name, child.name)
            current_level.append(child.name or '???')
            child_sub_levels = self.__dfs(child, graph)
            for level, child_sub_level in enumerate(child_sub_levels):
                if len(sub_levels) <= level:
                    sub_levels.append([])
                sub_levels[level].extend(child_sub_level)
        for parent in node.parents:
            graph.add_edge(node.name, parent.name)
        return [current_level] + sub_levels
