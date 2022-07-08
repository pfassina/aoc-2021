from dataclasses import dataclass


@dataclass
class FishCounter:
    initial_count: list[int]

    def __post_init__(self) -> None:
        self.fishes = {i: 0 for i in range(9)}
        for fish in self.initial_count:
            self.fishes[fish] += 1

    def mature(self) -> None:

        new_day = {i: 0 for i in range(9)}

        for maturity, fish in self.fishes.items():
            if maturity == 0:
                new_day[6] += fish
                new_day[8] += fish
            else:
                new_day[maturity - 1] += fish

        self.fishes = new_day

    @property
    def fish_count(self) -> int:
        return sum(f for f in self.fishes.values())


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def part_1(input_lines: list[str]):

    day_count = 80
    days = [[] for _ in range(day_count + 1)]
    days[0] = [int(i) for i in input_lines[0].split(",")]

    for n in range(len(days)):
        if n == 0:
            continue

        new_fish = [8 for f in days[n - 1] if f == 0]
        days[n] = [f - 1 if f > 0 else 6 for f in days[n - 1]] + new_fish

    return len(days[-1])


def part_2(input_lines: list[str]):

    initial_state = [int(i) for i in input_lines[0].split(",")]
    fc = FishCounter(initial_state)

    day = 256
    for _ in range(day):
        fc.mature()

    return fc.fish_count


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
