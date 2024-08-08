import itertools
from utils import read_problem_input

type Coord = tuple[int, int]


type UniverseRow = list[tuple[str, int]]
"""A row in the universe, with consecutive characters compressed into tuples"""

type EmptyUniverseRows = int
"""A count of consecutive empty rows in the universe"""


def get_row_len(row: UniverseRow) -> int:
    return sum(g[1] for g in row)


def get_universe() -> list[UniverseRow]:
    return [
        [(c, len(list(g))) for c, g in itertools.groupby(line)]
        for line in read_problem_input()
    ]


def decompress(universe: list[UniverseRow]) -> list[UniverseRow]:
    """Decompress UniverseRow into individual characters"""
    return [[(c, 1) for c, n in row for _ in range(n)] for row in universe]


def compress(universe: list[UniverseRow]) -> list[UniverseRow]:
    """Compress UniverseRow into its most compact form"""
    return [
        [
            (c, sum(n[1] for n in g))
            for c, g in itertools.groupby(row, key=lambda t: t[0])
        ]
        for row in universe
    ]


def expand(
    universe: list[UniverseRow], factor: int
) -> list[UniverseRow | EmptyUniverseRows]:
    universe = decompress(universe)
    new_universe: list[UniverseRow] = [[] for _ in range(len(universe))]

    # Column expansion
    for x in range(get_row_len(universe[0])):
        col_chars: set[str] = set()

        for y, row in enumerate(universe):
            col_chars.add(row[x][0])
            new_universe[y].append(row[x])

        if col_chars == {"."}:  # Empty column
            for new_row in new_universe:
                new_row[-1] = (new_row[-1][0], factor)

    new_universe = compress(new_universe)

    # Row expansion
    universe = new_universe
    new_universe = []
    empty_row: UniverseRow = [(".", get_row_len(universe[0]))]

    for row in universe:
        if row == empty_row:
            new_universe.append(factor)
        else:
            new_universe.append(row)

    return new_universe


def get_galaxies(universe: list[UniverseRow | EmptyUniverseRows]) -> list[Coord]:
    galaxies: list[Coord] = []
    yskip = 0

    for y, row in enumerate(universe):
        if isinstance(row, int):
            yskip += row - 1
            continue

        x = 0
        for c, n in row:
            if c == "#":
                galaxies.extend((y + yskip, x + i) for i in range(n))
            x += n

    return galaxies


def part_1(factor: int = 2) -> str:
    universe = expand(get_universe(), factor)
    galaxies = get_galaxies(universe)

    shortest_distance_sum = 0

    while galaxies:
        cur = galaxies.pop()
        shortest_distance_sum += sum(
            abs(cur[0] - other[0]) + abs(cur[1] - other[1]) for other in galaxies
        )

    return str(shortest_distance_sum)


def part_2() -> str:
    return part_1(1_000_000)
