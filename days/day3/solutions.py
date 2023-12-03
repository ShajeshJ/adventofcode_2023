from dataclasses import dataclass, field
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


def add_schematic_padding(schematic: list[str]) -> list[str]:
    """Adds padding to the schematic to avoid index out of bounds issues"""
    schematic = [f".{line}." for line in schematic]
    schematic.insert(0, "." * len(schematic[0]))
    schematic.append("." * len(schematic[0]))
    return schematic


def part_1() -> str:
    schematic = add_schematic_padding(read_problem_input())
    num_builder = ""
    total = 0

    for i, line in enumerate(schematic):
        for j, c in enumerate(line):
            if c.isdigit():
                num_builder += c
                continue

            if num_builder and next_to_symbol(schematic, i, j-len(num_builder), j-1):
                total += int(num_builder)

            num_builder = ""

    return str(total)


def is_gear(schematic: list[str], i: int, j: int) -> bool:
    """Returns True if the given position is a gear asterisk"""
    if schematic[i][j] != "*":
        return False

    part_num_count = 0

    # Possible part count configurations above/below:
    # `xNx` or `N$N` where x is anything, N is a digit, and $ is any non-digit
    # these would result in 1 or 2 part numbers respectively
    if schematic[i-1][j].isdigit():
        part_num_count += 1
    elif schematic[i-1][j-1].isdigit() and schematic[i-1][j+1].isdigit():
        part_num_count += 2

    if schematic[i+1][j].isdigit():
        part_num_count += 1
    elif schematic[i+1][j-1].isdigit() and schematic[i+1][j+1].isdigit():
        part_num_count += 2

    # Possible part count configurations left/right:
    if schematic[i][j-1].isdigit():
        part_num_count += 1
    if schematic[i][j+1].isdigit():
        part_num_count += 1

    return part_num_count == 2


@dataclass
class GearMapper:
    schematic: list[str]
    gears: dict[tuple[int, int], list[int]] = field(default_factory=dict)


    def find_all_gears(self) -> dict[tuple[int, int], list[int]]:
        num_builder = ""

        for i, line in enumerate(self.schematic):
            for j, c in enumerate(line):
                if c.isdigit():
                    num_builder += c
                    continue

                if not num_builder:
                    continue

                # update asterisk to the left of the number
                if self.schematic[i][j-len(num_builder)-1] == "*":
                    self.gears.setdefault((i, j-len(num_builder)-1), []).append(int(num_builder))
                if self.schematic[i][j] == "*":
                    self.gears.setdefault((i, j), []).append(int(num_builder))

                # update asterisks above/below the number
                for col in range(j-len(num_builder)-1, j+1):
                    if self.schematic[i-1][col] == "*":
                        self.gears.setdefault((i-1, col), []).append(int(num_builder))
                    if self.schematic[i+1][col] == "*":
                        self.gears.setdefault((i+1, col), []).append(int(num_builder))

                num_builder = ""

        for pos in list(self.gears.keys()):
            if len(self.gears[pos]) != 2:
                del self.gears[pos]

        return self.gears


def part_2() -> str:
    schematic = add_schematic_padding(read_problem_input())

    gearMapper = GearMapper(schematic)
    gears = gearMapper.find_all_gears()

    total = sum(part_nums[0] * part_nums[1] for part_nums in gears.values())
    return str(total)
