
from dataclasses import dataclass

from utils import read_problem_input


@dataclass
class Node:
    name: str
    children: tuple[str, str]

def parse_node_lookup(lines: list[str]) -> dict[str, Node]:
    lookup: dict[str, Node] = {}

    for line in lines:
        name, children = line.split(" = (")
        left, right = children.split(", ")
        right = right.replace(")", "")
        lookup[name] = Node(name, (left, right))

    return lookup

def part_1() -> str:
    lines = read_problem_input()
    instructions = [0 if c == "L" else 1 for c in lines.pop(0)]
    node_table = parse_node_lookup(lines[1:])

    steps = 0
    cur_node = node_table["AAA"]

    while True:
        for i in instructions:
            steps += 1
            cur_node = node_table[cur_node.children[i]]
            if cur_node.name == "ZZZ":
                return str(steps)

def part_2() -> str:
    raise NotImplementedError()
