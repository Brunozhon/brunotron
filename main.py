import sdl2
import sdl2.ext
import sdl2.sdlttf
import brunoviews as bv

# Initialize SDL and TTF
sdl2.ext.init()
sdl2.sdlttf.TTF_Init()
window = sdl2.ext.Window("Brunotron", size=(512, 384))
window.show()
renderer = sdl2.ext.Renderer(window)

# Important colors

# The font
font = sdl2.sdlttf.TTF_OpenFont(b"pixel-letters.ttf", 16)

# Renders text onto the display
def render_text(text, x, y, color=bv.WHITE):
    surface = sdl2.sdlttf.TTF_RenderText_Solid(font, text.encode(), color)
    texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
    text_rect = sdl2.SDL_Rect(x, y, surface.contents.w, surface.contents.h)
    sdl2.SDL_FreeSurface(surface)
    sdl2.SDL_RenderCopy(renderer.sdlrenderer, texture, None, text_rect)
    sdl2.SDL_DestroyTexture(texture)

button = bv.Button(10, 10, 50, 15, "Button", callback=bv.test_callback)
window = bv.Window("Window", button, 10, 10, 100, 100, bv.PRIMARY)

running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            x, y = event.button.x, event.button.y
            print(x, y)
            button.check_clicked(x, y)

    renderer.clear()

    window.draw(renderer, font)

    renderer.present()

# Clean up
sdl2.sdlttf.TTF_CloseFont(font)
sdl2.sdlttf.TTF_Quit()
sdl2.ext.quit()
