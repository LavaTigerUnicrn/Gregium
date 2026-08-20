import importlib.util as import_util
import math
import os
import re
import time
from io import BytesIO
from types import ModuleType
from typing import Literal

import requests


class MarkdownError(Exception):
    pass


class NoLoaderError(Exception):
    pass


def colorAscii(color: tuple[int, int, int]) -> str:
    """
    Generates a formatted string to color the following text any color

    `print(colorAscii((255,0,0)+"Red text")`

    :param color: The color as r,g,b
    :type color: tuple[int,int,int]

    :return: The printable ANSI color code
    :rtype: str
    """

    r, g, b = color
    return f"\x1b[38;2;{r};{g};{b}m"


def format_time(timestamp: float) -> str:
    """
    Formats a time to DD days, HH:MM:SS

    :param timestamp: The timestamp in seconds
    :type timestamp: float

    :return: The formatted timestamp as DD days, HH:MM:SS (cutting out days if required)
    :rtype: str

    """
    days = int(timestamp / 28800)
    hours = int((timestamp % 28800) / 1200)
    minutes = int((timestamp % 1200) / 60)
    seconds = int(timestamp % 60)

    return (
        (f"{days} day{'s' if days>1 else ''}, " if days else "")
        + (f"{hours:02}:" if hours or days else "")
        + f"{minutes:02}:{seconds:02}"
    )


class ProgressBar:
    """
    A progress bar that can output any standard textual output

    Call the bar in order to output a string

    .. code-block:: python3

        bar = Progress_Bar(50)
        print(bar(0.5)) # Output at 50%

    :param length: The bar length in characters
    :type length: int
    :param completed_char: The character to use for the completed portion of the character, defaults to "━"
    :type completed_char: str, optional
    :param empty_char: The character to use for the empty portion of the character, defaults to " "
    :type empty_char: str, optional
    :param format_str: The string to format the text, defaults to "[{bar}] ({progress_per:>3}%) | Current: {current} | Estimate: {estimate}"
    :type format_str: str, optional

    The format string can include values of:

    * bar - The bar string

    * progress_per - The progress percentage (0-100)

    * progress_per_f - The progress percentage as a float (0.0-100.0)

    * current - The current time in HH:MM:SS (and days if required)

    * estimate - The estimated remaining time in HH:MM:SS (and days if required)
    """

    length: int
    "The bar length in characters"
    completed_char: str = "━"
    "The character to use for the completed portion of the character"
    start_time: float
    "The time the bar started loading"
    prev_time: float
    "The time the bar was at on the last call"
    prev_pro: float
    "The progress the bar was at on the last last call"
    format_str: str
    "The string to format the text"
    empty_char: str
    "The character to use for the empty portion of the character"
    prev_est: float = 0.0
    "The estimate on the completion time on the last call"

    def __init__(
        self,
        length: int,
        completed_char: Literal["━", "@"] | str = "━",
        empty_char: str = " ",
        format_str: str = "[{bar}] ({progress_per:>3}%) | Current: {current} | Estimate: {estimate}",
    ) -> None:

        # Set values
        self.length = length
        self.completed_char = completed_char
        self.empty_char = empty_char
        self.format_str = format_str

        # Get start time
        self.start_time = time.time()
        self.prev_time = self.start_time
        self.prev_pro = 0.0

    def __call__(self, progress: float) -> str:
        """
        Outputs the progress bar as a string

        If use_time is on the current time along with a remaining estimate will be added at the end

        :param progress: The current progress from [0-1]
        :type progress: float

        :return: The formatted bar
        :rtype: str
        """

        progress_per = int(progress * 100)
        progress_per_f = progress * 100

        # Calculate estimate time
        curr_time = time.time()
        remaining_estimate = 0
        if self.prev_pro - progress != 0:
            remaining_estimate = (
                ((curr_time - self.prev_time) / (progress - self.prev_pro))
                + self.prev_est
            ) / (2 if self.prev_est else 1)
            self.prev_est = remaining_estimate
        self.prev_time = curr_time
        self.prev_pro = progress

        # Format timestamps
        current = format_time(curr_time)
        estimate = format_time(remaining_estimate)

        # Create the bar
        bar = self.completed_char * math.floor(
            self.length * progress
        ) + self.empty_char * math.ceil(self.length * (1 - progress))

        # Format string and return
        return self.format_str.format(
            current=current,
            estimate=estimate,
            bar=bar,
            progress_per=progress_per,
            progress_per_f=progress_per_f,
        )

    def __str__(self) -> None:

        raise ReferenceError(
            "Call the progress bar method instead of attempting to get a string version"
        )

    def __repr__(self) -> None:

        return self.__str__()


