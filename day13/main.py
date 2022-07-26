from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Vector):
            return self.x == __o.x and self.y == __o.y
        return False

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash(f"{self.x},{self.y}")


@dataclass
class Fold:
    direction: str
    index: int

    def __repr__(self) -> str:
        return f"({self.direction}{self.index})"


@dataclass
class Matrix:
    size: Vector
    dots: list[Vector]

    @property
    def height(self) -> int:
        return self.size.y

    @property
    def width(self) -> int:
        return self.size.x

    def get_vector(self, vector: Vector) -> bool:
        return True if vector in self.dots else False

    def print(self) -> None:
        for y in range(self.height):
            print(
                "".join(
                    [
                        "#" if self.get_vector(Vector(x, y)) else "."
                        for x in range(self.width)
                    ]
                )
            )


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def parse_vector(vector: str) -> Vector:
    x, y = [int(i) for i in vector.split(",")]
    return Vector(x, y)


def parse_fold(fold: str) -> Fold:
    fold_instruction = fold.split(" ")[2].split("=")
    direction = "V" if fold_instruction[0] == "x" else "H"
    index = int(fold_instruction[1])
    return Fold(direction, index)


def parse_input(input_lines: list[str]) -> tuple[list[Vector], list[Fold]]:
    empty_index = input_lines.index("")
    a = input_lines[:empty_index]
    coords = [parse_vector(v) for v in a]

    fold_start = empty_index + 1
    fold = [parse_fold(f) for f in input_lines[fold_start:]]
    return coords, fold


def get_size(dots: list[Vector]) -> Vector:
    h = max(v.y for v in dots) + 1
    w = max(v.x for v in dots) + 1
    return Vector(w, h)


def flip(dots: list[Vector], fold: Fold) -> list[Vector]:
    # print(dots)
    if fold.direction == "H":
        flipped = [Vector(d.x, (fold.index - d.y) % fold.index) for d in dots]
        # print(flipped)
        return flipped
    else:
        flipped = [Vector((fold.index - d.x) % fold.index, d.y) for d in dots]
        # print(flipped)
        return flipped


def fold_matrix(matrix: Matrix, fold: Fold) -> Matrix:

    o_dots = matrix.dots

    if fold.direction == "V":
        size = Vector(matrix.width // 2, matrix.height)
        below = [d for d in o_dots if d.x < fold.index]
        above = flip([d for d in o_dots if d.x > fold.index], fold)

    else:
        size = Vector(matrix.width, matrix.height // 2)
        below = [d for d in o_dots if d.y < fold.index]
        above = flip([d for d in o_dots if d.y > fold.index], fold)

    return Matrix(size, list(set(below + above)))


def part_1(input_lines: list[str]):
    dots, fold = parse_input(input_lines)
    size = get_size(dots)
    matrix = Matrix(size, dots)
    new_matrix = fold_matrix(matrix, fold[0])

    return len(new_matrix.dots)


def part_2(input_lines: list[str]):
    dots, fold = parse_input(input_lines)
    size = get_size(dots)
    matrix = Matrix(size, dots)

    for f in fold:
        matrix = fold_matrix(matrix, f)

    matrix.print()

    return len(matrix.dots)


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
