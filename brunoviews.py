"""The UI system for the Brunotron."""

import sdl2
import sdl2.ext
import sdl2.sdlttf
from abc import ABC, abstractmethod
from typing import Callable

WHITE = sdl2.SDL_Color(255, 255, 255)
BLACK = sdl2.SDL_Color(0, 0, 0)

PRIMARY = sdl2.SDL_Color(48, 213, 200)
SECONDARY = sdl2.SDL_Color(10, 186, 181)

def default_callback(): pass

class View(ABC):
    """The base view class.

    **Do not use this class.**
    """

    @abstractmethod
    def draw(self, renderer: sdl2.ext.Renderer, font: sdl2.sdlttf.TTF_Font) -> None:
        """Draws the view onto the screen.

        :param renderer: An SDL renderer.
        :param font: An SDL font.
        """
        pass

    @abstractmethod
    def check_clicked(self, x: int, y: int) -> bool:
        """Returns ``true`` if the view is clicked.

        You should not call this function; it will be handled automatically every frame. If you
        are sure that your view will never need to handle click events, you can make this function
        return ``false``.

        :param x: The x position of the cursor.
        :param y: The y position of the cursor.
        :return: If the view is clicked.
        """
        return False

class Button(View):
    """A class for drawing button views."""

    def __init__(self, x: int, y: int, width: int, height: int, label: str,
                 color: sdl2.SDL_Color = SECONDARY, text_color: sdl2.SDL_Color = WHITE,
                 callback: Callable[[], None] = default_callback):
        self.rect = sdl2.SDL_Rect(x, y, width, height) # type: sdl2.SDL_Rect
        self.label = label # type: str
        self.color = color # type: sdl2.SDL_Color
        self.text_color = text_color # type: sdl2.SDL_Color
        self.callback = callback # type: Callable[[], None]

    def draw(self, renderer: sdl2.ext.Renderer, font: sdl2.sdlttf.TTF_Font) -> None:
        renderer.fill(self.rect, self.color)
        surface = sdl2.sdlttf.TTF_RenderText_Solid(font, self.label.encode(), self.text_color)
        texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
        text_rect = sdl2.SDL_Rect(
            self.rect.x + (self.rect.w - surface.contents.w) // 2,
            self.rect.y + (self.rect.h - surface.contents.h) // 2,
            surface.contents.w,
            surface.contents.h
        )
        sdl2.SDL_FreeSurface(surface)
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, texture, None, text_rect)
        sdl2.SDL_DestroyTexture(texture)

    def check_clicked(self, x: int, y: int) -> bool:
        """Returns true if the button is clicked.

        You should not call this function; it will be handled automatically every frame.

        :param x: The x position of the cursor.
        :param y: The y position of the cursor.
        :return: If the view is clicked.
        """
        return False