# Based on the problem description, we can derive the equations:
# time_held + time_ran = total_time
# time_held * time_ran > distance_to_beat
#
# These can be rearranged into a quadratic equation solving for time_held.
# Solving for the zeroes will give you the lower/upper bounds:
#   lowerbound > (-t + sqrt(t^2-4d)) / -2
#   upperbound < (-t - sqrt(t^2-4d)) / -2
# where t is the total time and d is the distance to beat.

import math
import re
from utils import read_problem_input


def calculate_bounds(t: int, d: int) -> tuple[int, int]:
    lowerbound = math.ceil((-t + (t**2 - 4*d)**0.5) / -2)
    upperbound = math.floor((-t - (t**2 - 4*d)**0.5) / -2)
    return (lowerbound, upperbound)


def part_1() -> str:
    time_str, dist_str = read_problem_input()
    times = [int(time) for time in re.findall(r'\d+', time_str)]
    distances = [int(time) for time in re.findall(r'\d+', dist_str)]

    product = 1

    for t, d in zip(times, distances):
        lbound, ubound = calculate_bounds(t, d)
        product *= ubound - lbound + 1

    return str(product)

def part_2() -> str:
    time_str, dist_str = read_problem_input()
    t = int(time_str.replace(" ", "").split(":")[1])
    d = int(dist_str.replace(" ", "").split(":")[1])
    lbound, ubound = calculate_bounds(t, d)
    return str(ubound - lbound + 1)
