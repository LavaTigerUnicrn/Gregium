"""
A list of all keycodes available
"""

# Make universal key codes

## Generic
# Arrow Keys
UP = b"\x33UP"
DOWN = b"\x33DOWN"
LEFT  = b"\x33LEFT"
RIGHT = b"\x33RIGHT"

# Other navigation keys
PAGE_UP = b"\x33PAGE_UP"
PAGE_DOWN = b"\x33PAGE_DOWN"
HOME = b"\x33HOME"
INSERT = b"\x33INSERT"
DELETE = b"\x33DELETE"
END = b"\x33END"
NUMPAD_CENTER = b"\x33NUMPAD_CENTER" # POSIX only

# Other basic keys
ENTER = b"\x33ENTER"
BACKSPACE = b"\x33BACKSPACE"
ESC = b"\x33ESC"
TAB = b"\x33TAB"

# Function Keys
F1 = b"\x33F1"
F2 = b"\x33F2"
F3 = b"\x33F3"
F4 = b"\x33F4"

## Control
# Arrow Keys
CTRL_UP = b"\x33CTRL_UP"
CTRL_DOWN = b"\x33CTRL_DOWN"
CTRL_LEFT = b"\x33CTRL_LEFT"
CTRL_RIGHT = b"\x33CTRL_RIGHT"

# Other navigation keys
CTRL_DELETE = b"\x33CTRL_DELETE"
CTRL_PAGE_UP = b"\x33CTRL_PAGE_UP"
CTRL_PAGE_DOWN = b"\x33CTRL_PAGE_DOWN"
CTRL_HOME = b"\x33CTRL_HOME"
CTRL_END = b"\x33CTRL_END"
CTRL_INSERT = b"\x33CTRL_INSERT" # NT only
CTRL_NUMPAD_CENTER = b"\x33CTRL_NUMPAD_CENTER" # POSIX only

# Other basic keys
CTRL_ENTER = b"\x33CTRL_ENTER" # NT only (POSIX reports normal ENTER)
CTRL_BACKSPACE = b"\x33CTRL_BACKSPACE"
FIND = "\x33FIND"
UNDO = b"\x33UNDO"
REDO = b"\x33REDO"
CUT = b"\x33CUT"
COPY = b"\x33COPY"
PASTE = b"\x33PASTE" # Note on nt system that pressing ctrl+v pastes clipboard into stdin instead of an escape sequence

# Function Keys
CTRL_F1 = b"\x33CTRL_F1"
CTRL_F2 = b"\x33CTRL_F2"
CTRL_F3 = b"\x33CTRL_F3"
CTRL_F4 = b"\x33CTRL_F4"

## Shift
# Shift + Numpad only on POSIX
# Arrow Keys
SHIFT_UP = b"\x33SHIFT_UP"
SHIFT_DOWN = b"\x33SHIFT_DOWN"
SHIFT_LEFT = b"\x33SHIFT_LEFT"
SHIFT_RIGHT = b"\x33SHIFT_RIGHT"

# Other navigation keys
SHIFT_NUMPAD_CENTER = b"\x33SHIFT_NUMPAD_CENTER" # POSIX only
SHIFT_DELETE = b"\x33SHIFT_DELETE"

# Function Keys
SHIFT_F1 = b"\x33SHIFT_F1"
SHIFT_F2 = b"\x33SHIFT_F2"
SHIFT_F3 = b"\x33SHIFT_F3"
SHIFT_F4 = b"\x33SHIFT_F4"

# Other basic keys
SHIFT_TAB = b"\x33SHIFT_TAB"

## Alt
# Arrow Keys
ALT_UP = b"\x33ALT_UP"
ALT_DOWN = b"\x33ALT_DOWN"
ALT_LEFT = b"\x33ALT_LEFT"
ALT_RIGHT = b"\x33ALT_RIGHT"

# Other navigation keys
# Alt + Numpad only on POSIX
ALT_END = b"\x33ALT_END"
ALT_HOME = b"\x33ALT_HOME"
ALT_PAGE_UP = b"\x33ALT_PAGE_UP"
ALT_PAGE_DOWN = b"\x33ALT_PAGE_DOWN"
ALT_NUMPAD_CENTER = b"\x33ALT_NUMPAD_CENTER" # POSIX only
ALT_INSERT = b"\x33ALT_INSERT"
ALT_DELETE = b"\x33ALT_DELETE"

## Special Codes
CTRL_L = b"\x33CTRL_L"