from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Rotation(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3


class Facing(Enum):
    X_POSITIVE = 0
    X_NEGATIVE = 1
    Y_POSITIVE = 2
    Y_NEGATIVE = 3
    Z_POSITIVE = 4
    Z_NEGATIVE = 5


@dataclass
class Orientation:
    rotation: Rotation
    facing: Facing


@dataclass(slots=True)
class Vector3:
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, __o: object) -> Vector3:
        if not isinstance(__o, Vector3):
            raise Exception(TypeError)
        x = self.x + __o.x
        y = self.y + __o.y
        z = self.z + __o.z
        return Vector3(x, y, z)

    def __sub__(self, __o: object) -> Vector3:
        if not isinstance(__o, Vector3):
            raise Exception(TypeError)
        x = self.x - __o.x
        y = self.y - __o.y
        z = self.z - __o.z
        return Vector3(x, y, z)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Vector3):
            return self.x == __o.x and self.y == __o.y and self.z == __o.z
        return False

    def __gt__(self, __o: object) -> bool:
        if isinstance(__o, Vector3):
            a_dist = abs(self.x) + abs(self.y) + abs(self.z)
            b_dist = abs(__o.x) + abs(__o.y) + abs(__o.z)
            return a_dist > b_dist
        return False

    def __hash__(self) -> int:
        return hash(f"{self.x}{self.y}{self.z}")


@dataclass(slots=True)
class Scanner:
    beacons: set[Vector3]

    @property
    def constelation(self) -> dict[Vector3, set[Vector3]]:
        return {b: self.beacon_neighbors(b) for b in self.beacons}

    def beacon_neighbors(self, pos: Vector3) -> set[Vector3]:
        return {pos - b for b in self.beacons if b != pos}

    def print(self) -> None:
        for b in self.beacons:
            print(b)


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def parse_beacon(line: str) -> Vector3:
    x, y, z = [int(i) for i in line.split(",")]
    return Vector3(x, y, z)


def parse_scanners(lines: list[str]) -> list[Scanner]:

    breaks = [i for i, j in enumerate(lines) if j == ""]

    s = 1
    ranges = []
    for b in breaks + [len(lines)]:
        ranges.append((s, b))
        s = b + 2

    scanners = [lines[i:j] for (i, j) in ranges]
    return [Scanner({parse_beacon(b) for b in s}) for s in scanners]


def normalize_rotation(pos: Vector3, rotation: Rotation) -> Vector3:
    if rotation == Rotation.ONE:
        return Vector3(pos.x, pos.z, -pos.y)
    if rotation == Rotation.TWO:
        return Vector3(pos.x, -pos.y, -pos.z)
    if rotation == Rotation.THREE:
        return Vector3(pos.x, -pos.z, pos.y)
    return pos


def normalize_facing(pos: Vector3, facing: Facing) -> Vector3:
    if facing == Facing.X_NEGATIVE:
        return Vector3(-pos.x, pos.y, -pos.z)
    if facing == Facing.Y_POSITIVE:
        return Vector3(-pos.z, pos.x, -pos.y)
    if facing == Facing.Y_NEGATIVE:
        return Vector3(pos.z, -pos.x, -pos.y)
    if facing == Facing.Z_POSITIVE:
        return Vector3(-pos.z, pos.y, pos.x)
    if facing == Facing.Z_NEGATIVE:
        return Vector3(pos.z, pos.y, -pos.x)
    return pos


def normalize_vector(pos: Vector3, r: Rotation, f: Facing) -> Vector3:
    return normalize_facing(normalize_rotation(pos, r), f)


def normalize_scanner(scanner: Scanner, r: Rotation, f: Facing) -> Scanner:
    return Scanner({normalize_vector(b, r, f) for b in scanner.beacons})


def find_common_beacons(
    a: dict[Vector3, set[Vector3]], b: dict[Vector3, set[Vector3]]
) -> list[tuple[Vector3, Vector3]]:

    ak = list(a.keys())
    bk = list(b.keys())
    av = a.values()
    bv = b.values()

    common = []
    for i, x in enumerate(av):
        for j, y in enumerate(bv):
            n = x.intersection(y)
            if len(n) >= 11:
                common.append((ak[i], bk[j]))

    return common


def rel_position(a: Scanner, b: Scanner) -> tuple[Vector3, Orientation] | None:

    relative_position = None
    orientation = Orientation(Rotation.ZERO, Facing.X_POSITIVE)

    sa = a.constelation

    for r in Rotation:
        for f in Facing:
            norm_b = normalize_scanner(b, r, f)
            sb = norm_b.constelation
            common_beacons = find_common_beacons(sa, sb)
            if common_beacons:
                orientation = Orientation(r, f)
                relative_position = common_beacons[0][0] - common_beacons[0][1]

    if relative_position:
        return relative_position, orientation

    return None


def rotate_scanners(scanners: list[Scanner]) -> dict[int, tuple[Vector3, Orientation]]:

    rotated: dict[int, tuple[Vector3, Orientation]] = {
        0: (Vector3(0, 0, 0), Orientation(Rotation.ZERO, Facing.X_POSITIVE))
    }

    while len(rotated) < len(scanners):
        for i, _ in enumerate(scanners):
            if i not in rotated:
                continue

            p = rotated[i][0]
            o = rotated[i][1]
            a = normalize_scanner(scanners[i], o.rotation, o.facing)

            for j, b in enumerate(scanners):
                if j in rotated:
                    continue
                if j == i:
                    continue

                found = rel_position(a, b)
                if found:
                    rotated[j] = (found[0] + p, found[1])

    return rotated


def get_constelation(scanners: list[Scanner]) -> set[Vector3]:

    scanner_details = rotate_scanners(scanners)
    beacons: set[Vector3] = set(scanners[0].beacons)

    for i, s in enumerate(scanners):
        p = scanner_details[i][0]
        o = scanner_details[i][1]
        normal_beacons = [
            normalize_vector(b, o.rotation, o.facing) + p for b in s.beacons
        ]
        for b in normal_beacons:
            beacons.add(b)

    return beacons


def part_1(input_lines: list[str]):

    scanners = parse_scanners(input_lines)
    beacons = get_constelation(scanners)

    return len(beacons)


def part_2(input_lines: list[str]):

    scanners = parse_scanners(input_lines)
    positions = [s[0] for s in rotate_scanners(scanners).values()]
    #
    # for p in positions:
    #     print(p)

    distance = Vector3(0, 0, 0)
    for p in positions:
        for n in positions:
            distance = max(p - n, distance)

    return abs(distance.x) + abs(distance.y) + abs(distance.z)


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
