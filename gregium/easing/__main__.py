import pyglet
import gregium.easing as ease

if __name__ == "__main__":

    window = pyglet.window.Window(1920, 1080)

    progress = 0

    batch = pyglet.graphics.Batch()

    sinIn = pyglet.shapes.Rectangle(5, 540, 50, 50, batch=batch)
    sinInLabel = pyglet.text.Label(
        "In", 5, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    sinOut = pyglet.shapes.Rectangle(65, 540, 50, 50, batch=batch)
    sinOutLabel = pyglet.text.Label(
        "Out", 65, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    sinInOut = pyglet.shapes.Rectangle(125, 540, 50, 50, batch=batch)
    sinInOutLabel = pyglet.text.Label(
        "InOut", 125, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    sinLabel = pyglet.text.Label(
        "Sin", 65, 900, font_size=30, anchor_x="center", anchor_y="center", batch=batch
    )

    quadIn = pyglet.shapes.Rectangle(195, 540, 50, 50, batch=batch)
    quadInLabel = pyglet.text.Label(
        "In", 195, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    quadOut = pyglet.shapes.Rectangle(255, 540, 50, 50, batch=batch)
    quadOutLabel = pyglet.text.Label(
        "Out", 255, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    quadInOut = pyglet.shapes.Rectangle(315, 540, 50, 50, batch=batch)
    quadInOutLabel = pyglet.text.Label(
        "InOut", 315, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    quadLabel = pyglet.text.Label(
        "Quad",
        255,
        900,
        font_size=30,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
    )

    cubeIn = pyglet.shapes.Rectangle(380, 540, 50, 50, batch=batch)
    cubeInLabel = pyglet.text.Label(
        "In", 380, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    cubeOut = pyglet.shapes.Rectangle(440, 540, 50, 50, batch=batch)
    cubeOutLabel = pyglet.text.Label(
        "Out", 440, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    cubeInOut = pyglet.shapes.Rectangle(500, 540, 50, 50, batch=batch)
    cubeInOutLabel = pyglet.text.Label(
        "InOut", 500, 540, width=50, anchor_x="left", anchor_y="center", batch=batch
    )
    cubeLabel = pyglet.text.Label(
        "Mono\nDegree\n3",
        440,
        900,
        font_size=30,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
        multiline=True,
        width=60,
        align="center",
        dpi=50,
    )

    def update(dt):
        global progress
        progress = (progress + dt / 5) % 1

        sinIn.y = 215 + ease.easeInSine(progress) * 600
        sinOut.y = 215 + ease.easeOutSine(progress) * 600
        sinInOut.y = 215 + ease.easeInOutSine(progress) * 600

        quadIn.y = 215 + ease.easeInQuad(progress) * 600
        quadOut.y = 215 + ease.easeOutQuad(progress) * 600
        quadInOut.y = 215 + ease.easeInOutQuad(progress) * 600

        cubeIn.y = 215 + ease.easeInMono(progress, 3) * 600
        cubeOut.y = 215 + ease.easeOutMono(progress, 3) * 600
        cubeInOut.y = 215 + ease.easeInOutMono(progress, 3) * 600

    @window.event
    def on_draw():
        window.clear()

        batch.draw()

    pyglet.clock.schedule_interval(update, 1 / 60)

    pyglet.app.run()
