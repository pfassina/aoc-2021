def read_file(path: str) -> list[int]:
    with open(path, "r") as file:
        return [int(line) for line in file.readlines()]


def part_1(measurements: list[int]) -> int:

    count: int = 0
    for i, m in enumerate(measurements):
        if i == 0:
            continue
        if m > measurements[i - 1]:
            count += 1

    return count


def part_2(measurements: list[int]) -> int:

    count: int = 0
    for i in range(len(measurements)):
        if i == 0:
            continue
        if i >= len(measurements) - 2:
            break

        current_sum: int = sum(measurements[i : i + 3])
        previous_sum: int = sum(measurements[i - 1 : i + 2])

        if current_sum > previous_sum:
            count += 1

    return count


if __name__ == "__main__":
    measurements = read_file("input.txt")
    out = part_2(measurements)
    print(out)
