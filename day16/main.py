from dataclasses import dataclass
import math


def parse_hexa(hexa: str) -> str:
    return bin(int(hexa, 16))[2:].zfill(4)


def parse_input(line: str) -> str:
    return "".join([parse_hexa(c) for c in line])


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


@dataclass(slots=True)
class Version:
    bit_array: str

    def __repr__(self) -> str:
        return str(int(self.bit_array, 2))

    def __int__(self) -> int:
        return int(self.bit_array, 2)


@dataclass(slots=True)
class Type:
    bit_array: str

    def __eq__(self, __o: object) -> bool:
        return int(self.bit_array, 2) == __o


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

    @property
    def length(self) -> int:
        return len(self.bit_array)

    def __repr__(self) -> str:
        return str(self.bit_array)


@dataclass(slots=True)
class LengthType:
    bit_array: str

    @property
    def is_packets(self) -> bool:
        return True if bool(int(self.bit_array)) else False

    @property
    def bits(self) -> int:
        return 11 if self.is_packets else 15

    def __repr__(self) -> str:
        return "Packets" if self.is_packets else "Bits"


@dataclass(slots=True)
class Header:
    version: Version
    type: Type
    length_type: LengthType | None = None
    length: int = 0

    @property
    def bits(self) -> int:
        if self.length_type:
            return 6 + 1 + self.length_type.bits
        return 6


@dataclass(slots=True)
class Packet:
    header: Header
    literals: list[Bit]

    @property
    def length(self) -> int:
        return 6 + sum(b.length for b in self.literals) + len(self.literals)

    @property
    def value(self) -> int:
        return int("".join(str(b) for b in self.literals), 2)

    @property
    def packets(self) -> None:
        return None

    def __repr__(self) -> str:
        v = self.header.version
        t = self.header.type
        lt = self.literals
        return f"Packet: (V: {v} | T: {t} | L: {lt})"

    def __eq__(self, __o: object) -> bool:
        return id(self) == id(__o)


@dataclass
class Operator:
    header: Header
    packets: list

    @property
    def length(self) -> int:
        return self.header.bits + sum(p.length for p in self.packets)

    @property
    def value(self) -> int:

        if self.header.type == 0:
            return sum(p.value for p in self.packets)

        if self.header.type == 1:
            return math.prod(p.value for p in self.packets)

        if self.header.type == 2:
            return min(p.value for p in self.packets)

        if self.header.type == 3:
            return max(p.value for p in self.packets)

        if self.header.type == 5:
            return 1 if self.packets[0].value > self.packets[1].value else 0

        if self.header.type == 6:
            return 1 if self.packets[0].value < self.packets[1].value else 0

        if self.header.type == 7:
            return 1 if self.packets[0].value == self.packets[1].value else 0

        return 1

    def __repr__(self) -> str:
        v = self.header.version
        t = self.header.type
        p = self.packets
        return f"Operator (V: {v} | T: {t} | P: {p})"


SubPacket = Operator | Packet


def parse_bits(bit_array: str, start: int, length: int) -> str:
    a = start
    b = start + length
    return bit_array[a:b]


def get_type(bit_array: str, start: int) -> Type:
    return Type(parse_bits(bit_array, start, 3))


def get_version(bit_array: str, start: int) -> Version:
    return Version(parse_bits(bit_array, start, 3))


def get_length_type(bit_array: str, start: int) -> LengthType:
    return LengthType(parse_bits(bit_array, start, 1))


def get_length(bit_array: str, start: int, length_type: LengthType) -> int:
    return int(parse_bits(bit_array, start, length_type.bits), 2)


def get_last(bit_array: str, start: int) -> Last:
    return Last(parse_bits(bit_array, start, 1))


def get_literal(bit_array: str, start: int) -> Bit:
    return Bit(parse_bits(bit_array, start, 4))


def get_header(bit_array: str) -> Header:

    v = get_version(bit_array, 0)
    t = get_type(bit_array, 3)

    if t == 4:
        return Header(v, t)

    lt = get_length_type(bit_array, 6)
    length = get_length(bit_array, 7, lt)

    return Header(version=v, type=t, length_type=lt, length=length)


def get_packet(bit_array: str) -> Packet:

    header = get_header(bit_array)

    literals = []
    i = header.bits
    while i < len(bit_array):
        last = get_last(bit_array, i)
        i += 1
        literals.append(get_literal(bit_array, i))
        i += 4
        if last:
            break

    return Packet(header, literals)


def get_subpacket(bit_array: str) -> Operator | Packet:

    header = get_header(bit_array)

    if header.type == 4:
        return get_packet(bit_array)

    return get_operator(bit_array)


def get_by_packets(packet_count: int, bit_array: str) -> list[SubPacket]:
    packets: list[SubPacket] = []

    i = 0
    while len(packets) < packet_count:
        subpacket = get_subpacket(bit_array[i:])
        packets.append(subpacket)
        i += subpacket.length
    return packets


def get_by_bits(bit_count: int, bit_array: str) -> list[SubPacket]:

    subpackets: list[SubPacket] = []
    i = 0
    while i < bit_count:
        subpacket = get_subpacket(bit_array[i:])
        subpackets.append(subpacket)
        i += subpacket.length

    return subpackets


def get_subpacket_list(header: Header, bit_array: str) -> list[SubPacket]:

    is_packets = header.length_type.is_packets  # type: ignore
    length = header.length

    if is_packets:
        return get_by_packets(length, bit_array)

    return get_by_bits(length, bit_array[:length])


def get_operator(bit_array: str) -> Operator:

    header = get_header(bit_array)
    start = header.bits
    packets = get_subpacket_list(header, bit_array[start:])

    return Operator(header, packets)


def count_version(packet_list: list[SubPacket]) -> int:
    return sum(int(packet.header.version) for packet in packet_list)


def dfs(packet, visited):

    if packet not in visited:
        visited.append(packet)
        if packet.header.type == 4:
            return visited

        for p in packet.packets:
            dfs(p, visited)

    return visited


def part_1(input_lines: list[str]):

    bit_array = parse_input(input_lines[0])
    packets = get_operator(bit_array)

    visited = dfs(packets, [])
    versions = count_version(visited)

    return versions


def part_2(input_lines: list[str]):
    for line in input_lines:
        bit_array = parse_input(line)
        packets = get_operator(bit_array)
        print(packets.value)

    return


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)

    print(out)
