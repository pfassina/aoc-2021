from dataclasses import dataclass
import math


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


@dataclass(slots=True)
class Vector:
    x: int
    y: int

    @property
    def location(self) -> str:
        return f"{self.x}|{self.y}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Vector):
            return (self.x == __o.x) and (self.y == __o.y)
        return False


@dataclass
class FloorMap:
    height_map: list[list[int]]

    def __post_init__(self):
        self.basins = {v.location: [v] for v in self.low_points}

    @property
    def height(self) -> int:
        return len(self.height_map)

    @property
    def width(self) -> int:
        return len(self.height_map[0])

    @property
    def vectors(self) -> list[Vector]:
        return [
            Vector(x, y) for x in range(self.width) for y in range(self.height)
        ]  # noqa

    @property
    def low_points(self) -> list[Vector]:
        return [v for v in self.vectors if self.is_lowpoint(v)]

    @property
    def risk_level(self) -> int:
        return sum([self.get_vector_height(v) + 1 for v in self.low_points])

    def get_vector_height(self, pos: Vector) -> int:
        return self.height_map[pos.y][pos.x]

    def is_lowpoint(self, pos: Vector) -> bool:

        adj = self.get_adj(pos)
        pos_height = self.get_vector_height(pos)
        adj_height = [self.get_vector_height(a) for a in adj]

        return pos_height < min(adj_height)

    def is_ridge(self, pos: Vector) -> bool:
        return True if self.get_vector_height(pos) == 9 else False

    def find_basins(self) -> None:
        while True:
            start_len = sum(len(b) for b in self.basins.values())
            new_len = self.expand_basins()
            if start_len == new_len:
                break

    def expand_basins(self) -> int:

        for origin, basin in self.basins.items():
            for vector in basin:
                valid_vectors = [
                    v for v in self.get_adj(vector) if not self.is_ridge(v)
                ]
                for v in valid_vectors:
                    if v in basin:
                        continue
                    if self.is_ridge(v):
                        continue
                    self.basins[origin].append(v)
        return sum([len(b) for b in self.basins.values()])

    def get_adj(self, pos: Vector) -> list[Vector]:
        if pos == Vector(0, 0):
            return [
                Vector(pos.x + 1, pos.y),
                Vector(pos.x, pos.y + 1),
            ]
        if pos == Vector(0, self.height - 1):
            return [
                Vector(pos.x + 1, pos.y),
                Vector(pos.x, pos.y - 1),
            ]
        if pos == Vector(self.width - 1, 0):
            return [
                Vector(pos.x - 1, pos.y),
                Vector(pos.x, pos.y + 1),
            ]
        if pos == Vector(self.width - 1, self.height - 1):
            return [
                Vector(pos.x - 1, pos.y),
                Vector(pos.x, pos.y - 1),
            ]
        if pos.x == 0:
            return [
                Vector(pos.x + 1, pos.y),
                Vector(pos.x, pos.y - 1),
                Vector(pos.x, pos.y + 1),
            ]
        if pos.x == self.width - 1:
            return [
                Vector(pos.x - 1, pos.y),
                Vector(pos.x, pos.y - 1),
                Vector(pos.x, pos.y + 1),
            ]
        if pos.y == 0:
            return [
                Vector(pos.x - 1, pos.y),
                Vector(pos.x + 1, pos.y),
                Vector(pos.x, pos.y + 1),
            ]
        if pos.y == self.height - 1:
            return [
                Vector(pos.x - 1, pos.y),
                Vector(pos.x + 1, pos.y),
                Vector(pos.x, pos.y - 1),
            ]
        return [
            Vector(pos.x - 1, pos.y),
            Vector(pos.x + 1, pos.y),
            Vector(pos.x, pos.y - 1),
            Vector(pos.x, pos.y + 1),
        ]

    def print(self) -> None:
        for row in self.height_map:
            print(row)


def parse_input(input: list[str]) -> FloorMap:
    return FloorMap([[int(loc) for loc in row] for row in input])


def part_1(input_lines: list[str]):
    floor_map = parse_input(input_lines)
    return floor_map.risk_level


def part_2(input_lines: list[str]):
    floor_map = parse_input(input_lines)
    floor_map.find_basins()
    basins = floor_map.basins
    b_len = [len(b) for b in basins.values()]
    b_len.sort(reverse=True)

    return math.prod(b_len[:3])


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
