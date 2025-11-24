import random
from abc import ABC, abstractmethod
from enum import Enum
from itertools import cycle, product

WELCOME_SCREEN = """
TickTackToe

1) Play
2) Stats
3) Exit
"""
SEP_LINE = "█" * 32


class Figure(Enum):
    NONE = " "
    CROSS = "x"
    NOUGHT = "o"


def convert(figure: Figure) -> str:
    return figure.value


class MoveResult(Enum):
    INVALID = 0
    SUCCESS = 1
    GAME_END = 2


class GameBoard:
    def __init__(self, size: int):
        self.size = size
        self.__empty_cells_amount = size ** 2
        self.__board: list[list[Figure]] = [[Figure.NONE] * size for _ in range(size)]
        self.winner: Figure = Figure.NONE

    def move(self, x: int, y: int, player: Figure) -> MoveResult:
        if player == Figure.NONE:
            return MoveResult.INVALID
        try:
            if self.__board[x][y] != Figure.NONE:
                return MoveResult.INVALID
        except IndexError:
            return MoveResult.INVALID

        self.__board[x][y] = player
        self.__empty_cells_amount -= 1

        if self.__is_win(x, y, player):
            self.winner = player
            return MoveResult.GAME_END

        return MoveResult.SUCCESS if self.__empty_cells_amount > 0 else MoveResult.GAME_END

    def get_all_empty(self) -> tuple[tuple[int, int], ...]:
        return tuple((x, y) for x, y in product(range(self.size), repeat=2) if self.__board[x][y] == Figure.NONE)

    def print(self):
        middle = "  ┣" + "╋".join(["━━━"] * self.size) + "┫"

        print("   y" + "   ".join(map(str, list(range(self.size)))))
        print("x ┏" + "┳".join(["━━━"] * self.size) + "┓")
        for i in range(self.size):
            print(str(i) + " ┃ " + " ┃ ".join(map(convert, self.__board[i])) + " ┃")
            if i < self.size - 1:
                print(middle)
        print("  ┗" + "┻".join(["━━━"] * self.size) + "┛")

    def __is_win(self, x: int, y: int, player: Figure) -> bool:
        # |
        if all(self.__board[x][i] == player for i in range(self.size)):
            return True
        # -
        if all(self.__board[i][y] == player for i in range(self.size)):
            return True
        # \
        if x == y and all(self.__board[i][i] == player for i in range(self.size)):
            return True
        # /
        m = self.size - 1
        if x + y == m and all(self.__board[i][m - i] == player for i in range(self.size)):
            return True
        return False


class Player(ABC):
    def __init__(self, name: str, figure: Figure = Figure.NONE):
        self.name = name
        self.figure = figure

    @abstractmethod
    def on_move(self, board: GameBoard) -> MoveResult:
        pass


class RealPlayer(Player):
    def __init__(self, name: str, figure: Figure = Figure.NONE):
        super().__init__(name, figure)

    def on_move(self, board: GameBoard) -> MoveResult:
        print(SEP_LINE)
        print(f"Ход {self.name} ({convert(self.figure)})")
        board.print()

        return board.move(get_int_input("x: ", 0, board.size - 1), get_int_input("y: ", 0, board.size - 1), self.figure)


class AIPlayer(Player):
    def __init__(self, figure: Figure = Figure.NONE):
        super().__init__("BOT", figure)

    def on_move(self, board: GameBoard) -> MoveResult:
        x, y = random.choice(board.get_all_empty())
        return board.move(x, y, self.figure)


def get_int_input(text: str, min: int, max: int):
    while True:
        try:
            num = int(input(text))
            if min <= num <= max:
                return num
            print(f"[!] Число должно быть больше или равно {min} и меньше или равно {max}!")
        except Exception:
            print("[!] Не удалось преобразовать в число!")
            continue


def game_screen(size: int, bot: bool) -> None:
    pre_players = [RealPlayer("Player1"), AIPlayer() if bot else RealPlayer("Player2")]
    random.shuffle(pre_players)
    pre_players[0].figure = Figure.CROSS
    pre_players[1].figure = Figure.NOUGHT

    players = cycle(pre_players)
    game_board = GameBoard(size)
    res = MoveResult.SUCCESS
    player = next(players)
    while res != MoveResult.GAME_END:
        res = player.on_move(game_board)
        if res == MoveResult.SUCCESS:
            player = next(players)
        elif res == MoveResult.INVALID:
            print("[!] Не удалось выполниить ход!")

    print("Выиграл " + convert(game_board.winner) if game_board.winner != Figure.NONE else "Ничья")
    update_stats(1, 1 if bot else 0)


def read_stats() -> tuple[int, int]:
    try:
        with open("stats.txt", 'r', encoding='utf-8') as file:
            res = tuple(map(int, file.readline().replace("\n", "").split("|")))
            return res if len(res) == 2 else (0, 0)
    except Exception:
        return 0, 0


def update_stats(games: int, bot_games: int) -> None:
    stats = read_stats()
    with open("stats.txt", 'w', encoding='utf-8') as file:
        file.write(f"{stats[0] + games}|{stats[1] + bot_games}")


def stats_screen() -> None:
    stats = read_stats()
    print("STATS")
    print("Всего игр:", stats[0])
    print("Игр против бота:", stats[1])


if __name__ == "__main__":
    while True:
        print(SEP_LINE)
        print(WELCOME_SCREEN)
        match get_int_input("> ", 1, 3):
            case 1:
                print(SEP_LINE)
                print("Game settings\n")
                size = get_int_input("Размер поля: ", 3, 9)
                print("\nС кем играть?\n1) против игрока\n2) против бота")
                bot = bool(get_int_input("> ", 1, 2) - 1)
                game_screen(size, bot)
            case 2:
                print(SEP_LINE)
                stats_screen()
            case 3:
                break
