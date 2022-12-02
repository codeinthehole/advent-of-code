import enum
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


class Choice(enum.Enum):
    ROCK = enum.auto()
    PAPER = enum.auto()
    SCISSORS = enum.auto()


# Helpers


def _player_choices(lines: list[str]) -> Iterator[tuple[Choice, Choice]]:
    """
    Convert the data lines to an iterator of player moves where:

        A = X = rock
        B = Y = paper
        C = Z = scissors

    and the second column specifies player two's move.
    """
    for line in lines:
        parts = line.split()
        p1 = {
            "A": Choice.ROCK,
            "B": Choice.PAPER,
            "C": Choice.SCISSORS,
        }[parts[0]]
        p2 = {
            "X": Choice.ROCK,
            "Y": Choice.PAPER,
            "Z": Choice.SCISSORS,
        }[parts[1]]

        yield p1, p2


def _result_choices(lines: list[str]) -> Iterator[tuple[Choice, Choice]]:
    """
    Convert the lines to an iterator of player moves where:

        A = X = rock
        B = Y = paper
        C = Z = scissors

    and the second column specifies the result.
    """
    for line in lines:
        parts = line.split()
        p1 = {
            "A": Choice.ROCK,
            "B": Choice.PAPER,
            "C": Choice.SCISSORS,
        }[parts[0]]

        # Map the second column to a function that picks the right move.
        p2 = {"X": _losing_move, "Y": _drawing_move, "Z": _winning_move}[parts[1]](p1)

        yield p1, p2


def _line_scores(
    lines: list[str], choice_fn: Callable[[list[str]], Iterator[tuple[Choice, Choice]]]
) -> Iterator[int]:
    """
    Return an iterator of scores for each line.
    """
    for p1, p2 in choice_fn(lines):
        yield _choice_score(p2) + _result_score(p1, p2)


def _choice_score(choice: Choice) -> int:
    return {
        Choice.ROCK: 1,
        Choice.PAPER: 2,
        Choice.SCISSORS: 3,
    }[choice]


def _result_score(p1: Choice, p2: Choice) -> int:
    if _is_p2_win(p1, p2):
        return 6
    elif _is_draw(p1, p2):
        return 3
    else:
        return 0


# Map each choice to a tuple of (beats, loses).
RESULT_MATRIX = {
    Choice.ROCK: (Choice.SCISSORS, Choice.PAPER),
    Choice.PAPER: (Choice.ROCK, Choice.SCISSORS),
    Choice.SCISSORS: (Choice.PAPER, Choice.ROCK),
}


def _is_p2_win(p1: Choice, p2: Choice) -> bool:
    return p2 == _winning_move(p1)


def _is_draw(p1: Choice, p2: Choice) -> bool:
    return p1 == p2


def _losing_move(p1: Choice) -> Choice:
    return RESULT_MATRIX[p1][0]


def _drawing_move(p1: Choice) -> Choice:
    return p1


def _winning_move(p1: Choice) -> Choice:
    return RESULT_MATRIX[p1][1]


EXAMPLE_DATA = [
    "A Y",
    "B X",
    "C Z",
]


class TestPart1:
    def test_example_data(self):
        assert part1(EXAMPLE_DATA) == 15


class TestChoiceScore:
    def test_scores_are_correct(self):
        assert _choice_score(Choice.ROCK) == 1
        assert _choice_score(Choice.PAPER) == 2
        assert _choice_score(Choice.SCISSORS) == 3


class TestResultScore:
    def test_winning_results(self):
        assert _result_score(Choice.ROCK, Choice.PAPER) == 6
        assert _result_score(Choice.PAPER, Choice.SCISSORS) == 6
        assert _result_score(Choice.SCISSORS, Choice.ROCK) == 6


class TestPart2:
    def test_example_data(self):
        assert part2(EXAMPLE_DATA) == 12


if __name__ == "__main__":
    # Run tests
    assert pytest.main([__file__, "-v"]) == 0

    # Run with real data (inferred from filename).
    print("Part one: ", part1(aocd.lines))
    print("Part two: ", part2(aocd.lines))