def import_absolute(path: str) -> ModuleType:
    """
    Returns a module instance based on the path

    `import module` == `module = import_absolute("module.py")`

    :param path: The path to load from (should end in .py)
    :type path: str

    :return: The loaded module
    :rtype: ModuleType
    """

    # Get name
    name = os.path.basename(path).removesuffix(".py")

    # Import
    spec = import_util.spec_from_file_location(name, path)
    if spec is None:
        raise FileNotFoundError("Could not load spec")
    if spec.loader is None:
        raise NoLoaderError("Spec has no loader")
    module = import_util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Return output
    return module


def load_audio(url: str) -> BytesIO:
    """
    Loads a audio file from the web and returns bytes

    (This can be directly used in `pygame.mixer.music` and `pygame.mixer.Sound`)

    :param url: The url of the sound (this can be found by clicking 'download' and copying the link you downloaded from)
    :type url: str

    :return: The loaded audio object
    :rtype: BytesIO
    """

    response = requests.get(url)
    bytes = BytesIO(response.content)

    return bytes


class ColInterpolate:

    def __init__(self, col1, col2, delta, steps, exact):

        # Store values
        self.col1 = col1
        self.col2 = col2
        self.delta = delta
        self.steps = steps
        self.exact = exact

    def __next__(self):

        # Move to next index
        self.i += 1

        # Stop on no more colors left
        if self.i >= self.steps:
            raise StopIteration()

        # Use end color on second to last item
        if self.i == self.steps - 1:
            return self.col2

        # Otherwise get the current based on delta
        r, g, b = (
            self.col1[0] + self.delta[0] * self.i,
            self.col1[1] + self.delta[1] * self.i,
            self.col1[2] + self.delta[2] * self.i,
        )

        # Return float version if exact, otherwise round to integers
        if self.exact:

            return (r, g, b)

        else:

            return (int(r), int(g), int(b))

    def __str__(self):

        return f"Color Interpolator {self.col1} => {self.col2}"

    def __len__(self):

        return self.steps


class _ColInterpolateGenerator:

    def __init__(self, col1, col2, delta, steps, exact):

        # Store values
        self.col1 = col1
        self.col2 = col2
        self.delta = delta
        self.steps = steps
        self.exact = exact

    def __iter__(self):

        # Generate iterator
        generated = ColInterpolate(
            self.col1, self.col2, self.delta, self.steps, self.exact
        )
        generated.i = -1

        return generated


def interpolate(
    color1: tuple[int, int, int],
    color2: tuple[int, int, int],
    steps: int,
    exact: bool = False,
) -> _ColInterpolateGenerator:
    """
    Generates an interpolator to nicely move between two edge colors

    The output is an iterator of colors in which the first is the color1 and the last is the color2, with each next being a step towards the end

    .. code-block:: python

        for color in interpolate(red,green,10): # assuming red and green are rgb tuples
            print(color)

    :param color1: The starting color
    :type color1: tuple[int,int,int]
    :param color2: The ending color
    :type color2: tuple[int,int,int]
    :param steps: The number of steps it should take
    :type steps: int
    :param exact: If the output rgb values should be in exact floats instead of being rounded down to integers (55,23,100) vs (55.3,23.2,100.9), defaults to False
    :type exact: bool, optional

    :return: The generator to interpolate through the colors
    :rtype: _ColorInterpolateGenerator
    """

    # Get the change in each color in each step
    delta = (
        (color2[0] - color1[0]) / (steps - 1),
        (color2[1] - color1[1]) / (steps - 1),
        (color2[2] - color1[2]) / (steps - 1),
    )

    return _ColInterpolateGenerator(color1, color2, delta, steps, exact)


