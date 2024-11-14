import sdl2
import sdl2.ext
import sdl2.sdlttf
from abc import ABC, abstractmethod
from typing import Callable

class View(ABC):
    @abstractmethod
    def draw(self, renderer: sdl2.ext.Renderer, font: sdl2.sdlttf.TTF_Font) -> None:
        pass

    @abstractmethod
    def is_clicked(self, x: int, y: int) -> bool:
        return False

class Button(View):
    def __init__(self, x: int, y: int, width: int, height: int, label: str, color: sdl2.SDL_Color, callback: Callable[[], None]):
        self.rect = sdl2.SDL_Rect(x, y, width, height) # type: sdl2.SDL_Rect
        self.label = label # type: str
        self.color = color # type: sdl2.SDL_Color
        self.callback = callback # type: Callable[[], None]

    def draw(self, renderer: sdl2.ext.Renderer, font: sdl2.sdlttf.TTF_Font) -> None:
        pass

    def is_clicked(self, x: int, y: int) -> bool:
        return False