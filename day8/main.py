from dataclasses import dataclass


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


@dataclass
class Digit:
    number: int
    name: str
    segments: set[str]

    @property
    def segment_count(self) -> int:
        return len(self.segments)


DIGITS = {
    0: Digit(0, "Zero", {"a", "b", "c", "e", "f", "g"}),
    1: Digit(1, "One", {"c", "f"}),
    2: Digit(2, "Two", {"a", "c", "d", "e", "g"}),
    3: Digit(3, "Three", {"a", "c", "d", "f", "g"}),
    4: Digit(4, "Four", {"b", "c", "d", "f"}),
    5: Digit(5, "Five", {"a", "b", "d", "f", "g"}),
    6: Digit(6, "Six", {"a", "b", "d", "e", "f", "g"}),
    7: Digit(7, "Seven", {"a", "c", "f"}),
    8: Digit(8, "Eight", {"a", "b", "c", "d", "e", "f", "g"}),
    9: Digit(9, "Nine", {"a", "b", "c", "d", "f", "g"}),
}


@dataclass
class ParsedInput:
    unique_signals: list[str]
    output_values: list[str]


def parse_lines(input: list[str]) -> list[ParsedInput]:
    out = []
    for i in input:
        signals, values = i.split("|")
        signals_list = [s for s in signals.split(" ") if s != ""]
        values_list = [v for v in values.split(" ") if v != ""]
        out.append(ParsedInput(signals_list, values_list))
    return out


def part_1(input_lines: list[str]):

    parsed_lines = parse_lines(input_lines)

    out = 0
    unique_segments = [
        DIGITS[1].segment_count,
        DIGITS[4].segment_count,
        DIGITS[7].segment_count,
        DIGITS[8].segment_count,
    ]

    for line in parsed_lines:
        for output in line.output_values:
            if len(output) in (unique_segments):
                out += 1

    return out


@dataclass
class DigitParser:
    parsed_input: ParsedInput

    def __post_init__(self) -> None:
        self.signals = self.parsed_input.unique_signals
        self.values = self.parsed_input.output_values
        self.digit_dict = {i: "" for i in range(10)}
        self.segment_dict = {
            "a": "",
            "b": "",
            "c": "",
            "d": "",
            "e": "",
            "f": "",
            "g": "",
        }

    def find_unique_digits(self) -> None:
        for i in [1, 4, 7, 8]:
            self.digit_dict[i] = [
                s for s in self.signals if len(s) == DIGITS[i].segment_count
            ][0]

    def parse_segments(self) -> None:

        # parse 'a'
        one = set(self.digit_dict[1])
        seven = set(self.digit_dict[7])
        segment = [s for s in seven if s not in one][0]
        self.segment_dict[segment] = "a"

        # parse 'c'
        six_segments = [set(d) for d in self.signals if len(d) == 6]
        six = [d for d in six_segments if not one.issubset(d)][0]
        segment_c = [s for s in one if s not in six][0]
        self.segment_dict[segment_c] = "c"

        # parse 'f'
        segment_f = [s for s in one if s != segment_c][0]
        self.segment_dict[segment_f] = "f"

        # paese 'b' and 'd'
        four = set(self.digit_dict[4])
        maybe_0, maybe_9 = [d for d in six_segments if d != six]
        maybe_b, maybe_d = [s for s in four if s not in one]

        if (maybe_b in maybe_0) and (maybe_b in maybe_9):
            segment_b, segment_d = maybe_b, maybe_d
        else:
            segment_b, segment_d = maybe_d, maybe_b

        self.segment_dict[segment_b] = "b"
        self.segment_dict[segment_d] = "d"

        # parse e
        nine = maybe_9 if segment_d in maybe_9 else maybe_0
        eight = set(self.digit_dict[8])
        segment_e = [s for s in eight if s not in nine][0]
        self.segment_dict[segment_e] = "e"

        # parse g
        segment_g = [k for k, v in self.segment_dict.items() if not v][0]
        self.segment_dict[segment_g] = "g"

    def calculate_output(self) -> int:

        out = []
        for digit in self.values:
            parsed = {self.segment_dict[i] for i in digit}
            for d in DIGITS.values():
                if parsed == d.segments:
                    out.append(str(d.number))

        return int("".join(out))


def part_2(input_lines: list[str]):

    parsed_lines = parse_lines(input_lines)

    out = []
    for line in parsed_lines:

        parsed_digits = DigitParser(line)
        parsed_digits.find_unique_digits()
        parsed_digits.parse_segments()
        out.append(parsed_digits.calculate_output())

    return sum(out)


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
