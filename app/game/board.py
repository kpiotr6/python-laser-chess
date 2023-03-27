from typing import Dict, Optional, Tuple
from utils import Vector2d
import game as g
import game.pieces as pcs
import game.pieces.movement as pm
import game.observer as obs


class Board(obs.PositionObserver):
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._move_number: int = 0
        self._pieces: Dict[Vector2d, Tuple[pcs.Piece, pm.PieceMovement]] = {}

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    @property
    def move_number(self) -> int:
        return self._move_number

    @move_number.setter
    def move_number(self, value: int) -> None:
        self._move_number = value

    # override PositionObserver
    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        p = self._pieces
        p.pop(origin, None)
        p[destination] = p.pop(origin)

    def get_size(self) -> tuple[int, int]:
        return self._width, self._height

    def get_piece(self, position: Vector2d) -> Optional[pcs.Piece]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[0]

    def get_piece_movement(self, position: Vector2d) -> Optional[pm.PieceMovement]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[1]

    def can_move_to(self, to: Vector2d, piece: Optional[pcs.Piece] = None) -> bool:
        #
        # Check, if position after moving is in bounds of board
        #
        if to.x < 0 or to.x >= self.width or to.y < 0 or to.y >= self.height:
            return False

        #
        # Move with potential capturing
        #
        if isinstance(piece, pcs.Piece):
            p = self.get_piece(to)
            return True if not p or p.player_id != piece.player_id else False
        #
        # Move without capturing
        #
        else:
            return True if not self.get_piece(to) else False

    def add_piece(self, piece: Tuple[pcs.Piece, pm.PieceMovement]) -> None:
        if not self.get_piece(piece[0].position):
            self._pieces[piece[0].position] = piece
            piece[0].add_observer(self)

    def add_pieces(self, pieces: list[Tuple[pcs.Piece, pm.PieceMovement]]) -> None:
        for piece in pieces:
            self.add_piece(piece)




