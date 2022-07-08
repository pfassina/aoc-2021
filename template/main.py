def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def part_1(input_lines: list[str]):
    return input_lines


# def part_2(input_lines: list[str]):
#     return


if __name__ == "__main__":
    inp = read_file("sample.txt")
    out = part_1(inp)
    print(out)
