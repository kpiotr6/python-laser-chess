from __future__ import annotations
from utils import BoardVector2d
import game.piece as pcs
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.piece.move import PieceMoveType


class PieceMove:
    def __init__(self, piece: pcs.Piece = None, origin: BoardVector2d = None, destination: BoardVector2d = None,
                 promotion: pcs.Piece | None = None, move_type: PieceMoveType = None) -> None:
        if piece is None:
            self.move: int = None
        else:
            self.move: int = piece.player_id
        self.piece: pcs.Piece = piece
        self.origin: BoardVector2d = origin
        self.destination: BoardVector2d = destination
        self.promotion = promotion
        self.move_type = move_type
