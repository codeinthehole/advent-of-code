from typing import Callable, Iterator

import aocd
import pytest


def part1(lines: list[str]) -> int:
    """
    Calculate score when second column is assumed to be a choice indicator.

    A = X = rock
    B = Y = paper
    C = Z = scissors
    """
    return sum(_line_scores(lines, choice_fn=_player_choices))


def part2(lines: list[str]) -> int:
    """
    Calculate score when second column is the intended result.

    A = rock
    B = paper
    C = scissors
    X = lose
    Y = draw
    Z = win
    """
    return sum(_line_scores(lines, choice_fn=_result_choices))


# Helpers


def _player_choices(lines: list[str]) -> Iterator[tuple[str, str]]:
    """
    Convert the lines to an iterator of player moves where:

        A = X = rock
        B = Y = paper
        C = Z = scissors

    and the second column specifies player two's move.
    """
    for line in lines:
        parts = line.split()
        yield parts[0], parts[1]


def _result_choices(lines: list[str]) -> Iterator[tuple[str, str]]:
    """
    Convert the lines to an iterator of player moves where:

        A = X = rock
        B = Y = paper
        C = Z = scissors

    and the second column specifies the result.
    """
    for line in lines:
        parts = line.split()
        p1, result = parts[0], parts[1]
        if result == "X":
            # Need to pick losing response
            p2 = _losing_move(p1)
        elif result == "Y":
            # Need to draw
            p2 = _drawing_move(p1)
        elif result == "Z":
            # Need to win
            p2 = _winning_move(p1)
        yield p1, p2


def _line_scores(
    lines: list[str], choice_fn: Callable[[list[str]], Iterator[tuple[str, str]]]
) -> Iterator[int]:
    for p1, p2 in choice_fn(lines):
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


def _losing_move(p1: str) -> str:
    return {
        "A": "Z",
        "B": "X",
        "C": "Y",
    }[p1]


def _drawing_move(p1: str) -> str:
    return {
        "A": "X",
        "B": "Y",
        "C": "Z",
    }[p1]


def _winning_move(p1: str) -> str:
    return {
        "A": "Y",
        "B": "Z",
        "C": "X",
    }[p1]


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


EXAMPLE_DATA = [
    "A Y",
    "B X",
    "C Z",
]


class TestPart1:
    def test_example_data(self):
        assert part1(EXAMPLE_DATA) == 15


class TestPart2:
    def test_example_data(self):
        assert part2(EXAMPLE_DATA) == 12


if __name__ == "__main__":
    # Run tests
    assert pytest.main([__file__, "-v"]) == 0

    # Run with real data (inferred from filename).
    print("Part one: ", part1(aocd.lines))
    print("Part two: ", part2(aocd.lines))
