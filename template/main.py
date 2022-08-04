
def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def part_1(input_lines: list[str]):
    return input_lines


def part_2(input_lines: list[str]):
    return input_lines


if __name__ == "__main__":

    sample = 1
    part = 1

    path = "sample.txt" if sample else "input.txt"
    inp = read_file(path)

    if part == 1:
        out = part_1(inp)
    else:
        out = part_2(inp)

    print(out)
