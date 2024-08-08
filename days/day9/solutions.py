from collections.abc import Generator
import itertools

from utils import read_problem_input


def get_historical_values() -> Generator[list[int]]:
    for line in read_problem_input():
        yield [int(n) for n in line.split(" ")]


def get_differences(values: list[int]) -> list[int]:
    return [values[i] - values[i - 1] for i in range(1, len(values))]


def predict_next_value(values: list[int]) -> int:
    sum_of_lasts = values[-1]
    differences = get_differences(values)

    while any(n != 0 for n in differences):
        sum_of_lasts += differences[-1]
        differences = get_differences(differences)

    return sum_of_lasts


def part_1() -> str:
    return str(sum(predict_next_value(values) for values in get_historical_values()))


def predict_prev_value(values: list[int]) -> int:
    # To predict previous values, we alternative sum / difference of the first values
    # e.g. a - b + c - d ...
    sum_and_diff_of_firsts = values[0]
    operation = itertools.cycle([lambda a, b: a - b, lambda a, b: a + b])
    differences = get_differences(values)

    while any(n != 0 for n in differences):
        combine = next(operation)
        sum_and_diff_of_firsts = combine(sum_and_diff_of_firsts, differences[0])
        differences = get_differences(differences)

    return sum_and_diff_of_firsts


def part_2() -> str:
    return str(sum(predict_prev_value(values) for values in get_historical_values()))
