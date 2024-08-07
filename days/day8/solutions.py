import itertools
import math
from dataclasses import dataclass
from functools import cached_property

from utils import read_problem_input


@dataclass
class Node:
    name: str
    children: tuple[str, str]

    @cached_property
    def last_char(self) -> str:
        return self.name[-1]


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

    cur_node = node_table["AAA"]

    for dir, steps in zip(itertools.cycle(instructions), itertools.count(1)):
        cur_node = node_table[cur_node.children[dir]]
        if cur_node.name == "ZZZ":
            return str(steps)


def nav_path_simultaneously(
    node_table: dict[str, Node], instructions: list[int]
) -> set[int]:
    """Simultaneously traverses all paths from **A to **Z and returns the lengths of each path."""

    path_lens: set[int] = set()
    current_nodes: set[str] = {
        node.name for node in node_table.values() if node.last_char == "A"
    }

    for dir, steps in zip(itertools.cycle(instructions), itertools.count()):
        next_nodes: set[str] = set()
        for node_name in current_nodes:
            node = node_table[node_name]

            if node.last_char == "Z":
                path_lens.add(steps)
                continue

            next_nodes.add(node.children[dir])

        if not next_nodes:
            return path_lens

        current_nodes = next_nodes


def part_2() -> str:
    lines = read_problem_input()
    instructions = [0 if c == "L" else 1 for c in lines.pop(0)]
    node_table = parse_node_lookup(lines[1:])

    path_lens = nav_path_simultaneously(node_table, instructions)
    return str(math.lcm(*path_lens))
