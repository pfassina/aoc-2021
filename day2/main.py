from dataclasses import dataclass


@dataclass
class Position:
    horizontal: int
    depth: int

    @property
    def result(self) -> int:
        return self.horizontal * self.depth


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.readlines()


def parse_instructions(raw_input: list[str]) -> list[tuple[str, int]]:
    parsed_line = [line.split(" ") for line in raw_input]
    return [(i[0], int(i[1])) for i in parsed_line]


def part_1(input_lines: list[str]):

    parsed_input = parse_instructions(input_lines)
    position = Position(0, 0)

    for i, n in parsed_input:
        if i == "forward":
            position.horizontal += n
        elif i == "down":
            position.depth += n
        elif i == "up":
            position.depth -= n
        else:
            raise Exception(NotImplemented)

    return position.result


def part_2(input_lines: list[str]):
    parsed_input = parse_instructions(input_lines)
    position = Position(0, 0)

    aim = 0
    for i, n in parsed_input:
        if i == "forward":
            position.horizontal += n
            position.depth += aim * n
        elif i == "down":
            aim += n
        elif i == "up":
            aim -= n
        else:
            raise Exception(NotImplemented)

    return position.result


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
