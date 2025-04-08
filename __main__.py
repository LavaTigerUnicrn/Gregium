import gregium.buttons
import pyglet

window = pyglet.window.Window(1000, 1000)

batch = pyglet.graphics.Batch()

label = pyglet.text.Label(text="skbidi", font_size=10, color=[0, 0, 0], align="center")

FPS = pyglet.window.FPSDisplay(window)

frame = pyglet.gui.Frame(window)

vertPushButton = gregium.buttons.VerticalPushButtons(
    x=50,
    y=500,
    label=label,
    pressed=[0, 0, 0],
    depressed=[255, 255, 255],
    hover=[255, 0, 0],
    width=100,
    height=50,
    buttons=["skibid", "toilet", "among", "is", "fortnite"],
    frame=frame,
    batch=batch,
)


def hi(button):
    print(button)


vertPushButton.bind_press_function(hi)


@window.event
def on_draw():
    window.clear()

    batch.draw()

    FPS.draw()


pyglet.app.run()
