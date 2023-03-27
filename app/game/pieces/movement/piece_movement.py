from abc import ABC, abstractmethod
from typing import Tuple
from utils import Vector2d
# import game.board as b
import game.pieces as pcs


class PieceMovement(ABC):
    def __init__(self, piece: pcs.Piece, board) -> None:
        self._piece: pcs.Piece = piece
        self._board = board
        self._legal_moves: list[Vector2d] = []

    @abstractmethod
    def get_legal_moves(self) -> list[Vector2d]:
        pass

    def check_squares(
        self, piece: pcs.Piece, board, origin: Vector2d, destination: Vector2d, increment: Tuple[int, int]
    ) -> None:
        if increment[0] == 0 and increment[1] == 0:
            return

        if increment[0] == 0:
            dys = [dy for dy in range(origin.y, destination.y, increment[1])]
            dxs = [origin.x for _ in dys]
        else:
            dxs = [dx for dx in range(origin.x, destination.x, increment[0])]
            dys = [origin.y for _ in dxs]

        deltas = zip(dxs, dys)
        for dx, dy in deltas:
            pos = Vector2d(piece.position.x + dy, piece.position.y + dx)
            if not board.can_move_to(pos, piece):
                break
            self._legal_moves.append(pos)
