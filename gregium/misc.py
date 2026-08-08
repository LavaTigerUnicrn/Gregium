import importlib.util as import_util
import math
import os
import time
from io import BytesIO
from typing import Literal

import requests

Term_Type = Literal["powershell", "cmd"]


class NoLoaderError(Exception):
    pass


def colorAscii(color: tuple[int, int, int]) -> str:
    """
    Generates an ASCII formatted string to color a pixel any color

    Arguments:
        color:
            The color of the ASCII
    """

    r, g, b = color
    return f"\x1b[38;2;{r};{g};{b}m"

def format_time(timestamp: float) -> str:
    """
    Formats a time to DD days, HH:MM:SS

    Arguments:
        timestamp:
            The timestamp in seconds
    """
    days = int(timestamp / 28800)
    hours = int((timestamp % 28800) / 1200)
    minutes = int((timestamp % 1200) / 60)
    seconds = int(timestamp % 60)

    return (f"{days} day{'s' if days>1 else ''}, " if days else "") + (f"{hours:02}:" if hours or days else "") + f"{minutes:02}:{seconds:02}"


class ProgressBar:
    """
    A progress bar that can output any standard textual output

    Call the bar in order to output a string

    ```
    bar = Progress_Bar(50)
    print(bar(0.5)) # Output at 50%
    ```
    """

    length: int
    completed_char: str = "━"
    start_time: float
    prev_time: float
    prev_pro: float
    format_str: str
    empty_char: str
    prev_est: float = 0.0

    def __init__(
        self,
        length: int,
        completed_char: Literal["━", "@"] | str = "━",
        empty_char: str = " ",
        format_str: str = "[{bar}] ({progress_per:>3}%) | Current: {current} | Estimate: {estimate}",
    ) -> None:
        """
        A progress bar that can output any standard textual output

        Call the bar in order to output a string

        Arguments:
            length:
                The total length of the bar (in characters)
            completed_color:
                The color of the filled ascii bar (or none for no color)
            completed_char:
                The character to use for the completed progress bar
            empty_char:
                The character to use for the empty background on the progress bar
            format_str:
                The format string

                bar - The bar string
                progress_per - The progress percentage (0-100)
                progress_per_f - The progress percentage as a float (0.0-100.0)
                current - The current time in HH:MM:SS (and days if required)
                estimate - The estimated remaining time in HH:MM:SS (and days if required)

        Examples:

        ```
        bar = Progress_Bar(50)
        print(bar(0.5)) # Output at 50%
        ```
        """

        # Set values
        self.length = length
        self.completed_char = completed_char
        self.empty_char = empty_char
        self.format_str = format_str

        # Get start time
        self.start_time = time.time()
        self.prev_time = self.start_time
        self.prev_pro = 0.0

    def format(self, *args, **kwargs) -> str:
        """
        Formats and returns the output

        Redefine this function for custom formatters
        """
        return self.format_str.format(*args, **kwargs)

    def __call__(self, progress: float) -> str:
        """
        Outputs the progress bar as a string

        If use_time is on the current time along with a remaining estimate will be added at the end

        Arguments:
            progress:
                The current progress from [0-1]
        """

        progress_per = int(progress * 100)
        progress_per_f = progress * 100

        # Calculate estimate time
        curr_time = time.time()
        remaining_estimate = 0
        if self.prev_pro - progress != 0:
            remaining_estimate = (((curr_time - self.prev_time) / (progress - self.prev_pro)) + self.prev_est) / (2 if self.prev_est else 1)
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
        return self.format(
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


def import_absolute(path: str):
    """
    Returns a module based on supplied path

    Arguments:
        path:
            The path to load from (should end in .py)
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

    Arguments:
        url:
            The exact url to the downloadable file
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
):
    """
    Generates an interpolator to nicely move between two edge colors

    The output is an iterator of colors in which the first is the color1 and the last is the color2, with each next being a step towards the end

    ```for color in interpolate(red,green,10):...
    ```

    Arguments:
        color1:
            The starting color
        color2:
            The ending color
        steps:
            The number of steps it should take
        exact:
            If the output rgb values should be in exact floats instead of being rounded to integers
    """

    # Get the change in each color in each step
    delta = (
        (color2[0] - color1[0]) / (steps - 1),
        (color2[1] - color1[1]) / (steps - 1),
        (color2[2] - color1[2]) / (steps - 1),
    )

    return _ColInterpolateGenerator(color1, color2, delta, steps, exact)


def listdir_recurse(path: str, include_folder: bool = False):
    """
    Lists all the files found under {path} starting with {path}

    Arguments:
        path:
            The path to start checking under
        include_folder:
            Includes folder paths as well as files
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
