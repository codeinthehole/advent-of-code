from typing import Iterator

import aocd
import pytest


def part1(lines: list[str]) -> int:
    return sum(_line_scores(lines))


def _line_scores(lines: list[str]) -> Iterator[int]:
    for p1, p2 in _player_choices(lines):
        yield _choice_score(p2) + _result_score(p1, p2)


def _choice_score(choice: str) -> int:
    return {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }[choice]


def _result_score(p1: str, p2: str) -> int:
    if _is_p2_win(p1, p2):
        return 6
    elif _is_draw(p1, p2):
        return 3
    else:
        return 0


def _is_p2_win(p1: str, p2: str) -> bool:
    return {
        "A": "Y",
        "B": "Z",
        "C": "X",
    }[p1] == p2


def _is_draw(p1: str, p2: str) -> bool:
    return {
        "A": "X",
        "B": "Y",
        "C": "Z",
    }[p1] == p2


def _player_choices(lines):
    for line in lines:
        yield line.split()


def part2(lines: list[str]) -> int:
    return 0


EXAMPLE_DATA = [
    "A Y",
    "B X",
    "C Z",
]


class TestPart1:
    def test_example_data(self):
        assert part1(EXAMPLE_DATA) == 15


class TestPart2:
    pass


if __name__ == "__main__":
    # Run tests
    assert pytest.main([__file__, "-v"]) == 0

    # Run with real data (inferred from filename).
    print("Part one: ", part1(aocd.lines))
    print("Part two: ", part2(aocd.lines))
