import aocd
import pytest


def main(lines: list[str]) -> int:
    largest_total = 0
    for group_sum in _summed_groups(lines):
        largest_total = max(largest_total, group_sum)
    return largest_total


def _summed_groups(lines):
    for group in _groups(lines):
        yield sum(group)


def _groups(lines):
    values = []
    for line in lines:
        if line:
            values.append(int(line))
        else:
            yield values
            values = []
    if values:
        yield values


class TestMain:
    @pytest.mark.parametrize(
        "lines, result, scenario",
        [
            (
                [
                    "1000",
                    "2000",
                    "3000",
                    "",
                    "4000",
                    "",
                    "5000",
                    "6000",
                    "",
                    "7000",
                    "8000",
                    "9000",
                    "",
                    "10000",
                ],
                24000,
                "example",
            ),
        ],
    )
    def test_scenario(self, lines, result, scenario):
        assert main(lines) == result, scenario


if __name__ == "__main__":
    # Run tests
    exit_code = pytest.main([__file__])
    assert exit_code == 0

    # Run with real data (inferred from filename).
    print(main(aocd.lines))
