import typing as t

class Solutions(t.Protocol):
    def part_1(self) -> str:
        ...

    def part_2(self) -> str:
        ...


import days.day1.solutions as day1
ALL_DAYS: dict[int, Solutions] = {
    1: day1,
}

def run_solution(solution: Solutions, part_num: t.Literal[1, 2]) -> None:
    if part_num == 1:
        print(f"Part 1: {solution.part_1()}")
    else:
        print(f"Part 2: {solution.part_2()}")


def main() -> None:
    solution = None
    while not solution:
        try:
            solution = ALL_DAYS[int(input("Which day would you like to run? "))]
        except (ValueError, KeyError):
            print("Invalid day number. Try again\n")

    part_num = None
    while not part_num:
        match val := input("Would you like to run part 1 or 2? "):
            case "1" | "2":
                part_num = int(val)
            case _:
                print("Invalid part number. Try again\n")

    run_solution(solution, part_num)


if __name__ == "__main__":
    main()
