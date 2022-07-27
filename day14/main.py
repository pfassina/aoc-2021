from dataclasses import dataclass


@dataclass
class Element:
    name: str

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Element):
            return self.name == __o.name
        return False

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Pair:
    first: Element
    second: Element

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Pair):
            return self.first == __o.first and self.second == __o.second
        return False

    def __repr__(self) -> str:
        return f"{self.first}{self.second}"

    def __hash__(self) -> int:
        return hash(f"{self.first}{self.second}")


@dataclass
class Rules:
    pairs: dict[Pair, Element]

    def is_pair(self, pair: Pair) -> bool:
        return pair in self.pairs

    def polymer(self, pair: Pair) -> Element:
        return self.pairs[pair]

    def __repr__(self) -> str:
        return "\n".join([f"{k} -> {v}" for k, v in self.pairs.items()])

    def children(self, pair: Pair) -> tuple[Pair, Pair]:
        a = Pair(pair.first, self.pairs[pair])
        b = Pair(self.pairs[pair], pair.second)
        return a, b


@dataclass
class Template:
    elements: list[Element]

    def __post_init__(self) -> None:
        self.element_count = {e: self.elements.count(e) for e in self.elements}
        self.pair_dict: dict[Pair, int] = self.create_pair_dict()

    def add_element(self, index: int, element: Element) -> int:
        self.elements.insert(index, element)
        self.add_count(element)
        return 1

    def add_count(self, element: Element) -> None:
        if element in self.element_count:
            self.element_count[element] += 1
        else:
            self.element_count[element] = 1

    def create_pair_dict(self) -> dict[Pair, int]:
        pair_dict = {}
        for i in range(1, self.length):
            a = self.elements[i - 1]
            b = self.elements[i]
            pair = Pair(a, b)
            pair_dict[pair] = 1 + pair_dict.get(pair, 0)
        return pair_dict

    @property
    def length(self) -> int:
        return len(self.elements)

    @property
    def most_common_qty(self) -> int:
        return max([e for e in self.element_count.values()])

    @property
    def least_common_qty(self) -> int:
        return min([e for e in self.element_count.values()])

    def quantity(self, element: Element) -> int:
        return self.elements.count(element)

    def __repr__(self) -> str:
        return "".join([e.name for e in self.elements])


def parse_template(template: "str") -> Template:
    return Template([Element(e) for e in template])


def parse_line(line: str) -> tuple[Pair, Element]:
    pair = Pair(*[Element(e) for e in line.split(" ")[0]])
    element = Element(line.split(" ")[2])
    return pair, element


def parse_rules(rules: list["str"]) -> Rules:
    return Rules({parse_line(rule)[0]: parse_line(rule)[1] for rule in rules})


def parse_input(input_lines: list["str"]) -> tuple[Template, Rules]:
    template = parse_template(input_lines[0])
    rules = parse_rules(input_lines[2:])
    return template, rules


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def take_step(template: Template, rules: Rules) -> Template:

    i = 1
    while i < template.length:
        a = template.elements[i - 1]
        b = template.elements[i]
        pair = Pair(a, b)
        if rules.is_pair(pair):
            element = rules.polymer(pair)
            i += template.add_element(i, element)
        i += 1

    return template


def take_step2(template: Template, rules: Rules) -> Template:

    # 1588
    changes = {}
    for pair, qty in template.pair_dict.items():
        if qty == 0:
            continue
        a, b = rules.children(pair)
        changes[a] = changes.get(a, 0) + qty
        changes[b] = changes.get(b, 0) + qty
        changes[pair] = changes.get(pair, 0) - qty

    for pair, qty in changes.items():
        template.pair_dict[pair] = template.pair_dict.get(pair, 0) + qty

    return template


def part_1(input_lines: list[str]):
    template, rules = parse_input(input_lines)

    for i in range(10):
        template = take_step(template, rules)
        print(i)

    return template.most_common_qty - template.least_common_qty


def part_2(input_lines: list[str]):
    template, rules = parse_input(input_lines)

    for _ in range(40):
        take_step2(template, rules)

    elements = {v: 0 for v in rules.pairs.values()}
    for pair, qty in template.pair_dict.items():
        a, b = pair.first, pair.second
        elements[a] += 1 * qty
        elements[b] += 1 * qty

    print(elements)
    most = max(v for v in elements.values())
    least = min(v for v in elements.values())

    return (most - least) / 2


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
