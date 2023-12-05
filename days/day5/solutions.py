from dataclasses import dataclass
from utils import read_problem_input


@dataclass
class TranslationMap:
    source: int
    destination: int
    length: int

    def __contains__(self, item: int) -> bool:
        return item >= self.source and item < self.source + self.length

    def translate(self, item: int) -> int:
        """Translate a given item from source to destination

        Warning: This function assumes you've checked the item is in the source range
        """
        return self.destination + (item - self.source)


def parse_maps(lines: list[str]) -> tuple[list[str], list[TranslationMap]]:
    maps: list[TranslationMap] = []
    while lines and lines[0]:
        destination, source, length = lines.pop(0).split(" ")
        maps.append(TranslationMap(int(source), int(destination), int(length)))

    if len(lines) > 1:
        lines = lines[1:]

    return lines, maps


def part_1() -> str:
    lines = read_problem_input()
    seeds = [int(s) for s in lines.pop(0).replace("seeds: ", "").split(" ")]
    lines = lines[2:]

    while len(lines) > 0:
        lines, translation_maps = parse_maps(lines)
        next_seeds: list[int] = []
        for seed in seeds:
            for m in translation_maps:
                if seed in m:
                    next_seeds.append(m.translate(seed))
                    break
            else:
                next_seeds.append(seed)
        seeds = next_seeds
        lines = lines[1:]

    return str(min(seeds))


def process_seed_ranges(seed_ranges: list[tuple[int, int]], translation_maps: list[TranslationMap]) -> list[tuple[int, int]]:
    """Process a list of seed ranges using a list of translation maps"""
    next_ranges: list[tuple[int, int]] = []
    range_stack = list(seed_ranges)

    while range_stack:
        seed_range = range_stack.pop(0)
        for m in translation_maps:
            if seed_range[0] in m and seed_range[1] in m:
                # Full range is translatable by m
                next_ranges.append((m.translate(seed_range[0]), m.translate(seed_range[1])))
                break
            elif seed_range[0] in m:
                # Only first half of range can be translated by m
                next_ranges.append((m.translate(seed_range[0]), m.destination + m.length - 1))
                range_stack.append((m.source + m.length, seed_range[1]))
                break
            elif seed_range[1] in m:
                # Only second half of range can be translated by m
                next_ranges.append((m.destination, m.translate(seed_range[1])))
                range_stack.append((seed_range[0], m.source - 1))
                break
        else:
            # The entire range is not contained in any map
            next_ranges.append(seed_range)

    return next_ranges


def part_2() -> str:
    lines = read_problem_input()
    seeds_strs = lines.pop(0).replace("seeds: ", "").split(" ")

    # Parse seeds into tuples of [start, end] inclusively for each seed range
    init_seeds: list[tuple[int, int]] = []
    for start, num_seeds in zip(seeds_strs[::2], seeds_strs[1::2]):
        init_seeds.append((int(start), int(start) + int(num_seeds) - 1))
    lines = lines[2:]

    # Parse list of translation maps for each layer of translations
    mapset_groups: list[list[TranslationMap]] = []
    while len(lines) > 0:
        lines, translation_maps = parse_maps(lines)
        mapset_groups.append(translation_maps)
        lines = lines[1:]

    final_locs: list[tuple[int, int]] = []

    for init_seed in init_seeds:
        next_seeds = [init_seed]

        for translation_maps in mapset_groups:
            next_seeds = process_seed_ranges(next_seeds, translation_maps)

        final_locs.extend(next_seeds)

    return str(min([loc[0] for loc in final_locs]))
