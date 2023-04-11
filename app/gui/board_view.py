from typing import Any, Optional, Tuple
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import Callback
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from utils import Vector2d, rgba_int_to_float
import game as g
import game.piece as pcs
import game.observer as obs
from numpy import empty
from gui.piece_representation import PieceRepresentationLayout
from game.piece.piece import Piece


class MetaAB(type(obs.PositionObserver), type(Screen)):
    pass


class Board(obs.PositionObserver, Screen, metaclass=MetaAB):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = g.Game()
        self._grid = self.ids.board
        self._dots = empty(shape=27, dtype=Image)
        self._representations = empty(shape=(8, 8), dtype=PieceRepresentationLayout)
        self._current_dots = []
        self._init_board()
        self._selected = None
        self._selected_piece = None
        self._board = self._game.board

    def _init_board(self):
        board = self._game.board
        for i in range(len(self._dots)):
            self._dots[i] = Image(source="assets/dot.png")
        for i in range(8):
            for j in range(8):
                vector = Vector2d(j, 7 - i)

                # preparation of every button on board

                button = Button()
                button.vector = vector
                button.bind(on_press=self.on_tile_click)
                button.background_normal = ""
                if (i + j) % 2 == 0:
                    button.background_color = rgba_int_to_float((150, 50, 50, 255))
                else:
                    button.background_color = rgba_int_to_float((54, 54, 54, 255))

                # assigning observer to piece

                piece = board.get_piece(vector)
                if piece is not None:
                    piece.add_observer(self)

                # adding piece and button to board

                piece_layout = PieceRepresentationLayout(piece, button)
                self._grid.add_widget(piece_layout)
                self._representations[vector.y][vector.x] = piece_layout

    def _show_checks(self):
        check = Image(source="assets/this_fire.png")
        for king in self._board.kings:
            if self._board.is_king_under_check(king.player_id):
                vector = king.position
                self._representations[vector.y][vector.x].add_indicator(check)

    def on_tile_click(self, instance: Button):

        # clear indicating dots

        for d in self._current_dots:
            d.parent.remove_widget(d)
        self._current_dots.clear()

        # other piece

        piece = self._board.get_piece(instance.vector)
        if piece is not None and piece.player_id == self._board.move_number:
            self._selected_piece = self._board.get_piece(instance.vector)
            self._selected = self._board.get_piece_movement(instance.vector)
            self.on_show_possible_movements(self._selected.get_legal_moves())
            return

        # no piece selected
        self._game.move_piece(self._selected_piece, instance.vector)
        self._selected = None
        self._selected_piece = None

    def on_show_possible_movements(self, movements: list[list[Vector2d]]):
        i = 0
        print(movements)
        for row in movements:
            for m in row:
                self._representations[m.y][m.x].add_widget(self._dots[i])
                self._current_dots.append(self._dots[i])
                i += 1


    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        for i in range(len(self._representations)):
            for j in range(len(self._representations[i])):
                self._representations[i][j].remove_indicator()
                self._representations[i][j].remove_img()
                self._representations[i][j].new_image(self._board.get_piece(Vector2d(j, i)))
        self._show_checks()

    def update_representation(self, from_piece: pcs.Piece, to_piece: pcs.Piece):
        pass
