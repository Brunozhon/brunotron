import sdl2.ext
import sdl2.sdlttf
import sdl2.sdlimage
from sdl2.sdlimage import IMG_INIT_PNG, IMG_INIT_JPG
import brunoviews as bv

# Initialize SDL and TTF
sdl2.ext.init()
sdl2.sdlttf.TTF_Init()
sdl2.sdlimage.IMG_Init(IMG_INIT_PNG | IMG_INIT_JPG)
window = sdl2.ext.Window("Brunotron", size=(512, 384))
window.show()
renderer = sdl2.ext.Renderer(window)

# The font
font = sdl2.sdlttf.TTF_OpenFont(b"pixel-letters.ttf", 16)

button = bv.Button(10, 10, 50, 15, "Button", callback=bv.test_callback)
text = bv.Text(10, 30, "Hello, world!")
mv = bv.MV(0, 0, [button, text])
win = bv.Window("Window", mv, 10, 10, 100, 100, bv.PRIMARY)
app = bv.App(win, "wrench.png", 10, 10)

running = True
dragging_window = None

while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            x, y = event.button.x, event.button.y
            for w in bv.windows:
                if not w.view.check_clicked(x, y):
                    if w.titlebar_clicked(x, y):
                        dragging_window = w
                        dragging_window.move_to(x, y)
            if app.is_clicked(x, y):
                app.launch()
        elif sdl2.SDL_GetMouseState(None, None) & sdl2.SDL_BUTTON_LMASK:
            x, y = event.button.x, event.button.y
            if dragging_window and dragging_window.titlebar_clicked(x, y):
                dragging_window.move_to(x, y)
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            dragging_window = None
            for w in bv.windows:
                w.unclick()

    renderer.clear()
    app.draw_icon(renderer)

    for w in bv.windows:
        w.draw(renderer, font)

    renderer.present()

# Clean up
sdl2.sdlttf.TTF_CloseFont(font)
sdl2.sdlttf.TTF_Quit()
sdl2.sdlimage.IMG_Quit()
sdl2.ext.quit()
