from time import time
from random import choice
from enum import Enum, auto
from typing import Union, Sequence, Tuple, Dict

import pygame

from window import Window


class State(Enum):
    NONE = auto()
    PREVIEW = auto()
    RUNNING = auto()
    VICTORY = auto()
    DEFEAT = auto()
    FINISHED = auto()


class Game:
    def __init__(self,
            window: Window,
            number_range: int,
            field_spacing: int,
            board_size: Tuple[int, int],
            preview_time: int,
            game_rounds: int = 1,
        ) -> None:

        self._window = window
        self._number_range = number_range
        self._field_spacing = field_spacing
        self._board_size = board_size
        self._preview_time = preview_time
        
        self._total_rounds = game_rounds
        self._current_round = 0

        total_fields = (board_size[0] * board_size[1])

        if total_fields < self._number_range:
            raise ValueError("number_range argument exceeds the board_size argument")
        
        elif total_fields == 0:
            raise ValueError("field must at least be a 1 x 1")

        space_x, space_y = self._window.get_size()

        if field_spacing > 0:
            space_x -= (field_spacing * board_size[0]) + field_spacing
            space_y -= (field_spacing * board_size[1]) + field_spacing

        self._block_size = (space_x / board_size[0], space_y / board_size[1])

        self._finish_times = []
        self._state = State.NONE


    @property
    def state(self) -> auto:
        return self._state


    def _create_field(self) -> Sequence[pygame.Rect]:
        field = []

        x_offset = y_offset = self._field_spacing

        for _ in range(self._board_size[0]):
            for _ in range(self._board_size[1]):
                field.append(
                    pygame.Rect(
                        x_offset,
                        y_offset,
                        self._block_size[0],
                        self._block_size[1]
                    )
                )

                y_offset += (self._field_spacing + self._block_size[1])
            
            y_offset = self._field_spacing
            x_offset += (self._field_spacing + self._block_size[0])
        
        return field


    def _choose_number_rects(self, number_range: int) -> Dict[int, pygame.Rect]:
        numbers = {}
        available = [rect for rect in self._field]

        for num in range(1, number_range+1):
            rect = choice(available)
            available.remove(rect)
            numbers[num] = rect
        
        return numbers


    def _start_game(self) -> None:
        self._time_until_start = time() + self._preview_time
        self._start_time = None
        self._time_until_next = None
        self._state = State.PREVIEW

    
    def _create_new_game(self) -> None:
        # create an array of rects that make up the field
        self._field = self._create_field()

        # choose rects that will contain numbers
        self._numbered_rects = self._choose_number_rects(self._number_range)

        # keep track of last clicked rect to show what choice were wrong
        self._last_rect_clicked = None

        # the current number that must be pressed
        self._current_number = 1

        # sets game state and sets timers
        self._start_game()

    
    def _render_numbers(self) -> None:
        for number, rect in self._numbered_rects.items():
            self._window.render_text(
                str(number),
                rect.center
            )


    def get_current_time(self) -> None:
        return time() - self._start_time


    def get_finish_times(self) -> Union[None, Sequence[float]]:
        if self._state is State.FINISHED:
            return self._finish_times
        return None


    def render(self) -> None:
        if self._state not in (State.NONE, State.FINISHED):
            if self._state is not State.FINISHED:
                if self._state is State.DEFEAT:
                    self._window.render_block(self._last_rect_clicked, (255, 0, 0))

                self._render_numbers()
                
                if self._state is State.RUNNING:
                    mouse_pos = self._window.get_mouse_pos()

                    for rect in self._field:
                        if rect.collidepoint(*mouse_pos):
                            color = (200, 200, 200)
                        else:
                            color = (150, 150, 150)

                        self._window.render_block(rect, color)
        

    def update(self) -> None:
        if self._state is State.NONE:
            if self._current_round < self._total_rounds:
                self._current_round += 1
                self._create_new_game()
            else:
                self._state = State.FINISHED

        else:
            if self._state is State.PREVIEW and time() >= self._time_until_start:
                self._state = State.RUNNING
                self._start_time = time()
                return
            
            if self._window.get_mouse_click():
                if self._state is State.RUNNING:
                    mouse_pos = self._window.get_mouse_pos()

                    finished_rect = None
                    for rect in self._field:
                        if rect.collidepoint(*mouse_pos):
                            self._last_rect_clicked = rect

                            if rect is not self._numbered_rects[self._current_number]:
                                self._state = State.DEFEAT
                                self._finish_times.append(None)

                            else:
                                self._current_number += 1
                                finished_rect = rect

                                if self._current_number not in self._numbered_rects:
                                    self._state = State.VICTORY
                                    self._finish_times.append(round(self.get_current_time(), 3))
                            
                            break
                    
                    if finished_rect is not None:
                        self._field.remove(finished_rect)

            if self._state in (State.VICTORY, State.DEFEAT):
                if self._time_until_next is None:
                    self._time_until_next = time() + 2
                else:
                    if time() >= self._time_until_next:
                        self._state = State.NONE