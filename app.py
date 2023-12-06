from collections import OrderedDict
import typing as t
import importlib
import importlib.resources as ilr

import days


@t.runtime_checkable
class Solutions(t.Protocol):
    def part_1(self) -> str:
        ...

    def part_2(self) -> str:
        ...


_day_dir_names = [d.name for d in ilr.files(days).iterdir() if d.name.startswith("day")]
_day_dir_names.sort()

ALL_DAYS: OrderedDict[int, Solutions] = {}
for day in _day_dir_names:
    day_module = importlib.import_module(f"days.{day}.solutions")
    if isinstance(day_module, Solutions):
        ALL_DAYS[int(day[3:])] = day_module
    else:
        print(f"skipping {day} because it doesn't implement Solutions")


def run_solution(solution: Solutions, part_num: t.Literal[1, 2]) -> None:
    if part_num == 1:
        print(f"Part 1: {solution.part_1()}")
    else:
        print(f"Part 2: {solution.part_2()}")


def main() -> None:
    print(f"Days with solutions: {", ".join(str(day) for day in ALL_DAYS)}\n")

    solution = None
    while not solution:
        try:
            solution = ALL_DAYS[int(input("Which day would you like to run? "))]
        except (ValueError, KeyError):
            print("Invalid day. Try again\n")

    part_num = None
    while not part_num:
        if (val := input("Would you like to run part 1 or 2? ")) in ["1", "2"]:
            part_num = int(val)
        else:
            print("Invalid part. Try again\n")

    run_solution(solution, part_num)


if __name__ == "__main__":
    main()