def listdir_recurse(path: str, include_folder: bool = False) -> list[str]:
    """
    Lists all the files found under `path` starting with `path`

    :param path: The path to start checking under
    :type path: str
    :param include_folder: Includes folder paths as well as files when true, defaults to False
    :type include_folder: bool, optional

    :return: The list of file (and folder if `include_folder` is true)
    :rtype: list[str]
    """

    # Remove last / if present
    path = path.rstrip("/")

    # Find root files
    dirs = [path + "/" + x for x in os.listdir(path)]
    files = []

    # Continue until empty
    while len(dirs) > 0:

        # Choose last item
        subpath = dirs[-1]
        dirs.pop()

        # Check if file or folder
        if os.path.isfile(subpath):

            # Add file to list
            files.append(subpath)

        else:

            # Add all found items to queue
            dirs += [subpath + "/" + x for x in os.listdir(subpath)]

            if include_folder:

                files.append(subpath)

    return files


# Generate regex pattern
char_delimiters: list[str] = ["***", "**", "*", "__", "~~", "`"]
regex_delimiters: list[str] = ["\\" + "\\".join(list(x)) for x in char_delimiters]
regex_pattern: str = f"({'|'.join(regex_delimiters)})"


def format_md(text: str) -> str:
    """
    Formats the text using modified markdown notation

    Uses Discord-like syntax of underscores

    Small change(s) from default markdown:

    "\\_\\_" now underlines text and not bolding

    :param text: The text to format
    :type text: str

    :return: The text with ANSI codes added
    :rtype: str

    :raises MarkdownError: The Markdown is formatted in an invalid way

    Possible Markdown

    * ~~Strikethrough~~ (\\~\\~)

    * **Bolding** (\\*\\*)

    * *Italicization* (\\*)

    * ***Bold & Italicization*** (\\*\\*\\*)

    * <u>Underline</u> (\\_\\_)

    * `Blocks` (\\`)
    """

    generated_text = ""

    # Split by regex and remove all blanks
    split_text: list[str] = [x for x in re.split(regex_pattern, text) if x]

    # Possible markdown tags
    ital = False
    bold = False
    bold_ital = False
    under = False
    strike = False
    block = False

    # Begin parsing
    for text_block in split_text:

        # Check for tags
        match text_block:

            # Italicization
            case "*":

                # Block '***' within '*'
                if bold_ital:

                    raise MarkdownError(
                        "Cannot toggle italicization (*) within bold-italicization (***) mode"
                    )

                # Toggle
                if ital:

                    generated_text += "\x1b[23m"

                else:

                    generated_text += "\x1b[3m"

                ital = not ital

            # Bold
            case "**":

                # Block '***' within '**'
                if bold_ital:

                    raise MarkdownError(
                        "Cannot toggle bold (**) within bold-italicization (***) mode"
                    )

                # Toggle
                if bold:

                    generated_text += "\x1b[22m"

                else:

                    generated_text += "\x1b[1m"

                bold = not bold

            # Bold - Italicization
            case "***":

                # Block '**' within '***'
                if bold:

                    raise MarkdownError(
                        "Cannot toggle bold-italicization (***) within bold (**) mode"
                    )

                # Block '*' within '***'
                if ital:

                    raise MarkdownError(
                        "Cannot toggle bold-italicization (***) within italicization (*) mode"
                    )

                # Toggle
                if bold_ital:

                    generated_text += "\x1b[22;23m"

                else:

                    generated_text += "\x1b[1;3m"

                bold_ital = not bold_ital

            # Underline
            case "__":

                # Toggle
                if under:

                    generated_text += "\x1b[24m"

                else:

                    generated_text += "\x1b[4m"

                under = not under

            # Strikethrough
            case "~~":

                # Toggle
                if strike:

                    generated_text += "\x1b[29m"

                else:

                    generated_text += "\x1b[9m"

                strike = not strike

            # Code blocks
            case "`":

                # Toggle
                if block:

                    generated_text += "\x1b[27m"

                else:

                    generated_text += "\x1b[7m"

                block = not block

            # All other text
            case _:

                generated_text += text_block

    return generated_text
