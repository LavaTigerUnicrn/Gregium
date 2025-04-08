import pyglet


def rectPoint(rect: pyglet.shapes.Rectangle, point: tuple[int, int]) -> bool:
    """
    Collides pygame rect and point

    rect:
        Pyglet rect object

    point:
        A tuple of the point in which collision occurs

    """

    # Unpack point
    x, y = point

    # Check if point is within the bounds
    if (
        rect.x < x
        and rect.x + rect.width > x
        and rect.y < y
        and rect.y + rect.height > y
    ):

        # Return true if colliding
        return True

    # Return false if point isn't within bounds
    return False
