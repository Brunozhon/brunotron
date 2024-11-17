"""The UI system for the Brunotron."""

import sdl2
import sdl2.ext
import sdl2.sdlttf
from abc import ABC, abstractmethod
from typing import Callable

#  ██████   ███████  ██        ███████  ████████   ██████
# ██    ██ ██     ██ ██       ██     ██ ██     ██ ██    ██
# ██       ██     ██ ██       ██     ██ ██     ██ ██
# ██       ██     ██ ██       ██     ██ ████████   ██████
# ██       ██     ██ ██       ██     ██ ██   ██         ██
# ██    ██ ██     ██ ██       ██     ██ ██    ██  ██    ██
#  ██████   ███████  ████████  ███████  ██     ██  ██████

WHITE = sdl2.SDL_Color(255, 255, 255)
BLACK = sdl2.SDL_Color(0, 0, 0)

PRIMARY = sdl2.SDL_Color(48, 213, 200)
SECONDARY = sdl2.SDL_Color(10, 186, 181)
TERTIARY = sdl2.SDL_Color(0, 139, 139)

# ████████ ██     ██ ██    ██  ██████  ████████ ████  ███████  ██    ██  ██████
# ██       ██     ██ ███   ██ ██    ██    ██     ██  ██     ██ ███   ██ ██    ██
# ██       ██     ██ ████  ██ ██          ██     ██  ██     ██ ████  ██ ██
# ██████   ██     ██ ██ ██ ██ ██          ██     ██  ██     ██ ██ ██ ██  ██████
# ██       ██     ██ ██  ████ ██          ██     ██  ██     ██ ██  ████       ██
# ██       ██     ██ ██   ███ ██    ██    ██     ██  ██     ██ ██   ███ ██    ██
# ██        ███████  ██    ██  ██████     ██    ████  ███████  ██    ██  ██████

def default_callback():
    """The default callback for a button. Does nothing."""
    pass

def test_callback():
    """The test callback for a button. Prints \"You clicked me!\" when called."""
    print("You clicked me!")

# ██     ██ ████ ████████ ██      ██  ██████
# ██     ██  ██  ██       ██  ██  ██ ██    ██
# ██     ██  ██  ██       ██  ██  ██ ██
# ██     ██  ██  ██████   ██  ██  ██  ██████
#  ██   ██   ██  ██       ██  ██  ██       ██
#   ██ ██    ██  ██       ██  ██  ██ ██    ██
#    ███    ████ ████████  ███  ███   ██████

class View(ABC):
    """The base view class.

    **Do not use this class.**
    """
    @abstractmethod
    def __init__(self, x, y):
        """Initializes a view with the given x and y positions."""
        self.x = x # type: int
        self.y = y # type: int

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

    def update_position(self, x: int, y: int) -> None:
        """Updates the position of the view in relation to the screen.

        You should not call this function; it will be called before rendering to make sure elements are
        positioned correctly. If you are implementing a class that contains other ``View`` s, make sure
        to update each of their positions by calling ``update_position`` for every view.

        :param x: The offset X position.
        :param y: The offset Y position.
        """
        self.x += x
        self.y += y

class Text(View):
    def __init__(self, x: int, y: int, text: str, text_color: sdl2.SDL_Color = WHITE):
        super().__init__(x, y)

        self.text = text # type: str
        self.text_color = text_color # type: sdl2.SDL_Color

    def draw(self, renderer: sdl2.ext.Renderer, font: sdl2.sdlttf.TTF_Font) -> None:

        surface = sdl2.sdlttf.TTF_RenderText_Solid(font, self.text.encode(), self.text_color)
        texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
        text_rect = sdl2.SDL_Rect(
            self.x,
            self.y,
            surface.contents.w,
            surface.contents.h
        )
        sdl2.SDL_FreeSurface(surface)
        sdl2.SDL_RenderCopy(renderer.sdlrenderer, texture, None, text_rect)
        sdl2.SDL_DestroyTexture(texture)


    def check_clicked(self, x: int, y: int) -> bool:
        """Returns ``False`` as text views cannot be clicked.

        :param x: The x position of the cursor.
        :param y: The y position of the cursor.
        :return: ``False``
        """
        return False

