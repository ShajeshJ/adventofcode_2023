from dataclasses import dataclass
from utils import read_problem_input


def is_symbol(c: str) -> bool:
    """Returns True if the character is a schematic symbol, False otherwise."""
    return c != "." and not c.isdigit()


def next_to_symbol(schematic: list[str], i: int, sj: int, ej: int) -> bool:
    """Returns True if the given range of characters is next to a symbol"""

    # check row above the range
    if any(is_symbol(c) for c in schematic[i-1][sj-1:ej+2]):
        return True

    # check row below the range
    if any(is_symbol(c) for c in schematic[i+1][sj-1:ej+2]):
        return True

    # check the sides
    if is_symbol(schematic[i][sj-1]) or is_symbol(schematic[i][ej+1]):
        return True

    return False


def part_1() -> str:
    schematic = [f".{line}." for line in read_problem_input()]
    schematic.insert(0, "." * len(schematic[0]))
    schematic.append("." * len(schematic[0]))
    num_builder = ""
    sum = 0

    for i, line in enumerate(schematic):
        for j, c in enumerate(line):
            if c.isdigit():
                num_builder += c
                continue

            if num_builder and next_to_symbol(schematic, i, j-len(num_builder), j-1):
                sum += int(num_builder)

            num_builder = ""

    return str(sum)


def part_2() -> str:
    raise NotImplementedError()
