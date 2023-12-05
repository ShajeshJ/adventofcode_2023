from dataclasses import dataclass
from utils import read_problem_input


@dataclass
class TranslationMap:
    source: int
    destination: int
    length: int

    def __contains__(self, item: int) -> bool:
        return item in range(self.source, self.source + self.length)

def parse_maps(lines: list[str]) -> tuple[list[str], list[TranslationMap]]:
    maps: list[TranslationMap] = []
    while lines and lines[0]:
        destination, source, length = lines.pop(0).split(" ")
        maps.append(TranslationMap(int(source), int(destination), int(length)))

    if len(lines) > 1:
        lines = lines[1:]

    return lines, maps


def part_1():
    lines = read_problem_input()
    seeds = [int(s) for s in lines.pop(0).replace("seeds: ", "").split(" ")]
    lines = lines[2:]
    
    while len(lines) > 0:
        lines, translation_maps = parse_maps(lines)
        next_seeds: list[int] = []
        for seed in seeds:
            for m in translation_maps:
                if seed in m:
                    next_seeds.append(m.destination + (seed - m.source))
                    break
            else:
                next_seeds.append(seed)
        seeds = next_seeds
        lines = lines[1:]

    return str(min(seeds))

def part_2():
    raise NotImplementedError()
