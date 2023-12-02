from dataclasses import dataclass
import re
from typing import Self
from utils import read_problem_input

@dataclass
class Round:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __gt__(self, other: "Round") -> bool:
        return self.red > other.red or self.blue > other.blue or self.green > other.green

    def __le__(self, other: "Round") -> bool:
        return self.red <= other.red and self.blue <= other.blue and self.green <= other.green

@dataclass
class Game:
    id: int
    rounds: list[Round]

    @classmethod
    def from_str(cls: type[Self], game_str: str) -> Self:
        id_str, rounds_str = game_str.removeprefix("Game ").split(":", 1)

        rounds_str_list = rounds_str.replace(" ", "").strip().split(";")
        rounds: list[Round] = []

        for round_str in rounds_str_list:
            colors: dict[str, int] = {}
            for color in ["red", "blue", "green"]:
                match = re.search(rf"(\d+){color}", round_str)
                if match:
                    colors[color] = int(match.group(1))
            rounds.append(Round(**colors))

        return cls(int(id_str), rounds)


def part_1() -> str:
    games = (Game.from_str(game_str) for game_str in read_problem_input())
    max_cubes = Round(12, 13, 14)

    id_sum = 0
    for game in games:
        if all(round <= max_cubes for round in game.rounds):
            id_sum += game.id

    return str(id_sum)


def part_2() -> str:
    games = (Game.from_str(game_str) for game_str in read_problem_input())

    power_sum = 0
    for game in games:
        max_red = max(round.red for round in game.rounds)
        max_blue = max(round.blue for round in game.rounds)
        max_green = max(round.green for round in game.rounds)
        power_sum += max_red * max_blue * max_green

    return str(power_sum)
