from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

PREFERRED_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)


@dataclass(frozen=True)
class WinResult:
    winner: Optional[str]
    line: Optional[tuple[int, int, int]]


def empty_board() -> list[str]:
    return [""] * 9


def new_game(mode: str) -> dict:
    return {
        "mode": mode,
        "board": empty_board(),
        "current_player": "X",
        "winner": None,
        "winner_line": None,
        "draw": False,
        "message": "Player X to move",
    }


def other_player(player: str) -> str:
    return "O" if player == "X" else "X"


def check_winner(board: list[str]) -> WinResult:
    for line in WIN_LINES:
        first, second, third = line
        token = board[first]
        if token and token == board[second] == board[third]:
            return WinResult(token, line)
    return WinResult(None, None)


def is_draw(board: list[str]) -> bool:
    return all(cell for cell in board) and check_winner(board).winner is None


def available_moves(board: list[str]) -> list[int]:
    return [index for index, cell in enumerate(board) if not cell]


def apply_move(state: dict, index: int, player: str) -> bool:
    board = state["board"]
    if not 0 <= index < 9:
        state["message"] = "Choose a valid square."
        return False
    if state["winner"] or state["draw"]:
        state["message"] = "The game is already over."
        return False
    if board[index]:
        state["message"] = "That square is already taken."
        return False
    if state["current_player"] != player:
        state["message"] = f"It is {state['current_player']}'s turn."
        return False

    board[index] = player
    result = check_winner(board)
    if result.winner:
        state["winner"] = result.winner
        state["winner_line"] = list(result.line) if result.line else None
        state["message"] = f"Player {result.winner} wins!"
        return True

    if is_draw(board):
        state["draw"] = True
        state["message"] = "It is a draw."
        return True

    state["current_player"] = other_player(player)
    state["message"] = f"Player {state['current_player']} to move"
    return True


def computer_move(board: list[str], computer: str = "O") -> Optional[int]:
    human = other_player(computer)

    for index in available_moves(board):
        trial = board.copy()
        trial[index] = computer
        if check_winner(trial).winner == computer:
            return index

    for index in available_moves(board):
        trial = board.copy()
        trial[index] = human
        if check_winner(trial).winner == human:
            return index

    for index in PREFERRED_MOVES:
        if not board[index]:
            return index

    return None


def format_cell(value: str) -> str:
    return value if value else ""
