from typing import Sequence, Tuple

import pygame


class Window:
    def __init__(self,
            title: str,
            resolution: Tuple[int, int],
            font_size: int
        ) -> None:
        
        pygame.init()
        pygame.display.set_caption(title)
        
        self._display = pygame.display.set_mode(
            resolution, pygame.SCALED | pygame.RESIZABLE
        )

        self._font = pygame.font.Font(
            pygame.font.get_default_font(),
            font_size
        )
        
        self._key_presses = []
        self._clock = pygame.time.Clock()
        self._resolution = resolution


    def get_size(self) -> Tuple[int, int]:
        return self._resolution


    def get_mouse_pos(self) -> Sequence[pygame.event.Event]:
        return pygame.mouse.get_pos()


    def get_mouse_click(self) -> bool:
        return pygame.mouse.get_pressed()[0]


    def get_pressed_keys(self) -> Sequence[pygame.event.Event]:
        return self._key_presses


    def get_events(self) -> Sequence[pygame.event.Event]:
        events = pygame.event.get()
        
        key_presses = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                key_presses.append(event)
        
        self._key_presses = key_presses

        return events


    def render_surface(self,
            surface: pygame.Surface,
            rect: pygame.Rect
        ) -> None:
        
        self._display.blit(surface, rect)


    def render_block(self,
            rect: pygame.Rect,
            color: Tuple[int, int, int]
        ) -> None:

        pygame.draw.rect(self._display, color, rect)


    def render_text(self,
            text: str,
            pos: Tuple[int, int],
            dest_surf: pygame.Surface = None
        ) -> None:
        
        if dest_surf is None:
            dest_surf = self._display

        surface = self._font.render(text, True, (255, 255, 255))

        rect = surface.get_rect()
        rect.center = pos

        dest_surf.blit(surface, rect)


    def update(self) -> None:
        pygame.display.update()
        self._display.fill((25, 25, 25))
        self._clock.tick(60)