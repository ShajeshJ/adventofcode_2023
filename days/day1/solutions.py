from utils import read_problem_input

def part_1() -> str:
    lines = read_problem_input()
    total = 0

    for line in lines:
        num_str = next(n for n in line if n.isdigit()) + next(n for n in reversed(line) if n.isdigit())
        total += int(num_str)

    return str(total)


def part_2() -> str:
    lines = read_problem_input()
    total = 0
    valid_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    for line in lines:
        numeric_line = ""

        for i, c in enumerate(line):
            if c.isdigit():
                numeric_line += c
                continue

            for word, value in valid_words.items():
                if line[0:i+1].endswith(word):
                    numeric_line += str(value)
                    break

        total += int(numeric_line[0] + numeric_line[-1])

    return str(total)
