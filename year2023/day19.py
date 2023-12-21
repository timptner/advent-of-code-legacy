import math

from enum import Enum

from utilities.backend import BasePuzzle


class Category(Enum):
    EXTREMELY_COOL_LOOKING = 'x'
    MUSICAL = 'm'
    AERODYNAMIC = 'a'
    SHINY = 's'


class Part:
    def __init__(self, line: str) -> None:
        self.categories = {}
        for item in line[1:-1].split(','):
            category, rating = item.split('=')
            category = Category(category)
            self.categories[category] = int(rating)

    def total(self) -> int:
        return sum(self.categories.values())


class Workflow:
    def __init__(self, line: str) -> None:
        name, rules = line.split('{')
        self.name = name

        rules = rules[:-1].split(',')

        self.rules = []
        for rule in rules[:-1]:
            condition, result = rule.split(':')
            if '<' in condition:
                operation = self.is_less_than
                category, value = condition.split('<')
            else:
                operation = self.is_greater_than
                category, value = condition.split('>')
            category = Category(category)
            value = int(value)
            rule = (category, operation, value, result)
            self.rules.append(rule)
        self.rules.append(rules[-1])

    def __repr__(self) -> str:
        return f"Workflow({self.name})"

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def is_less_than(value, rating) -> bool:
        return value < rating

    @staticmethod
    def is_greater_than(value, rating) -> bool:
        return value > rating

    def apply(self, part: Part) -> str:
        for rule in self.rules[:-1]:
            category, operation, value, result = rule
            rating = part.categories[category]
            if operation(rating, value):
                return result
        return self.rules[-1]


def make_rules_independent(workflows: dict) -> dict:
    improved_workflows = {}
    for name, rules in workflows.items():
        next_names, conditions = zip(*rules)
        new_rules = []
        for index, next_name in enumerate(next_names):
            new_conditions = []
            condition = conditions[index]
            if condition:
                new_conditions.append(condition)
            for condition in conditions[:index]:
                if '>' in condition:
                    condition = condition.replace('>', '<=')
                else:
                    condition = condition.replace('<', '>=')
                new_conditions.append(condition)
            rule = next_name, new_conditions
            new_rules.append(rule)
        improved_workflows[name] = new_rules
    return improved_workflows


def parse_data(text: str) -> tuple[dict, list]:
    groups = text.split('\n\n')

    workflows = {}
    for workflow in groups[0].splitlines():
        name, rules_str = workflow[:-1].split('{')
        rules = []
        for rule in rules_str.split(','):
            if ':' in rule:
                condition, next_name = rule.split(':')
            else:
                condition = None
                next_name = rule
            rules.append((next_name, condition))
        workflows[name] = rules

    workflows = make_rules_independent(workflows)

    parts = []
    for part in groups[1].splitlines():
        part = {key: int(value) for key, value in [category.split('=') for category in part[1:-1].split(',')]}
        parts.append(part)

    return workflows, parts


class Tree:
    def __init__(self, workflows: dict) -> None:
        self.workflows = workflows
        self.accepted = []

    def build(self, name: str, previous_conditions: list) -> None:
        rules = self.workflows[name]
        for next_name, conditions in rules:
            next_conditions = previous_conditions + conditions
            if next_name in ['A', 'R']:
                if next_name == 'A':
                    self.accepted.append(next_conditions)
                continue

            self.build(next_name, next_conditions)


class Puzzle(BasePuzzle):
    year = 2023
    day = 19
    name = "Aplenty"

    @property
    def test_data(self) -> dict:
        text = """
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}
        
        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """
        return {
            'part1': (text, 19114),
            'part2': (text, 167409079868000),
        }

    def part1(self, text: str) -> int:
        workflows, parts = text.split('\n\n')

        workflows = [Workflow(line) for line in workflows.splitlines()]
        workflows = {str(workflow): workflow for workflow in workflows}

        parts = [Part(part) for part in parts.splitlines()]

        results = {}
        for part in parts:
            value = 'in'
            while value not in ['A', 'R']:
                value = workflows[value].apply(part)
            if value == 'R':
                results[part] = value
            else:
                results[part] = value

        total = 0
        for part, value in results.items():
            if value == 'R':
                continue
            total += part.total()

        return total

    def part2(self, text: str) -> int:
        workflows, parts = parse_data(text)
        tree = Tree(workflows)
        tree.build('in', [])
        total = 0
        for conditions in tree.accepted:
            rating = {
                'x': (1, 4000),
                'm': (1, 4000),
                'a': (1, 4000),
                's': (1, 4000),
            }
            for condition in conditions:
                if '=' in condition:
                    if '>=' in condition:
                        category, value = condition.split('>=')
                        value = int(value)
                        start, end = rating[category]
                        if start < value:
                            start = value
                        rating[category] = start, end
                    else:
                        category, value = condition.split('<=')
                        value = int(value)
                        start, end = rating[category]
                        if end > value:
                            end = value
                        rating[category] = start, end
                else:
                    if '>' in condition:
                        category, value = condition.split('>')
                        value = int(value)
                        start, end = rating[category]
                        if start <= value:
                            start = value + 1
                        rating[category] = start, end
                    else:
                        category, value = condition.split('<')
                        value = int(value)
                        start, end = rating[category]
                        if end >= value:
                            end = value - 1
                        rating[category] = start, end

            rating = {key: end + 1 - start for key, (start, end) in rating.items()}
            total += math.prod(rating.values())
        return total
