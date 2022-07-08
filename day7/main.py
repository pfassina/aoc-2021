def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def parse_input(input: list[str]) -> list[int]:
    return [int(i) for i in input[0].split(",")]


def part_1(input_lines: list[str]):

    crabs = parse_input(input_lines)
    available_pos = range(min(crabs), max(crabs) + 1)
    fuel_cost = {i: 0 for i in available_pos}

    for pos in available_pos:
        for crab in crabs:
            fuel_cost[pos] += abs(crab - pos)

    return min(fuel_cost.values())


def part_2(input_lines: list[str]):

    crabs = parse_input(input_lines)
    available_pos = range(min(crabs), max(crabs) + 1)
    fuel_cost = {i: 0 for i in available_pos}

    for pos in available_pos:
        for crab in crabs:
            distance = abs(crab - pos)
            fuel_cost[pos] += int(distance * (distance + 1) / 2)

    return min(fuel_cost.values())


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
