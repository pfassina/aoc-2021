from dataclasses import dataclass


@dataclass(slots=True)
class Vector:
    x: int
    y: int

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Vector):
            return (self.x == __o.x) and (self.y == __o.y)
        return False

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Octopus:
    energy: int
    location: Vector
    flashed: bool

    @property
    def neighbors(self) -> list[Vector]:
        directions = [
            Vector(x + self.location.x, y + self.location.y)
            for x in range(-1, 2)
            for y in range(-1, 2)
            if (x, y) != (0, 0)  # noqa
        ]
        return [d for d in directions]


@dataclass
class FloorMap:
    width: int
    height: int
    octopusi: list[Octopus]

    def __post_init__(self):
        self.flash_count = 0
        self.step_count = 0

    @property
    def vectors(self) -> list[Vector]:
        return [
            Vector(x, y) for x in range(self.width) for y in range(self.height)
        ]  # noqa

    def octopus(self, location) -> Octopus:
        return [o for o in self.octopusi if o.location == location][0]

    def get_neighbors(self, octopus: Octopus) -> list[Octopus]:
        location = octopus.location
        neighbors = [
            Vector(x + location.x, y + location.y)
            for x in range(-1, 2)
            for y in range(-1, 2)
            if (x, y) != (0, 0)  # noqa
        ]
        return [
            self.octopus(neighbor)
            for neighbor in neighbors
            if (0 <= neighbor.x < self.width)
            and (0 <= neighbor.y < self.height)  # noqa
        ]

    def print(self) -> None:
        for y in range(self.height):
            print([o.energy for o in self.octopusi if o.location.y == y])
        print("")

    def take_step(self) -> None:

        # increase energy of all octopusi
        for octopus in self.octopusi:
            octopus.energy += 1

        # set all octopusi with energery > 9 to flashed
        flashed = [octopus for octopus in self.octopusi if octopus.energy > 9]
        for octopus in flashed:
            octopus.flashed = True

        # calculate flash impact to neighbors
        for octopus in flashed:
            self.flash_neighbors(octopus)

    def end_step(self) -> None:
        self.step_count = 0
        for octopus in self.octopusi:
            if not octopus.flashed:
                continue
            octopus.energy = 0
            octopus.flashed = False
            self.flash_count += 1
            self.step_count += 1

    def flash_neighbors(self, octopus: Octopus) -> None:
        neighbors = [n for n in self.get_neighbors(octopus) if not n.flashed]
        if not neighbors:
            return
        for neighbor in neighbors:
            if neighbor.flashed:
                continue
            neighbor.energy += 1
            if neighbor.energy < 10:
                continue
            neighbor.flashed = True
            self.flash_neighbors(neighbor)


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def load_octupusi(input_lines: list[str]) -> list[Octopus]:

    octupusi: list[Octopus] = []
    for y, line in enumerate(input_lines):
        for x, energy in enumerate(line):
            octupusi.append(Octopus(int(energy), Vector(x, y), False))

    return octupusi


def part_1(input_lines: list[str]):
    octupusi = load_octupusi(input_lines)
    floor_map = FloorMap(10, 10, octupusi)

    for _ in range(100):
        floor_map.take_step()
        floor_map.end_step()

    return floor_map.flash_count


def part_2(input_lines: list[str]):
    octupusi = load_octupusi(input_lines)
    floor_map = FloorMap(10, 10, octupusi)

    i = 0
    while floor_map.step_count != 100:
        floor_map.take_step()
        floor_map.end_step()
        i += 1

    return i


if __name__ == "__main__":
    inp = read_file("input.txt")
    octupusi = part_2(inp)
    print(octupusi)
