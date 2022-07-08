from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    VERT = "vertical"
    HORZ = "horizontal"
    ASC = "ascending"
    DESC = "descending"


@dataclass
class Vector:
    x: int
    y: int

    def __eq__(self, other) -> bool:
        if (self.x == other.x) and (self.y == self.y):
            return True
        return False

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Line:
    start: Vector
    end: Vector

    @property
    def direction(self) -> Direction:

        if self.start.x == self.end.x:
            return Direction.VERT
        elif self.start.y == self.end.y:
            return Direction.HORZ
        elif self.start.x == self.min_x and self.start.y == self.min_y:
            return Direction.DESC
        elif self.start.x == self.max_x and self.start.y == self.max_y:
            return Direction.DESC
        elif self.start.x == self.min_x and self.start.y == self.max_y:
            return Direction.ASC
        elif self.start.x == self.max_x and self.start.y == self.min_y:
            return Direction.ASC

        else:
            raise Exception(NotImplemented)

    @property
    def max_x(self) -> int:
        return max(self.start.x, self.end.x)

    @property
    def max_y(self) -> int:
        return max(self.start.y, self.end.y)

    @property
    def min_x(self) -> int:
        return min(self.start.x, self.end.x)

    @property
    def min_y(self) -> int:
        return min(self.start.y, self.end.y)


@dataclass
class SurfaceMap:
    raw_lines: list[str]
    diagonal: bool

    def valid_line(self, line: Line) -> bool:
        if line.start.x == line.end.x:
            return True
        if line.start.y == line.end.y:
            return True
        return False

    def parse_line(self, raw_line) -> Line:
        raw_start, raw_end = raw_line.split("->")
        start = Vector(*[int(i) for i in raw_start.split(",")])
        end = Vector(*[int(i) for i in raw_end.split(",")])

        return Line(start, end)

    def __post_init__(self):
        self.vent_lines = [self.parse_line(line) for line in self.raw_lines]

        if not self.diagonal:
            self.vent_lines = [
                line for line in self.vent_lines if self.valid_line(line)
            ]

        max_x = max(line.max_x for line in self.vent_lines)
        max_y = max(line.max_y for line in self.vent_lines)
        self.map = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    def draw_map(self):

        for line in self.vent_lines:

            # draw vertical lines
            if line.direction == Direction.VERT:
                row = line.start.x
                start = line.min_y
                finish = line.max_y

                for y, l in enumerate(self.map):
                    for x in range(len(l)):
                        if x != row:
                            continue
                        if start <= y <= finish:
                            self.map[y][x] += 1
                continue

            # draw horizontal lines
            if line.direction == Direction.HORZ:
                col = line.start.y
                start = line.min_x
                finish = line.max_x
                for x in range(len(self.map[col])):
                    if start <= x <= finish:
                        self.map[col][x] += 1
                continue

            valid_x = range(line.min_x, line.max_x + 1)
            valid_y = []

            if line.direction == Direction.ASC:
                valid_y = range(line.max_y, line.min_y - 1, -1)

            if line.direction == Direction.DESC:
                valid_y = range(line.min_y, line.max_y + 1)

            vent_loc = zip(valid_x, valid_y)

            for loc in vent_loc:
                x = loc[0]
                y = loc[1]
                self.map[y][x] += 1

    @property
    def intersections(self) -> int:
        self.draw_map()

        intersections = 0
        for row in self.map:
            for pos in row:
                if pos > 1:
                    intersections += 1
        return intersections


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def part_1(input_lines: list[str]):
    surface_map = SurfaceMap(input_lines, diagonal=False)
    return surface_map.intersections


def part_2(input_lines: list[str]):
    surface_map = SurfaceMap(input_lines, diagonal=True)
    return surface_map.intersections


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
