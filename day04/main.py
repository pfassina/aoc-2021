from dataclasses import dataclass


@dataclass
class Draws:
    raw_input: str

    @property
    def draws(self) -> list[int]:
        return [int(i) for i in self.raw_input.split(",")]


@dataclass
class Board:
    layout: list[list[int]]

    def __post_init__(self):
        self.score_board: list[list[int]] = [
            [0 for _ in range(5)] for _ in range(5)
        ]  # noqa

    def score(self, n):
        for i, line in enumerate(self.layout):
            for j, number in enumerate(line):
                if number == n:
                    self.score_board[i][j] = 1

    def check_win(self) -> bool:
        row = [sum(line) for line in self.score_board]
        col = [sum([line[n] for line in self.score_board]) for n in range(5)]

        if 5 in row:
            return True
        if 5 in col:
            return True

        return False

    def final_score(self, n):
        unmarked = [
            [n for j, n in enumerate(row) if self.score_board[i][j] == 0]
            for i, row in enumerate(self.layout)
        ]
        return sum(sum(row) for row in unmarked) * n


@dataclass
class Boards:
    raw_input: list[str]

    @property
    def flat_boards(self):
        return [
            [int(n) for n in line.split(" ") if n != ""]
            for line in self.raw_input
            if line != ""
        ]

    @property
    def boards(self) -> list[Board]:
        return [Board(list(i)) for i in zip(*[iter(self.flat_boards)] * 5)]

    def board(self, n: int) -> Board:
        return self.boards[n]


def read_file(path) -> list[str]:
    with open(path, "r") as file:
        return file.read().splitlines()


def part_1(input_lines: list[str]):

    draws = Draws(input_lines[0]).draws
    boards = Boards(input_lines[2:]).boards

    winners = []
    final_draw = 0

    for draw in draws:
        for n, board in enumerate(boards):
            board.score(draw)
            if board.check_win():
                winners.append(n)
        if winners:
            final_draw = draw
            break

    return boards[winners[0]].final_score(final_draw)


def part_2(input_lines: list[str]):
    draws = Draws(input_lines[0]).draws
    boards = Boards(input_lines[2:]).boards

    winners = []
    final_draw = 0

    for draw in draws:
        for n, board in enumerate(boards):
            if n in winners:
                continue
            board.score(draw)
            if board.check_win():
                winners.append(n)
        if len(winners) == len(boards):
            final_draw = draw
            break

    return boards[winners[-1]].final_score(final_draw)


if __name__ == "__main__":
    inp = read_file("input.txt")
    out = part_2(inp)
    print(out)
