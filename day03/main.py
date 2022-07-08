def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def bit_length(bits: list[str]) -> int:
    return len(bits[0])


def bit_to_int(digits: list[int]) -> int:
    return int("".join(str(d) for d in digits), 2)


def bit_counter(bit_lines: list[str]) -> list[dict[int, int]]:
    bit_counter = [{0: 0, 1: 0} for _ in range(bit_length(bit_lines))]
    for line in bit_lines:
        for digit, bit in enumerate(line):
            bit_counter[int(digit)][int(bit)] += 1
    return bit_counter


def filter_by_common_digit(
    bits: list[str], digit: int, criteria: str
) -> list[str]:  # noqa

    counter = bit_counter(bits)
    first = "1" if criteria == "oxygen" else "0"
    second = "0" if criteria == "oxygen" else "1"

    common_digit = first if counter[digit][1] >= counter[digit][0] else second

    return [b for b in bits if b[digit] == common_digit]


def reduce_to_one(bit_options: list[str], criteria: str) -> str:

    if len(bit_options) == 1:
        return bit_options[0]

    counter = bit_counter(bit_options)
    length = len(counter)

    digit = [i for i in range(length) if counter[i][0] * counter[i][1] != 0][0]

    new_options = filter_by_common_digit(bit_options, digit, criteria)

    return reduce_to_one(new_options, criteria)


def part_1(input_lines: list[str]):

    common_bits = bit_counter(input_lines)

    gamma = bit_to_int([0 if b[0] > b[1] else 1 for b in common_bits])
    epsilon = bit_to_int([1 if b[0] > b[1] else 0 for b in common_bits])

    return gamma * epsilon


def part_2(input_lines: list[str]):

    oxygen = int(reduce_to_one(input_lines, "oxygen"), 2)
    co2 = int(reduce_to_one(input_lines, "co2"), 2)

    return oxygen * co2


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
