"""
Adds additional functions for interacting with the standard terminal

For many additional functions use `blessed <https://blessed.readthedocs.io/en/latest/>`_
"""

from typing import TypeVar

from blessed import Terminal

term = Terminal()

T = TypeVar("T")

TERMINAL_CAROUSEL: int = 10
DEFAULT_TERMINAL_CHOICE_HELP: bool = False


def clear() -> None:
    """
    Clears terminal
    """
    print(term.clear, end="")


def getch() -> str:
    """
    Gets a character from the terminal as a string, for example KEY_UP

    It may also return the raw key if no key name can be found (generally happens for keyboard keys)
    """

    with term.raw():

        char = term.inkey()

    if char.name is None:

        return char

    return char.name


def bell() -> None:
    """
    Triggers the terminal bell using \\\\a
    """
    print("\a", end="")


def choice(options: dict[T, dict[str, str]], help: bool | None = None) -> T:
    """
    Makes a choice input for given choices in terminal

    :param options: The valid choices, formatted as ```{"choice_1":{"name":"custom_choice_name","desc":"custom_choice_description"}}```

        And the text on the terminal would be formatted as "custom_choice_name" normally or "[custom_choice_name] - custom_choice_description" when hovered and would return "choice_1" when enter is pressed
        
        Keys can be omitted up to ```{"choice_1":{}}``` in which the description would be assumed to be none and the name would be treated as the choice
        
        Any type can be used as the possible option, but only a string is allowed as the name (if the name is left empty it will be changed to a string)
        
        If too many choices are present the choices will go into carousel mode in which only the maximum amount will be shown at any given time, change this amount using `TERMINAL_CAROUSEL`
    :type options: dict
    :param help: Whether or not the help text should show (change default with `DEFAULT_TERMINAL_CHOICE_HELP`)
    :type help: bool, optional

    :return: The selected option by the user
    :rtype: The same type as the given options
    """

    # Update help option
    help = help or DEFAULT_TERMINAL_CHOICE_HELP

    # Verify carousel value
    if TERMINAL_CAROUSEL % 2 != 0 or TERMINAL_CAROUSEL < 2:
        raise ValueError(
            "The value of TERMINAL_CAROUSEL must be a positive even integer"
        )

    # Load choices
    for option, properties in options.items():

        # Set defaults
        properties["name"] = properties.get("name") or str(option)
        if properties.get("desc") is None:
            properties["desc"] = ""

        properties["name_norm"] = term.clear_eol + " " + properties["name"]
        properties["name_hover"] = (
            term.clear_eol
            + f"[{properties['name']}]"
            + ((" - " + properties["desc"]) if properties["desc"] != "" else "")
        )

    # Begin terminal
    selected: int = 0
    with term.raw():

        if help:

            print("Use [up] [down] and [enter] to select an item")

        while True:

            # Get total printed lines
            printed_lines = min(len(options), TERMINAL_CAROUSEL)

            # Check for carousel and set bounds
            low_bound: int = 0
            high_bound: int = len(options)
            if TERMINAL_CAROUSEL < len(options):

                # (Add special clamping when on the edges of options to prevent strange effects)
                low_bound = selected - TERMINAL_CAROUSEL // 2
                high_bound = (
                    selected
                    + TERMINAL_CAROUSEL // 2
                    + (-low_bound if low_bound < 0 else 0)
                    - 1
                )
                if high_bound > len(options) - 1:
                    low_bound -= high_bound - len(options) + 1

            # Print all options
            for i, item in enumerate(options.items()):
                if low_bound > i or high_bound < i:
                    continue

                if (low_bound == i or high_bound == i) and not (
                    i == 0 or i == len(options) - 1
                ):
                    print("\x1b[2m", end="")

                option, properties = item

                if i == selected:
                    print(properties["name_hover"], end="\n\r")
                else:
                    print(properties["name_norm"], end="\n\r")
                print("\x1b[22m", end="")

            # Move up cursor
            print(term.move_up(printed_lines), end="")

            # Accept inputs
            key = term.inkey()

            if key.name == "KEY_UP":

                selected -= 1

            elif key.name == "KEY_DOWN":

                selected += 1

            elif key.name == "KEY_ENTER":

                # Move cursor to correct position
                print(term.move_down(printed_lines), end="")

                # Return chosen item
                return list(options.keys())[selected]

            # Clamp selected
            selected %= len(options)


def confirm(title: str = "Are you sure", help: bool | None = None) -> bool:
    """
    Confirmation using the terminal

    :param title: The title string
    :type title: str, optional
    :param help: Whether or not the help text should show (change default with `DEFAULT_TERMINAL_CHOICE_HELP`)
    :type help: bool, optional

    :return: True (yes) or False (no)
    :rtype: bool
    """

    print(title)

    return choice({True: {"name": "Yes"}, False: {"name": "No"}}, help=help)
