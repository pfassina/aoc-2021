import ast
from functools import reduce
import re


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def parse_line(line: str | list):
    if isinstance(line, list):
        return line
    return ast.literal_eval(line)


def check_depth(snail_number: list) -> int:

    sn = str(snail_number)

    n = 0
    for i, c in enumerate(sn):
        if c == "[":
            n += 1
        if c == "]":
            n -= 1
        if n == 5:
            return i

    return -1


def extract_n(snail_number: list, i: int) -> list[int]:

    sn = str(snail_number)
    d4 = sn[i:]
    j = d4.find("]") + 1

    return ast.literal_eval(d4[:j])


def extract_before(snail_number: list, n: list[int], n_i: int) -> str:

    sn = str(snail_number)
    before = sn[:n_i]
    last_n = re.search(r"\d+", before[::-1])
    if not last_n:
        return before

    i = len(before) - last_n.start()
    j = len(before) - last_n.end()

    left_n = int(before[j:i]) + n[0]

    return before[:j] + str(left_n) + before[i:]


def extract_after(snail_number: list, n: list[int], n_i: int) -> str:
    sn = str(snail_number)

    i = n_i + len(str(n))
    after = sn[i:]

    next_n = re.search(r"\d+", after)
    if not next_n:
        return after

    i = next_n.start()
    j = next_n.end()

    next_n = int(after[i:j]) + n[1]

    return after[:i] + str(next_n) + after[j:]


def explode(snail_number: list, log: bool = False) -> list:

    d4_i = check_depth(snail_number)
    if d4_i == -1:
        return snail_number

    n = extract_n(snail_number, d4_i)
    if log:
        print("\t ", n)

    before = extract_before(snail_number, n, d4_i)
    after = extract_after(snail_number, n, d4_i)

    return ast.literal_eval(before + "0" + after)


def check_split(snail_number: list) -> int:
    sn = str(snail_number)
    splits = re.search(r"[1-9][0-9]+", sn)

    if not splits:
        return -1

    return splits.start()


def split(snail_number: list, log: bool = False) -> list:

    sn = str(snail_number)

    splits = re.search(r"[1-9][0-9]+", sn)

    if not splits:
        return snail_number

    i = splits.start()
    j = splits.end()
    n = int(sn[i:j])
    if log:
        print("\t ", n)

    before = sn[:i]
    after = sn[j:]

    new_sn = ast.literal_eval(before + f"[{n//2}, {n - n//2}]" + after)
    return new_sn


def add_sn(a: list, b: list) -> list:
    return [a, b]


def magnitude(snail_number: list) -> int:
    def rsn(sn):
        if not isinstance(sn, list):
            return sn
        return reduce(lambda a, b: rsn(a) * 3 + rsn(b) * 2, sn)

    return reduce(lambda a, b: rsn(a) * 3 + rsn(b) * 2, snail_number)


def process_sn(snail_number: list, log: bool) -> list:

    e = check_depth(snail_number)
    s = check_split(snail_number)

    if e != -1:
        if log:
            print("\texp:")
            print("\t ", snail_number)
            print("\t ", explode(snail_number, log))
        return explode(snail_number)

    if s != -1:
        if log:
            print("\tspl:")
            print("\t ", snail_number)
            print("\t ", split(snail_number, log))
        return split(snail_number)

    return snail_number


def calc(a: list | str, b: list | str, log: bool = False) -> list:

    old = add_sn(parse_line(a), parse_line(b))
    new = process_sn(old, log)

    if new == old:
        return old

    while new != old:
        old = new
        new = process_sn(old, log)

    return new


def part_1(input_lines: list[str]):

    snl = input_lines

    sn = reduce(lambda a, b: calc(a, b), snl)
    print(sn)

    return magnitude(sn)  # type: ignore


def part_2(input_lines: list[str]):

    from itertools import permutations

    sn_pairs = permutations(input_lines, 2)

    m = 0
    for p in sn_pairs:
        n = magnitude(calc(p[0], p[1]))
        m = max(n, m)

    return m


if __name__ == "__main__":

    sample = 0
    part = 2

    path = "sample.txt" if sample else "input.txt"
    inp = read_file(path)

    if part == 1:
        out = part_1(inp)
    else:
        out = part_2(inp)

    print(out)
