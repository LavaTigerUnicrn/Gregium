"""
Adds extra buttons not found in pyglet, such as push buttons from rects and text entry with borders
"""

import pyglet
import math
from pyglet.graphics import Group


class PushButtonRect(pyglet.gui.WidgetBase):
    """The base of all widgets."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        pressed: tuple[int, int, int],
        depressed: tuple[int, int, int],
        hover: tuple[int, int, int] | None = None,
        label: pyglet.text.Label | None = None,
        batch: pyglet.graphics.Batch | None = None,
        group: Group | None = None,
    ) -> None:
        """Instance of a push button based on a rect.

        Args:
            x:
                X coordinate of the push button.
            y:
                Y coordinate of the push button.
            pressed:
                Color to display when the button is pressed.
            depressed:
                Color to display when the button isn't pressed.
            hover:
                Color to display when the button is being hovered over.
            batch:
                Optional batch to add the push button to.
            label:
                Optional label to have on the text
            group:
                Optional parent group of the push button.
        """
        super().__init__(x=x, y=y, width=width, height=height)
        self._pressed = pressed
        self._depressed = depressed
        self._hover = hover or depressed
        self._batch = batch or pyglet.graphics.Batch()
        bg_group = Group(order=0, parent=group)
        fg_group = Group(order=1, parent=group)
        self._user_group = group

        self._label = label
        self.text = label.text

        self._label.batch = batch
        self._label.group = fg_group
        self._label.multiline = True
        self._label.x, self._label.y, self._label.width = (
            x + width / 2,
            y + height / 2,
            width,
        )
        self._rect = pyglet.shapes.BorderedRectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            color=depressed,
            group=bg_group,
            batch=batch,
            border_color=(0, 0, 0, 255),
            border=5,
        )

        self._is_pressed = False

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        assert type(value) is str, "This Widget's text must be a string."
        self._text = value
        self._label.text = self._text
        self._label.height = (
            self._label.get_line_count() * self._label.font_size * 1.5
            + ((self._label.get_line_count() - 1) * self._label.font_size * (1 / 4))
        )

    @property
    def value(self) -> bool:
        return self._is_pressed

    @value.setter
    def value(self, value: bool) -> None:
        assert type(value) is bool, "This Widget's value must be True or False."
        self._is_pressed = value
        self._rect.color = self._pressed if self._is_pressed else self._depressed

    def update_groups(self, order: int) -> None:
        self._rect.group = Group(order=order, parent=self._user_group)
        self._label.group = Group(order=order + 1, parent=self._user_group)

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or not self._check_hit(x, y):
            return
        self._rect.color = self._pressed
        self._is_pressed = True
        self.dispatch_event("on_press")

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or not self._is_pressed:
            return
        self._rect.color = self._hover if self._check_hit(x, y) else self._depressed
        self._is_pressed = False
        self.dispatch_event("on_release")

    def on_mouse_leave(self, x: int, y: int) -> None:
        if not self.enabled or not self._is_pressed:
            return
        self._rect.color = self._depressed
        self._is_pressed = False
        self.dispatch_event("on_release")

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        if not self.enabled or self._is_pressed:
            return
        self._rect.color = self._hover if self._check_hit(x, y) else self._depressed

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int
    ) -> None:
        if not self.enabled or self._is_pressed:
            return
        self._rect.color = self._hover if self._check_hit(x, y) else self._depressed

    def on_press(self) -> None:
        """Event: Dispatched when the button is clicked."""

    def on_release(self) -> None:
        """Event: Dispatched when the button is released."""


PushButtonRect.register_event_type("on_press")
PushButtonRect.register_event_type("on_release")


class ToggleButtonRect(PushButtonRect):
    """Instance of a toggle button based on a rect.

    Triggers the event 'on_toggle' when the mouse is pressed or released.
    """

    def _get_release_color(self, x: int, y: int) -> tuple[int, int, int]:
        return self._hover if self._check_hit(x, y) else self._depressed

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or not self._check_hit(x, y):
            return
        self._is_pressed = not self._is_pressed
        self._rect.color = (
            self._pressed if self._is_pressed else self._get_release_color(x, y)
        )
        self.dispatch_event("on_toggle", self._is_pressed)

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled or self._is_pressed:
            return
        self._rect.color = self._get_release_color(x, y)

    def on_toggle(self, value: bool) -> None:
        """Event: returns True or False to indicate the current state."""


ToggleButtonRect.register_event_type("on_toggle")


class SliderRect(pyglet.gui.WidgetBase):
    """Instance of a slider made of a base and a knob rect.

    Triggers the event 'on_change' when the knob position is changed.
    The knob position can be changed by dragging with the mouse, or
    scrolling the mouse wheel.
    """

    def __init__(
        self,
        x: int,
        y: int,
        base: pyglet.shapes.BorderedRectangle,
        knob: pyglet.shapes.BorderedRectangle,
        edge: int = 0,
        batch: pyglet.graphics.Batch | None = None,
        group: Group | None = None,
    ) -> None:
        """Create a slider.

        Args:
            x:
                X coordinate of the slider.
            y:
                Y coordinate of the slider.
            base:
                Color to display as the background to the slider.
            knob:
                Color of Knob that moves to show the position of the slider.
            edge:
                Pixels from the maximum and minimum position of the slider,
                to the edge of the base rect.
            batch:
                Optional batch to add the slider to.
            group:
                Optional parent group of the slider.
        """
        super().__init__(x, y, base.width, knob.height)
        self._edge = edge
        self._base_rect = base
        self._knob_rect = knob
        self._half_knob_width = knob.width / 2
        self._half_knob_height = knob.height / 2
        self._knob_rect.anchor_y = int(knob.height / 2)

        self._min_knob_x = x + edge
        self._max_knob_x = x + base.width - knob.width - edge

        self._user_group = group
        bg_group = Group(order=0, parent=group)
        fg_group = Group(order=1, parent=group)
        self._base_rect.anchor_y = base.height / 2
        (
            self._base_rect.x,
            self._base_rect.y,
            self._base_rect.batch,
            self._base_rect.group,
        ) = x, y, batch, bg_group
        self._knob_rect.anchor_y = knob.height / 2
        (
            self._knob_rect.x,
            self._knob_rect.y,
            self._knob_rect.batch,
            self._knob_rect.group,
        ) = x + edge, y, batch, fg_group

        self._value = 0
        self._in_update = False

    def _update_position(self) -> None:
        self._base_rect.position = self._x, self._y, 0
        self._knob_rect.position = (
            self._x + self._edge,
            self._y + self._base_rect.height / 2,
            0,
        )

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        assert type(value) in (
            int,
            float,
        ), "This Widget's value must be an int or float."
        self._value = value
        x = (
            (self._max_knob_x - self._min_knob_x) * value / 100
            + self._min_knob_x
            + self._half_knob_width
        )
        self._knob_rect.x = max(
            self._min_knob_x, min(x - self._half_knob_width, self._max_knob_x)
        )

    def update_groups(self, order: int) -> None:
        self._base_rect.group = Group(order=order + 1, parent=self._user_group)
        self._knob_rect.group = Group(order=order + 2, parent=self._user_group)

    @property
    def _min_x(self) -> int:
        return self._x + self._edge

    @property
    def _max_x(self) -> int:
        return self._x + self._width - self._edge

    @property
    def _min_y(self) -> int:
        return int(self._y - self._half_knob_height)

    @property
    def _max_y(self) -> int:
        return int(self._y + self._half_knob_height + self._base_rect.height / 2)

    def _check_hit(self, x: int, y: int) -> bool:
        return self._min_x < x < self._max_x and self._min_y < y < self._max_y

    def _update_knob(self, x: int) -> None:
        self._knob_rect.x = max(
            self._min_knob_x, min(x - self._half_knob_width, self._max_knob_x)
        )
        self._value = abs(
            ((self._knob_rect.x - self._min_knob_x) * 100)
            / (self._min_knob_x - self._max_knob_x)
        )
        self.dispatch_event("on_change", self._value)

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled:
            return
        if self._check_hit(x, y):
            self._in_update = True
            self._update_knob(x)

    def on_mouse_drag(
        self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int
    ) -> None:
        if not self.enabled:
            return
        if self._in_update:
            self._update_knob(x)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: float, scroll_y: float) -> None:
        if not self.enabled:
            return
        if self._check_hit(x, y):
            self._update_knob(self._knob_rect.x + self._half_knob_width + scroll_y)  # type: ignore reportArgumentType

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if not self.enabled:
            return
        self._in_update = False

    def on_change(self, value: float) -> None:
        """Event: Returns the current value when the slider is changed."""


SliderRect.register_event_type("on_change")


class BorderedTextEntry(pyglet.gui.TextEntry):
    """Instance of a text entry widget. Allows the user to enter and submit text.

    Triggers the event 'on_commit', when the user hits the Enter or Return key.
    The current text string is passed along with the event.
    """

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
        text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        caret_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        border: int = 2,
        border_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        batch: pyglet.graphics.Batch | None = None,
        group: Group | None = None,
    ) -> None:
        """Create a text entry widget.

        Args:
            text:
                Initial text to display.
            x:
                X coordinate of the text entry widget.
            y:
                Y coordinate of the text entry widget.
            width:
                The width of the text entry widget.
            color:
                The color of the outline box in RGBA format.
            text_color:
                The color of the text in RGBA format.
            caret_color:
                The color of the caret (when it is visible) in RGBA or RGB format.
            border:
                The width of the border
            border_color:
                The color of the border
            batch:
                Optional batch to add the text entry widget to.
            group:
                Optional parent group of text entry widget.
        """
        super().__init__(
            text=text,
            x=x,
            y=y,
            width=width,
            color=color,
            text_color=text_color,
            caret_color=caret_color,
            batch=batch,
            group=group,
        )
        font = self._doc.get_font()
        height = font.ascent - font.descent
        bg_group = Group(order=0, parent=group)
        p = 2
        self._outline = pyglet.shapes.BorderedRectangle(
            x=x - p,
            y=y - p,
            width=width + p + p,
            height=height + p + p,
            color=color,
            batch=batch,
            group=bg_group,
            border=border,
            border_color=border_color,
        )


class MouseDistanceDetector(pyglet.gui.WidgetBase):
    def __init__(self, x: int, y: int):
        """Creates a widget that detects the mouse distance at any given position;
        it is reccomended to not have this in a frame so it's able to detect distance no matter what

        Args:
            text:
                Initial text to display.
            x:
                X coordinate of the text entry widget.
            y:
                Y coordinate of the text entry widget.

        """

        super().__init__(x=x, y=y, width=0, height=0)

        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

    def on_mouse_motion(self, x, y, dx, dy):
        self._value = math.sqrt((self._x - x) ** 2 + (self._y - y) ** 2)
        self.dispatch_event("on_change", self._value)

    def on_change(self, value: float) -> None:
        """Event: Returns the mouse distance when it is moved."""


MouseDistanceDetector.register_event_type("on_change")
