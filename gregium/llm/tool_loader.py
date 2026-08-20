from collections.abc import Callable

from ..verification import verify_exists

verify_exists("ollama", "ollama")
from ollama import _utils


def func_from_annotation(function:Callable) -> dict:
    """
    Generates a func dict from a function using the ollama library

    :param function: The function to annotate
    :type function: Callable

    :return: The tool dictionary for use in AI models that support tools
    :rtype: dict
    """

    return _utils.convert_function_to_tool(function).model_dump()
