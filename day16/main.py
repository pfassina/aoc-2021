from dataclasses import dataclass
from os import wait


@dataclass(slots=True)
class Version:
    bit_array: str

    def __repr__(self) -> str:
        return str(int(self.bit_array, 2))


@dataclass(slots=True)
class Type:
    bit_array: str

    def __eq__(self, __o: object) -> bool:
        return int(self.bit_array, 2) == __o

    def __repr__(self) -> str:
        return str(int(self.bit_array, 2))


@dataclass(slots=True)
class Last:
    bit_array: str

    def __bool__(self) -> bool:
        return not bool(int(self.bit_array, 2))

    def __repr__(self) -> str:
        return str(not bool(int(self.bit_array, 2)))


@dataclass(slots=True)
class Bit:
    bit_array: str

    def __repr__(self) -> str:
        return self.bit_array


@dataclass(slots=True)
class LengthType:
    bit_array: str

    @property
    def range(self) -> int:
        return 11 if bool(int(self.bit_array)) else 15

    def __repr__(self) -> str:
        return str(bool(self.bit_array))


@dataclass
class Packet:
    version: Version
    type: Type
    bits: list[Bit]

    @property
    def length(self) -> int:
        return 3 + 3 + sum(len(str(b)) for b in self.bits)

    @property
    def literal(self) -> bool:
        return self.type == 4

    @property
    def value(self) -> int:
        if self.literal:
            return int("".join(str(b) for b in self.bits), 2)
        else:
            return 0


@dataclass
class Operator:
    version: Version
    type: Type
    packets: list

    @property
    def length(self) -> int:
        return 6 + sum(p.length for p in self.packets)


def chop_bit(input: str, start: int, length: int) -> str:
    a = start
    b = start + length
    return input[a:b]


def chop_packet(bit_array: str) -> Packet:
    v = Version(chop_bit(bit_array, 0, 3))
    t = Type(chop_bit(bit_array, 3, 3))

    bits = []
    i = 6
    while i < len(bit_array):
        last = Last(chop_bit(bit_array, i, 1))
        i += 1
        bits.append(Bit(chop_bit(bit_array, i, 4)))
        i += 4
        if last:
            break

    return Packet(v, t, bits)


def chop_header(bit_array: str) -> tuple[Version, Type, int]:

    v = Version(chop_bit(bit_array, 0, 3))
    t = Type(chop_bit(bit_array, 3, 3))

    if t != 4:
        lt = LengthType(chop_bit(bit_array, 6, 1))
        length = lt.range

    else:
        length = 0

    return v, t, length


def chop_operator(bit_array: str, packets: list) -> Operator:

    v, t, length = chop_header(bit_array)
    start = 7 + length

    next_type = Type(chop_bit(bit_array, 3, 3))
    if next_type == 4:
        packets.append(chop_packet(bit_array))
        return Operator(v, t, packets)

    return chop_operator(bit_array[start:], packets)
    # return Operator(v, t, packets)


def parse_hexa(hexa: str) -> str:
    return bin(int(hexa, 16))[2:].zfill(4)


def parse_input(line: str) -> str:
    return "".join([parse_hexa(c) for c in line])


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def part_1(input_lines: list[str]):

    h = parse_input(input_lines[0])
    a = chop_operator(h, [])

    return a


# def part_2(input_lines: list[str]):
#     return


if __name__ == "__main__":
    inp = read_file("sample.txt")
    out = part_1(inp)

    print(out)
