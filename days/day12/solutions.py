import logging

from utils import read_problem_input

UNKNOWN = "?"
DAMAGED = "#"
WORKING = "."


logger = logging.getLogger("day12")


def get_minimum_len(damaged: list[int]) -> int:
    return sum(damaged) + len(damaged) - 1


def _count_arrangements(row: str, damaged: list[int], sln: str = "") -> int:
    """Recursively iterates and returns the number of valid arrangements"""
    if not damaged:
        if not any(c == DAMAGED for c in row):
            logger.debug("solution: " + sln + "." * len(row))
        return 0 if any(c == DAMAGED for c in row) else 1

    if row[0] == DAMAGED:
        return 0

    row = row[1:]  # remove minimum 1 working gap
    total_arrangements = 0

    for i in range(0, len(row) - get_minimum_len(damaged) + 1):
        if any(c == WORKING for c in row[i : i + damaged[0]]):
            if row[i] == DAMAGED:
                break  # the first damage entry must align with a damaged section so we stop after processing it
            else:
                continue

        sln += WORKING

        next_row = row[i + damaged[0] :]
        next_damaged = damaged[1:]
        next_sln = sln + DAMAGED * damaged[0]
        total_arrangements += _count_arrangements(next_row, next_damaged, next_sln)

        if row[i] == DAMAGED:
            break  # the first damage entry must align with a damaged section so we stop after processing it

    return total_arrangements


def count_arrangements(row: str, damaged: list[int]) -> int:
    """Returns the number of valid arrangements given a row and the damaged record"""
    logger.debug(f"Row: {row} | Damaged: {damaged}")

    # Simplify left side
    while row and row[0] != UNKNOWN:
        if row[0] == WORKING:
            row = row.lstrip(WORKING)

        if row[0] == DAMAGED:
            # known damage at the edges must match the edge of the tuple
            row = row[damaged[0] :]
            damaged = damaged[1:]

            if damaged:
                row = row[1:]  # remove minimum 1 working gap

    # Simplify right side
    while row and row[-1] != UNKNOWN:
        if row[-1] == WORKING:
            row = row.rstrip(WORKING)

        if row[-1] == DAMAGED:
            # known damage at the edges must match the edge of the tuple
            row = row[: damaged[-1] * -1]
            damaged = damaged[:-1]

            if damaged:
                row = row[:-1]  # remove minimum 1 working gap

    row = f"{WORKING}{row}"
    count = _count_arrangements(row, damaged)

    logger.debug(f"Total arrangements: {count}")
    return count


def parse_input(raw_lines: list[str]) -> list[tuple[str, list[int]]]:
    return [
        (line.split(" ")[0], [int(x) for x in line.split(" ")[1].split(",")])
        for line in raw_lines
    ]


def part_1() -> str:
    data = parse_input(read_problem_input())
    total_possible_arrangements = sum(
        count_arrangements(row, damaged) for row, damaged in data
    )
    return str(total_possible_arrangements)


def part_2() -> str: ...
