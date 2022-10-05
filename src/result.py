from typing import Sequence

import pygame

from window import Window


class Result:
    def __init__(self, window: Window, results: Sequence[float]) -> None:
        self._window = window
        self._results = sorted(results, key=lambda i: (i is None, i))[:10]

        self._scoreboard_scroll = 0

        w, h = self._window.get_size()
        
        self._scoreboard_rect = pygame.Rect(100, 100, w-200, h-200)
        self._scoreboard_surf = pygame.Surface(self._scoreboard_rect.size)
        
        self._closed = False


    @property
    def is_closed(self) -> bool:
        return self._closed


    def render(self) -> None:
        w, h = self._window.get_size()

        center_x_screen = (w / 2)
        center_x_scoreboard = self._scoreboard_rect.w / 2
        
        self._window.render_text("Scoreboard", (center_x_screen, 50))
        self._window.render_text("Press Esq to return", (center_x_screen, h - 50))

        self._scoreboard_surf.fill((50, 50, 50))

        spacing = self._scoreboard_rect.height / 11

        for index, value in enumerate(self._results):
            y = (spacing * index) + spacing

            if value is None:
                value = "Fail"

            self._window.render_text(
                str(value),
                (center_x_scoreboard, y),
                self._scoreboard_surf
            )

        self._window.render_surface(
            self._scoreboard_surf,
            self._scoreboard_rect
        )

    

    def update(self) -> None:
        pressed_keys = self._window.get_pressed_keys()

        for key_event in pressed_keys:
            print(key_event)
            if key_event.key == pygame.K_ESCAPE:
                self._closed = True