import logging
import sys


class StdoutFormatter(logging.Formatter):
    """
    Custom formatter for adding colors to stdout
    """

    level_colors: dict[int, str]

    level_formatters: dict[int, logging.Formatter]

    default_formatter = logging.Formatter(
        fmt="\x1b[38;5;20m[%(asctime)s]\x1b[0m [%(name)s/%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    def __init__(self):

        self.level_colors = {
            logging.DEBUG: "\x1b[38;5;245m",
            logging.INFO: "\x1b[38;5;10m",
            logging.WARNING: "\x1b[38;5;11m",
            logging.ERROR: "\x1b[38;5;196m",
            logging.CRITICAL: "\x1b[38;5;129m",
        }

        self.level_formatters = {}

        for level, color in self.level_colors.items():

            self.level_formatters[level] = logging.Formatter(
                fmt=f"\x1b[38;5;20m[%(asctime)s]\x1b[0m [%(name)s/{color}%(levelname)s\x1b[0m] %(message)s",
                datefmt="%H:%M:%S",
            )

    def format(self, record: logging.LogRecord):

        if record.levelno in self.level_formatters:

            return self.level_formatters[record.levelno].format(record)

        else:

            return self.default_formatter.format(record)


def style(
    filename: str | None = None,
    mode: str = "w",
    stdout: bool = False,
    level: int = logging.WARNING,
) -> None:
    """
    Enables gregium-style logging formatting

    You can use any combination of settings

    :param filename: The path to log to (or None for no logging file)
    :type filename: str | None, optional, defaults to None
    :param mode: The mode to log the file in, this is only used if a logging file is specified (generally should be w to clear log but can also be a to add to the end of the file), defaults to "w"
    :type mode: str, optional
    :param stdout: To log to standard output (terminal), defaults to False
    :type stdout: bool, optional
    :param level: The minimum logging level to log, defaults to logging.WARNING
    :type level: int, optional
    """

    handlers = []

    # Make stdout handler
    if stdout:

        stdout_handler = logging.StreamHandler(sys.stdout)

        stdoutFormatter = GeneratedStdoutFormatter

        stdout_handler.setFormatter(stdoutFormatter)

        stdout_handler.setLevel(level)

        handlers.append(stdout_handler)

    # Make file handler
    if filename is not None:

        file_handler = logging.FileHandler(filename=filename, mode=mode)

        file_handler.setFormatter(
            logging.Formatter(
                fmt="[%(asctime)s] [%(name)s/%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            )
        )

        file_handler.setLevel(level)

        handlers.append(file_handler)

    # Set settings and handlers
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s/%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[stdout_handler, file_handler],
        level=level,
    )


def addLevel(
    level: int, levelName: str, levelColor: tuple[int, int, int] = (255, 255, 255)
) -> None:
    """
    Associate 'levelName' with 'level'.

    This is used when converting levels to text during message formatting.

    Also adds a color when printing to standard output (terminal)

    :param level: The logging level number
    :type level: int
    :param levelColor: The color for the level in rgb
    :type levelColor: tuple[int,int,int], optional
    """

    # Add name
    logging.addLevelName(level, levelName)

    # Make color
    r, g, b = levelColor

    color_code = f"\x1b[38;2;{r};{g};{b}m"

    # Add color value
    GeneratedStdoutFormatter.level_colors[level] = color_code

    # Add color formatter
    GeneratedStdoutFormatter.level_formatters[level] = logging.Formatter(
        fmt=f"\x1b[38;5;20m[%(asctime)s]\x1b[0m [%(name)s/{color_code}%(levelname)s\x1b[0m] %(message)s",
        datefmt="%H:%M:%S",
    )


# Make stdout formatter
GeneratedStdoutFormatter = StdoutFormatter()
