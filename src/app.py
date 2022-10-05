import math
from typing import Tuple

import pygame

from window import Window
from menu import Menu
from result import Result
from game import Game, State


class App:
    def __init__(self,
            title: str,
            resolution: Tuple[int, int],
            board_size: Tuple[int, int],
            field_spacing: int,
            font_size: int,
        ) -> None:
        
        self._board_size = board_size
        self._field_spacing = field_spacing

        self._window = Window(title, resolution, font_size)
        self._menu = Menu(self._window, math.prod(board_size))

        self._reset_state()


    def _reset_state(self) -> None:
        self._menu.reset()
        
        self._game = None
        self._results = None
        
        self._game_running = False
        self._game_finished = False


    def run(self) -> None:
        running = True
        while running:
            for event in self._window.get_events():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            if self._game_finished:
                self._results.update()
                self._results.render()
                
                if self._results.is_closed:
                    self._reset_state()
                    continue

            elif self._game_running:
                self._game.update()
                self._game.render()

                if self._game.state == State.FINISHED:
                    self._results = Result(
                        self._window,
                        self._game.get_finish_times()
                    )

                    self._game_finished = True
                
            else:
                self._menu.update()
                self._menu.render()

                if self._menu.game_start:
                    values = self._menu.get_values()
                    print(values)
                    
                    self._game = Game(
                        self._window,
                        values["numbers"],
                        self._field_spacing,
                        self._board_size,
                        values["preview"],
                        values["rounds"],
                    )

                    self._game_running = True

            self._window.update()