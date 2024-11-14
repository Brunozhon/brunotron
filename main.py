import sdl2
import sdl2.ext
import sdl2.sdlttf

# Initialize SDL and TTF
sdl2.ext.init()
sdl2.sdlttf.TTF_Init()
window = sdl2.ext.Window("Brunotron", size=(512, 384))
window.show()
renderer = sdl2.ext.Renderer(window)

# Important colors
WHITE = sdl2.SDL_Color(255, 255, 255)
BLACK = sdl2.SDL_Color(0, 0, 0)

PRIMARY = sdl2.SDL_Color(48, 213, 200)
SECONDARY = sdl2.SDL_Color(10, 186, 181)

# The font
font = sdl2.sdlttf.TTF_OpenFont(b"pixel-letters.ttf", 16)

# Renders text onto the display
def render_text(text, x, y, color=WHITE):
    surface = sdl2.sdlttf.TTF_RenderText_Solid(font, text.encode(), color)
    texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
    text_rect = sdl2.SDL_Rect(x, y, surface.contents.w, surface.contents.h)
    sdl2.SDL_FreeSurface(surface)
    sdl2.SDL_RenderCopy(renderer.sdlrenderer, texture, None, text_rect)
    sdl2.SDL_DestroyTexture(texture)

def draw_menu_bar():
    renderer.fill(sdl2.SDL_Rect(0, 0, 512, 30), SECONDARY)
    render_text("Placeholder", 7, 10)

running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False

    renderer.clear()

    draw_menu_bar()

    renderer.present()

# Clean up
sdl2.sdlttf.TTF_CloseFont(font)
sdl2.sdlttf.TTF_Quit()
sdl2.ext.quit()
