from utils import read_problem_input

type Coord = tuple[int, int]


def expand(universe: list[str]) -> list[str]:
    new_universe: list[str] = [""] * len(universe)

    # Column expansion
    for x in range(len(universe[0])):
        col_chars: set[str] = set()

        for y, row in enumerate(universe):
            col_chars.add(row[x])
            new_universe[y] += row[x]

        if col_chars == {"."}:  # Empty column
            new_universe = [row + "." for row in new_universe]

    # Row expansion
    universe = new_universe
    new_universe = []
    empty_row = "." * len(universe[0])

    for row in universe:
        new_universe.append(row)
        if row == empty_row:
            new_universe.append(empty_row)

    return new_universe


def get_galaxies(universe: list[str]) -> list[Coord]:
    galaxies: list[Coord] = []
    for y, row in enumerate(universe):
        for x, cell in enumerate(row):
            if cell == "#":
                galaxies.append((y, x))
    return galaxies


def part_1() -> str:
    universe = read_problem_input()
    universe = expand(universe)
    galaxies = get_galaxies(universe)

    shortest_distance_sum = 0

    while galaxies:
        cur = galaxies.pop()
        shortest_distance_sum += sum(
            abs(cur[0] - other[0]) + abs(cur[1] - other[1]) for other in galaxies
        )

    return str(shortest_distance_sum)


def part_2() -> str: ...
