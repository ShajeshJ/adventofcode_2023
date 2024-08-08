from dataclasses import dataclass
import itertools
from typing import Any, NamedTuple, Self

from utils import read_problem_input

type Dir = tuple[int, int]
type Point = tuple[int, int]


NORTH: Dir = (-1, 0)
EAST: Dir = (0, 1)
SOUTH: Dir = (1, 0)
WEST: Dir = (0, -1)


@dataclass
class Pipe:
    sides: tuple[Dir]

    def get_exit(self, entry: Dir) -> Dir:
        if entry == (self.sides[0][0] * -1, self.sides[0][1] * -1):
            return self.sides[1]
        elif entry == (self.sides[1][0] * -1, self.sides[1][1] * -1):
            return self.sides[0]
        else:
            raise ValueError("Invalid entry direction")


PIPES: dict[str, Pipe] = {
    "|": Pipe((NORTH, SOUTH)),
    "-": Pipe((EAST, WEST)),
    "L": Pipe((NORTH, EAST)),
    "J": Pipe((NORTH, WEST)),
    "7": Pipe((SOUTH, WEST)),
    "F": Pipe((SOUTH, EAST)),
}


def get_starting_point(char_map: list[str]) -> Point:
    """Returns the starting point of the map, ordered [y, x]"""
    for y, line in enumerate(char_map):
        x = line.find("S")
        if x != -1:
            return y, x
    raise ValueError("Starting point not found")


def get_path(char_map: list[str]) -> list[Point]:
    sy, sx = get_starting_point(char_map)
    path: list[Point] = [(sy, sx)]

    # test input shows the start is in the middle
    # so we skip bound checking
    if char_map[sy - 1][sx] in ("|", "7", "F"):
        next_move = NORTH
    elif char_map[sy + 1][sx] in ("|", "L", "J"):
        next_move = SOUTH
    else:
        # we can assume S is a "-", and pick EAST arbitrarily
        next_move = EAST

    cy = sy + next_move[0]
    cx = sx + next_move[1]

    while cy != sy or cx != sx:
        path.append((cy, cx))
        cur_pipe = PIPES[char_map[cy][cx]]

        next_move = cur_pipe.get_exit(next_move)
        cy += next_move[0]
        cx += next_move[1]

    return path


def part_1() -> str:
    char_map = read_problem_input()
    path = get_path(char_map)
    return str(len(path) // 2)


def get_pipe(sides: tuple[Dir, Dir]) -> str:
    """Given the two connecting directions, return the pipe character"""
    for ch, pipe in PIPES.items():
        if sides == pipe.sides or sides == pipe.sides[::-1]:
            return ch

    raise ValueError("no matching pipe")


def upscale_times_3(char_map: list[str]) -> list[str]:
    new_map: list[str] = []

    for row in char_map:
        new_map.extend(["", "", ""])
        for ch in row:
            if ch == ".":
                new_map[-3] += "..."
                new_map[-2] += "..."
                new_map[-1] += "..."
            elif ch == "o":
                new_map[-3] += "ooo"
                new_map[-2] += "ooo"
                new_map[-1] += "ooo"
            elif ch == "|":
                new_map[-3] += ".|."
                new_map[-2] += ".|."
                new_map[-1] += ".|."
            elif ch == "-":
                new_map[-3] += "..."
                new_map[-2] += "---"
                new_map[-1] += "..."
            elif ch == "L":
                new_map[-3] += ".|."
                new_map[-2] += ".L-"
                new_map[-1] += "..."
            elif ch == "J":
                new_map[-3] += ".|."
                new_map[-2] += "-J."
                new_map[-1] += "..."
            elif ch == "7":
                new_map[-3] += "..."
                new_map[-2] += "-7."
                new_map[-1] += ".|."
            elif ch == "F":
                new_map[-3] += "..."
                new_map[-2] += ".F-"
                new_map[-1] += ".|."
            else:
                raise ValueError(f"Unknown character {ch}")

    return new_map


def flood_connecting_ground(char_map: list[str], y: int, x: int) -> list[str]:
    """Flood fills connecting ground tiles with 'o's"""
    edge_stack: list[Point] = [(y, x)]
    char_map[y] = char_map[y][:x] + "o" + char_map[y][x + 1 :]
    row_len = len(char_map[0])

    while edge_stack:
        cur_y, cur_x = edge_stack.pop()

        for dy, dx in (NORTH, EAST, SOUTH, WEST):
            new_y, new_x = cur_y + dy, cur_x + dx
            if (
                0 <= new_y < len(char_map)
                and 0 <= new_x < row_len
                and char_map[new_y][new_x] == "."
            ):
                char_map[new_y] = (
                    char_map[new_y][:new_x] + "o" + char_map[new_y][new_x + 1 :]
                )
                edge_stack.append((new_y, new_x))

    return char_map


def downscale_times_3(char_map: list[str]) -> list[str]:
    new_map: list[str] = []
    row_len = len(char_map[0])

    for _, middle_line, _ in itertools.batched(char_map, 3):
        # due to the way upscaling works, we can always assume the middle character
        # in the 3x3 is equivalent to the downscaled version
        new_row = "".join(middle_line[x + 1] for x in range(0, row_len, 3))
        new_map.append(new_row)

    return new_map


def part_2() -> str:
    char_map = read_problem_input()
    path = get_path(char_map)

    # replace S with its pipe character
    sy, sx = path[0]
    side1: Dir = path[1][0] - sy, path[1][1] - sx
    side2: Dir = path[-1][0] - sy, path[-1][1] - sx
    char_map[sy] = char_map[sy].replace("S", get_pipe((side1, side2)))

    # Convert all tiles not along the path to ground characters
    for row in range(len(char_map)):
        char_map[row] = "".join(
            ch if (row, col) in path else "." for col, ch in enumerate(char_map[row])
        )

    # triple the resolution so we can path find between the pipes
    char_map = upscale_times_3(char_map)

    # tripling the resolution inadvertently adds a '.' padding around the map
    # so we can assume (0, 0) is outside, and all of the outside is interconnected
    char_map = flood_connecting_ground(char_map, 0, 0)

    char_map = downscale_times_3(char_map)

    return str(sum(row.count(".") for row in char_map))