class Button(View):
    """A class for drawing button views."""

    def __init__(self, x: int, y: int, width: int, height: int, label: str,
                 color: sdl2.SDL_Color = SECONDARY, text_color: sdl2.SDL_Color = WHITE,
                 callback: Callable[[], None] = default_callback):
        """Initializes a button.

        :param x: The x position of the button.
        :param y: The y position of the button.
        :param width: The width of the button.
        :param height: The length of the button.
        :param label: The text on the button.
        :param color: The color of the button. Defaults to ``bv.SECONDARY``.
        :param text_color: The color of the text on the button. Defaults to ``bv.WHITE``.
        :param callback: The callback. Defaults to an empty function.
        """
        super().__init__(x, y)

        self.rect = sdl2.SDL_Rect(x, y, width, height) # type: sdl2.SDL_Rect
        self.label = label # type: str
        self.color = color # type: sdl2.SDL_Color
        self.text_color = text_color # type: sdl2.SDL_Color
        self.callback = callback # type: Callable[[], None]

    def draw(self, renderer: sdl2.ext.Renderer, font: sdl2.sdlttf.TTF_Font) -> None:
        """Draws the button to the screen.

        :param renderer: An SDL renderer.
        :param font: An SDL font.
        """
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

        if self.rect.x <= x <= self.rect.x + self.rect.w and \
            self.rect.y <= y <= self.rect.y + self.rect.h:
            self.callback()
            return True

        return False

    def update_position(self, x: int, y: int) -> None:
        super().update_position(x, y)
        self.rect.x += x
        self.rect.y += y

# ██      ██ ████ ██    ██ ████████   ███████  ██      ██  ██████
# ██  ██  ██  ██  ███   ██ ██     ██ ██     ██ ██  ██  ██ ██    ██
# ██  ██  ██  ██  ████  ██ ██     ██ ██     ██ ██  ██  ██ ██
# ██  ██  ██  ██  ██ ██ ██ ██     ██ ██     ██ ██  ██  ██  ██████
# ██  ██  ██  ██  ██  ████ ██     ██ ██     ██ ██  ██  ██       ██
# ██  ██  ██  ██  ██   ███ ██     ██ ██     ██ ██  ██  ██ ██    ██
#  ███  ███  ████ ██    ██ ████████   ███████   ███  ███   ██████

class Window:
    def __init__(self, name: str, view: View, x: int, y: int, width: int, height: int,
                 color: sdl2.SDL_Color = BLACK, titlebar_color: sdl2.SDL_Color = TERTIARY):
        """Initializes a new window.

        :param name: The title to display on the titlebar (not implemented yet)
        :param view: The base view for the window to display
        :param x: The initial x position of the window
        :param y: The initial y position of the window
        :param width: The width of the window
        :param height: The height of the window
        :param color: The color of the window
        """
        self.text = Text(x + 4, y + 2, name) # type: Text
        self.view = view # type: View
        self.x = x # type: int
        self.y = y # type: int
        self.width = width # type: int
        self.height = height # type: int
        self.color = color # type: sdl2.SDL_Color
        self.titlebar_color = titlebar_color # type: sdl2.SDL_Color

        self.update_position(self.x, self.y + 20)

    def draw(self, renderer: sdl2.ext.Renderer, font: sdl2.sdlttf.TTF_Font) -> None:
        """Draws a default window with a titlebar.

        :param renderer: An SDL renderer.
        :param font: An SDL font.
        """
        titlebar = sdl2.SDL_Rect(self.x, self.y, self.width, 20)
        renderer.fill(titlebar, self.titlebar_color)

        self.text.draw(renderer, font)

        rect = sdl2.SDL_Rect(self.x, self.y + 20, self.width, self.height)
        renderer.fill(rect, self.color)

        self.view.draw(renderer, font)

    def update_position(self, x: int, y: int) -> None:
        self.view.update_position(x, y)