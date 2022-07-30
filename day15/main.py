from dataclasses import dataclass
from queue import PriorityQueue
import sys


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


@dataclass(slots=True)
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
        return hash(f"{self.x}{self.y}")


@dataclass(slots=True)
class Node:
    pos: Vector
    risk: int

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.pos == __o.pos and self.risk == __o.risk
        return False

    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.risk < __o.risk
        else:
            raise Exception(TypeError)

    def __le__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.risk <= __o.risk
        else:
            raise Exception(TypeError)

    def __gt__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.risk > __o.risk
        else:
            raise Exception(TypeError)

    def __ge__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.risk >= __o.risk
        else:
            raise Exception(TypeError)

    def __ne__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.risk != __o.risk
        else:
            raise Exception(TypeError)

    def __repr__(self) -> str:
        return str(self.pos)

    def __hash__(self) -> int:
        return hash(f"{self.pos.x}{self.pos.y}")


Path = list[Node]


@dataclass(slots=True)
class Matrix:
    nodes: list[list[Node]]

    @property
    def node_list(self) -> Path:
        return [n for r in self.nodes for n in r]

    @property
    def start(self) -> Node:
        return self.nodes[0][0]

    @property
    def end(self) -> Node:
        return self.nodes[-1][-1]

    @property
    def width(self) -> int:
        return len(self.nodes[0])

    @property
    def height(self) -> int:
        return len(self.nodes)

    def get_node(self, pos: Vector) -> Node:
        return self.nodes[pos.y][pos.x]

    def get_neighbors(self, node: Node) -> list[Node]:
        return [
            self.get_node(Vector(x, y))
            for x, y in [
                (node.pos.x - 1, node.pos.y),
                (node.pos.x + 1, node.pos.y),
                (node.pos.x, node.pos.y - 1),
                (node.pos.x, node.pos.y + 1),
            ]
            if (0 <= x < self.width) and (0 <= y < self.height)
        ]

    def set_node(self, node: Node) -> None:
        self.nodes[node.pos.y][node.pos.x] = node

    def print(self) -> None:
        for row in self.nodes:
            print(row)


def get_path(matrix: Matrix) -> int:

    min_path: dict[Node, int] = {n: sys.maxsize for n in matrix.node_list}
    min_path[matrix.start] = 0

    pq = PriorityQueue()
    pq.put((matrix.start.risk, matrix.start))

    visited: set[Node] = set()

    while not pq.empty():
        _, node = pq.get()

        if node == matrix.end:
            return min_path[matrix.end]

        visited.add(node)

        neighbors = matrix.get_neighbors(node)

        for neighbor in neighbors:
            if neighbor in visited:
                continue
            old_cost = min_path[neighbor]
            new_cost = min_path[node] + neighbor.risk
            if new_cost >= old_cost:
                continue
            pq.put((new_cost, neighbor))
            min_path[neighbor] = new_cost

    # print(min_path)

    return min_path[matrix.end]


def parse_input(input_lines: list[str]) -> list[list[Node]]:

    out = []
    for y, line in enumerate(input_lines):
        out.append([Node(Vector(x, y), int(r)) for x, r in enumerate(line)])
    return out


def part_1(input_lines: list[str]):

    matrix = Matrix(parse_input(input_lines))
    path = get_path(matrix)

    return path


def calc_risk(risk: int, offset: int) -> int:

    new_risk = risk + offset
    if new_risk > 9:
        new_risk = new_risk % 9

    return new_risk


def row_pos(node: Node, offset, h: int) -> Vector:
    return Vector(node.pos.x, node.pos.y + h * offset)


def col_pos(node: Node, offset, w: int) -> Vector:
    return Vector(node.pos.x + w * offset, node.pos.y)


def extend_row(row: Path, off: int, is_row: bool, size: Vector) -> list[Node]:
    w = size.x
    h = size.y
    if is_row:
        return [Node(row_pos(n, off, h), calc_risk(n.risk, off)) for n in row]
    return [Node(col_pos(n, off, w), calc_risk(n.risk, off)) for n in row]


def expand_cave(matrix: Matrix) -> Matrix:

    size = Vector(matrix.width, matrix.height)

    cave = []
    for i in range(5):
        cell = []
        for y in range(matrix.height):
            cell.append(extend_row(matrix.nodes[y], i, True, size))
        cave.append(cell)

    for cell in cave:
        for row in cell:
            n1 = extend_row(row, 1, False, size)
            n2 = extend_row(row, 2, False, size)
            n3 = extend_row(row, 3, False, size)
            n4 = extend_row(row, 4, False, size)
            row += n1 + n2 + n3 + n4

    m2 = cave[0] + cave[1] + cave[2] + cave[3] + cave[4]

    return Matrix(m2)


def part_2(input_lines: list[str]):

    matrix = expand_cave(Matrix(parse_input(input_lines)))
    path = get_path(matrix)

    return path


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
