from string import ascii_letters, digits
from typing import Union, Dict

import pygame

from window import Window


_valid_chars = ascii_letters + digits


class ValueBox:
    def __init__(self,
            x: int,
            y: int,
            width: int,
            height: int,
            start_value: Union[int, float] = None
        ) -> None:
        
        self._rect = pygame.Rect(x, y, width, height)
        
        if start_value is None:
            start_value = "0"
        
        self.value = str(start_value)
        self._invalid_value = False


    @property
    def invalid_value(self) -> bool:
        return self._invalid_value


    @invalid_value.setter
    def invalid_value(self, value: bool) -> None:
        self._invalid_value = value


    @property
    def rect(self) -> pygame.Rect:
        return self._rect


    @property
    def value(self) -> str:
        return self._value
    

    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value


class Menu:
    def __init__(self, window: Window, max_number: int) -> None:
        self._window = window
        self._max_number = max_number

        self._value_boxes = {
            "rounds": ValueBox(50, 100, 150, 150, "1"),
            "preview": ValueBox(225, 100, 150, 150, "1"),
            "numbers": ValueBox(400, 100, 150, 150, "3")
        }

        self._start_button = pygame.Rect(175, 450, 250, 75)

        self.reset()


    def reset(self) -> None:
        self._values = None
        self._game_has_started = False
        self._selected_box = None


    @property
    def game_start(self) -> bool:
        return self._game_has_started


    def get_values(self) -> Dict[str, int]:
        return self._values


    def _start_game(self) -> None:
        errors = False
        numerics = [int, float, int]

        values = {}
        for number_type, (name, box) in zip(numerics, self._value_boxes.items()):
            try:
                values[name] = number_type(box.value)
                box.invalid_value = False
            except Exception:
                box.invalid_value = True
                errors = True
        
        if values["numbers"] == 0 or values["numbers"] > self._max_number:
            self._value_boxes["numbers"].invalid_value = True
            errors = True

        if not errors:
            self._game_has_started = True
            self._values = values
    

    def render(self) -> None:
        for name, valuebox in self._value_boxes.items():
            if valuebox.invalid_value:
                outer_line = valuebox.rect.copy()

                outer_line.x -= 5
                outer_line.y -= 5
                outer_line.w += 10
                outer_line.h += 10

                self._window.render_block(outer_line, (255, 0, 0))

            if valuebox is self._selected_box:
                color = (150, 150, 150)
            else:
                color = (100, 100, 100)

            self._window.render_block(valuebox.rect, color)
            self._window.render_text(valuebox.value, valuebox.rect.center)
            
            text_pos = valuebox.rect.copy()
            text_pos.y += 125
            
            self._window.render_text(name.capitalize(), text_pos.center)

        self._window.render_block(self._start_button, (100, 100, 100))
        self._window.render_text("Start Game", self._start_button.center)
    

    def update(self) -> None:
        if self._window.get_mouse_click():
            mouse_pos = self._window.get_mouse_pos()
            box_clicked = False
            
            for valuebox in self._value_boxes.values():
                if valuebox.rect.collidepoint(mouse_pos):
                    if self._window.get_mouse_click():
                        self._selected_box = valuebox
                        box_clicked = True
                    else:
                        self._selected_box = None
        
            if not box_clicked:
                self._selected_box = None
            
                if self._start_button.collidepoint(mouse_pos):
                    self._start_game()

        pressed_keys = self._window.get_pressed_keys()

        if self._selected_box is not None:
            for key_event in pressed_keys:
                if key_event.key == pygame.K_BACKSPACE:
                    self._selected_box.value = self._selected_box.value[:-1]
                
                elif key_event.key == pygame.K_PERIOD:
                    self._selected_box.value += "."

                else:
                    if (letter := key_event.unicode) in _valid_chars:
                        self._selected_box.value += letter.lower()