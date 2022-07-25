from dataclasses import dataclass
from itertools import product


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


@dataclass
class Node:
    name: str

    @property
    def is_small(self) -> bool:
        return False if self.name.isupper() else True

    def __post_init__(self) -> None:
        self.adjacent: list[Node]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.name == __o.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name


Path = list[Node]


@dataclass
class Graph:
    nodes: dict[Node, set[Node]]

    def add_edge(self, edge: list[Node]) -> None:
        n1, n2 = edge
        self.nodes[n1].add(n2)
        self.nodes[n2].add(n1)


def bfs(node: Node, paths: list[Path], graph: Graph) -> list[Path]:

    valid = [p for p in paths if p[-1] != Node("end") and p[-1] == node]
    other = [p for p in paths if p not in valid]

    if not valid:
        return paths

    children = graph.nodes[node]
    small = [child for child in children if child.is_small]
    big = [child for child in children if not child.is_small]

    extended = [p[0] + [p[1]] for p in product(valid, big)]

    for child in small:
        for path in valid:
            if not child:
                continue
            if path.count(child) == 1:
                continue
            extended += [path + [child]]

    new_paths = other + extended

    for child in children:
        if child != Node("end"):
            new_paths = bfs(child, new_paths, graph)

    return new_paths


def validate_path(path: Path) -> bool:

    if path.count(Node("start")) > 1:
        return False

    small_caves = {cave: path.count(cave) for cave in path if cave.is_small}
    for v in small_caves.values():
        if v > 2:
            return False
    double_visits = len([v for v in small_caves.values() if v > 1])

    return True if double_visits <= 1 else False


def bfs2(node: Node, paths: list[Path], graph: Graph) -> list[Path]:

    valid = [p for p in paths if p[-1] == node and p[-1] != Node("end")]
    other = [p for p in paths if p not in valid]

    if not valid:
        return paths

    children = [i for i in graph.nodes[node] if i != Node("start")]
    big = [cave for cave in children if not cave.is_small]
    small = [cave for cave in children if cave.is_small]

    big_paths = [p[0] + [p[1]] for p in product(valid, big)]
    small_paths = [p[0] + [p[1]] for p in product(valid, small)]
    valid_small = [path for path in small_paths if validate_path(path)]

    new_paths = other + big_paths + valid_small
    for child in children:
        new_paths = bfs2(child, new_paths, graph)

    return new_paths


def parse_edges(edge: str) -> list[Node]:
    return [Node(node) for node in edge.split("-")]


def load_nodes(nodes: list[Node]) -> set[Node]:
    return {node for node in nodes}


def create_graph(edges: list[str]) -> Graph:
    nodes = {node: set() for line in edges for node in parse_edges(line)}
    graph = Graph(nodes)
    [graph.add_edge(parse_edges(edge)) for edge in edges]
    return graph


def part_1(input_lines: list[str]):
    graph = create_graph(input_lines)
    start = Node("start")
    paths = bfs(start, [[start]], graph)

    for p in paths:
        print(p)

    return len(paths)


def part_2(input_lines: list[str]):
    graph = create_graph(input_lines)
    start = Node("start")
    paths = bfs2(start, [[start]], graph)

    # for p in paths:
    #     print(p)
    return len(paths)


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
