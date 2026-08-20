import inspect
import shlex
import textwrap
from collections.abc import Callable
from typing import Any, TypeAlias

Command: TypeAlias = Callable[..., str]


def _load_argument(argument: str) -> float | str | int | bool:
    """
    Attempts to load the given argument to the closest possible type

    :param argument: The single argument
    :type argument: str
    """

    if argument.startswith('"'):

        return argument.strip('"')

    if argument == "true" or argument == "True":

        return True

    if argument == "false" or argument == "False":

        return False

    if argument.isnumeric():

        return int(argument)

    if argument.replace(".", "").isnumeric():

        return float(argument)

    return argument


class CommandTree:
    """
    A simple command tree for running commands closely to the terminal style

    For help use the 'help' command

    To run the interpreter use the `__call__` function
    """

    commands: dict[str, Command]
    "A dictionary of commands in the tree"

    def __init__(self):

        self.commands = {"help": self._help}

    def add_command(self, command: Command, name: str = ""):
        """
        Adds the given command to the tree

        :param command: The command
        :type command: Callable
        :param name: The name of the command (otherwise it will assume the function name)
        :type name: str, optional
        """

        name = name or command.__name__
        if name in self.commands:
            raise IndexError(f"Command '{name}' already exists on the given tree")
        self.commands[name] = command

    def _help(self, command: str | None = None) -> str:
        """
        Attempts to find the information on a given command
        When called without arguments, will instead return a list of commands

        :param command: The command name
        :type command: str
        """

        if command is None:

            # List commands
            out: str = (
                "Command Interpreter\n\nCommands must be formatted as follows:\n`command_name arg1_value arg2_value --kwarg1 kwarg1_value --kwarg2 kwarg2_value`\nWhich equates to:\n`command(arg1_value,arg2_value,kwarg1=kwarg1_value,kwarg2=kwarg2_value)`\n\nPositional arguments can be written as keyword arguments (for example, you could run `help command_name` or `help --command command_name`)\n\nCommand List:\n"
            )
            for cmd in self.commands:

                _cmd = self.commands[cmd]

                out += cmd

                if _cmd.__doc__ is None:

                    out += "\n"

                else:

                    out += (
                        ": "
                        + (
                            textwrap.dedent(
                                next(
                                    x
                                    for x in _cmd.__doc__.split("\n")
                                    if textwrap.dedent(x) != ""
                                )
                            )
                        )
                        + "\n"
                    )

            return out

        if command not in self.commands:

            return f"Unknown command '{command}', call help without arguments for a list of commands"

        _command = self.commands[command]

        sig = inspect.signature(_command)

        if _command.__doc__ is None:

            return f"{command}{sig}\n\n\tNo description provided"

        else:

            return f"{command}{sig}\n{"\n".join([f"\t{x}" for x in textwrap.dedent(_command.__doc__).splitlines()])}"

    def __call__(self, command: str) -> str:
        """
        Attempt to run the given command

        :param command: The command string with arguments included
        :type command: str

        :return: The output of the command
        :rtype: str
        """

        # Compile command
        raw_cmd = shlex.split(command, posix=False)

        if len(raw_cmd) == 0:
            return "No input, type 'help' for help"

        if len(raw_cmd) == 1:
            command_name = raw_cmd[0]

        else:
            command_name, *raw_arguments = raw_cmd

        # Find valid command
        try:
            command_inst = self.commands[command_name]
        except KeyError:
            return f"Command '{command_name}' not found, type 'help' for help"

        if len(raw_cmd) == 1:
            return command_inst()

        # Parse arguments
        kwargs: dict[str, Any] = {}
        args: list[Any] = []

        kwarg_name: str | None = None
        found_kwarg: bool = False
        for arg in raw_arguments:

            if arg.startswith("--"):

                found_kwarg = True

                if kwarg_name:

                    return f"Command failed to parse, missing keyword argument value for '{kwarg_name}'"

                kwarg_name = arg.lstrip("-")

                if kwarg_name in kwargs:

                    return f"Command failed to parse, duplicate keyword arguments '{kwarg_name}'"

            elif kwarg_name:

                kwargs[kwarg_name] = _load_argument(arg)

                kwarg_name = None

            else:

                if found_kwarg:

                    return "Command failed to parse, positional argument found after keyword argument"

                args.append(_load_argument(arg))

        if kwarg_name:

            return f"Command failed to parse, missing value for keyword argument '{kwarg_name}'"

        # Run command
        try:
            return command_inst(*args, **kwargs)
        except Exception as e:

            return f"Error while running command: {e}"

    def __str__(self):

        return self._help()
