from dataclasses import dataclass


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


@dataclass
class Score:
    errors: list[str]

    def __post_init__(self):
        self.corrupted = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137,
        }
        self.incomplete = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4,
        }

    @property
    def corrupted_score(self) -> int:
        return sum(self.corrupted[e] for e in self.errors)

    @property
    def incomplete_score(self) -> int:
        score: list[int] = []
        for line in self.errors:
            line_score = 0
            for c in line:
                line_score = line_score * 5 + self.incomplete[c]
            score.append(line_score)

        score.sort()
        return score[len(score) // 2]


@dataclass
class LineParser:
    line: str

    def __post_init__(self) -> None:
        self.openers = {"(": ")", "[": "]", "{": "}", "<": ">"}
        self.closers = {")": "(", "]": "[", "}": "{", ">": "<"}

    def find_corrupted(self) -> list[str]:
        characters: list[str] = list(self.line)
        open_chars: list[str] = []
        corrupted: list[str] = []

        for c in characters:
            if c in self.openers:
                open_chars.append(c)
                continue
            if open_chars[-1] == self.closers[c]:
                open_chars.pop(-1)
                continue
            corrupted.append(c)

        return corrupted

    def find_incomplete(self) -> str:
        characters: list[str] = list(self.line)
        open_chars: list[str] = []

        for c in characters:
            if c in self.openers:
                open_chars.append(c)
                continue
            if open_chars[-1] == self.closers[c]:
                open_chars.pop(-1)
                continue

        missing_chars = [self.openers[c] for c in open_chars[::-1]]

        return "".join(missing_chars)


def part_1(input_lines: list[str]):
    errors_found: list[str] = []
    for line in input_lines:
        parsed_line = LineParser(line)
        corrupted = parsed_line.find_corrupted()
        if corrupted:
            errors_found += corrupted[0]

    score = Score(errors_found)
    return score.corrupted_score


def part_2(input_lines: list[str]):
    errors_found = []
    for line in input_lines:
        parsed_line = LineParser(line)
        corrupted = parsed_line.find_corrupted()
        if corrupted:
            continue
        errors_found.append(parsed_line.find_incomplete())

    score = Score(errors_found)
    return score.incomplete_score


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
