from __future__ import annotations
from dataclasses import dataclass


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


@dataclass
class Vector:
    x: int
    y: int

    def __add__(self, __o) -> Vector:
        if isinstance(__o, Vector):
            x = self.x + __o.x
            y = self.y + __o.y
            return Vector(x, y)
        raise Exception(TypeError)

    def __iadd__(self, __o) -> Vector:
        if isinstance(__o, Vector):
            x = self.x + __o.x
            y = self.y + __o.y
            return Vector(x, y)
        raise Exception(TypeError)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Vector):
            return self.x == __o.x and self.y == __o.y
        return False

    def __le__(self, __o: object) -> bool:
        if isinstance(__o, Vector):
            return self.x <= __o.x and self.y <= __o.y
        return False

    def __ge__(self, __o: object) -> bool:
        if isinstance(__o, Vector):
            return self.x >= __o.x and self.y >= __o.y
        return False

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash(f"{self.x}{self.y}")


@dataclass
class Target:
    start: Vector
    end: Vector

    @property
    def min_x(self) -> int:
        return min(self.start.x, self.end.x)

    @property
    def max_x(self) -> int:
        return max(self.start.x, self.end.x)

    @property
    def min_y(self) -> int:
        return min(self.start.y, self.end.y)

    @property
    def max_y(self) -> int:
        return max(self.start.y, self.end.y)

    def hit(self, pos: Vector) -> bool:
        return self.start <= pos <= self.end


def parse_input(input: str) -> Target:
    ranges = input[13:]
    x_range, y_range = [r.split("=")[1].split("..") for r in ranges.split(",")]
    x = [int(i) for i in x_range]
    y = [int(i) for i in y_range]

    return Target(Vector(x[0], y[0]), Vector(x[1], y[1]))


def take_step(pos: Vector, vel: Vector) -> tuple[Vector, Vector]:

    pos += vel

    if vel.x > 0:
        vel += Vector(-1, 0)

    if vel.x < 0:
        vel += Vector(1, 0)

    vel += Vector(0, -1)

    return pos, vel


def hits_x(target: Target, x0: int) -> bool:

    p = Vector(0, 0)
    v = Vector(x0, target.min_y)

    possible_x: list[Vector] = []
    while v.x != 0:
        p, v = take_step(p, v)
        possible_x.append(Vector(p.x, target.start.y))

    return any(target.hit(x) for x in possible_x)


def hits_y(target: Target, y0: int) -> bool:

    p = Vector(target.min_x, 0)
    v = Vector(0, y0)

    old_p = p
    new_p, v = take_step(p, v)

    possible_y: list[Vector] = []
    if target.hit(new_p):
        possible_y.append(new_p)

    raising_y: list[Vector] = [old_p, new_p]
    while new_p.y > old_p.y:
        old_p = new_p
        new_p, v = take_step(old_p, v)
        raising_y.append(new_p)

    declining_y: list[Vector] = []
    while new_p.y >= target.min_y:
        old_p = new_p
        new_p, v = take_step(old_p, v)
        if new_p.y >= target.min_y:
            declining_y.append(new_p)

    possible_y += raising_y + declining_y

    return any(target.hit(y) for y in possible_y)


def hits_both(target: Target, vel: Vector) -> bool:

    p = Vector(0, 0)
    v = vel

    while p.y >= target.min_y:
        p, v = take_step(p, v)
        if target.hit(p):
            return True

    return False


def possible_x(target: Target) -> set[int]:
    return {x for x in range(target.max_x + 1) if hits_x(target, x)}


def possible_y(target: Target) -> set[int]:
    y_range = range(target.min_y, abs(target.min_y))
    return {y for y in y_range if hits_y(target, y)}


def possible_v(target: Target) -> set[Vector]:
    x_range = possible_x(target)
    y_range = possible_y(target)

    possible_v: set[Vector] = set()
    for x in x_range:
        for y in y_range:
            v = Vector(x, y)
            if hits_both(target, v):
                possible_v.add(v)

    return possible_v


def get_max_height(velocity: Vector) -> tuple[Vector, int]:

    old_p = Vector(0, 0)
    new_p, v = take_step(old_p, velocity)

    if new_p.y == 0:
        return velocity, 0

    raising_y: list[int] = []
    while new_p.y > old_p.y:
        old_p = new_p
        new_p, v = take_step(old_p, v)
        raising_y.append(new_p.y)

    return velocity, raising_y[-1]


def part_1(input_lines: list[str]):

    t = parse_input(input_lines[0])

    v_range = possible_v(t)

    max_h = [get_max_height(v) for v in v_range]
    max_v, max_y = max_h[0]

    for h in max_h:
        if h[1] > max_y:
            max_v = h[0]
            max_y = h[1]

    return max_v, max_y


def part_2(input_lines: list[str]):

    t = parse_input(input_lines[0])
    v_range = possible_v(t)

    # for v in v_range:
    #     print(v)
    #
    return len(v_range)


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
