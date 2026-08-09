"""
Base chatbots
"""

from collections.abc import Callable, Iterator
from typing import Any, Literal, TypeAlias

Role: TypeAlias = Literal["user", "system", "assistant", "tool"]

class ChatBot:
    """
    The base ChatBot

    This has almost no function but is built as a base for other bots for standard syntax

    #### WHEN MAKING SUBCLASS

    1) Overwrite the __init__ and class docstring
    2) If implementing a custom __init__ method, call `super().__init__()`
    3) Implement the 'flush' method
    4) Implement the 'flush_stream' method
    """

    tools: list[Callable]
    "A list of callable tools as python functions"
    message_history: list[dict[str, Any]]
    "The message history"
    queued_tools: list[dict[str, Any]]
    "The currently waiting tools to be run"

    def __init__(self):
        """
        The base ChatBot

        This does nothing by itself

        #### WHEN MAKING SUBCLASS

        1) Overwrite the __init__ and class docstring
        2) If implementing a custom __init__ method, call `super().__init__()`
        3) Implement the 'flush' method
        4) Implement the 'flush_stream' method
        """

    def clear_history(self) -> None:
        """
        Wipes all memory of the bot (does not clear tools)
        """

    def add_tool(self, tool: Callable) -> None:
        """
        Adds a tool to the given bot that it can call whenever

        Arguments:
            tool:
                The python function that will be converted into an AI tool

                This must follow specific docstring format (Including the name 'args' and 'returns')

        Examples:
            def add_two_numbers(a: int, b: int) -> int:

            \"\"\"

            Add two numbers together.

            Args:

                a: First number to add
                b: Second number to add

            Returns:

                int: The sum of a and b

            \"\"\"

            return a + b
        """

    def run_tool(self, tool_name: str, arguments: dict, id: str | None = None) -> None:
        """
        Runs the tool and adds the output to the current message history (as a dict)

        Does not re-prompt the bot once the tool has been run

        Arguments:
            tool_name:
                The name of the tool to run

                This must have already been added to the bot
            argument:
                The tool kwargs
            id:
                The id of the tool call

                Some bots don't include the 'id' so it isn't required unless the bot specifically wants it
        """

    def run_tools(self) -> None:
        """
        Runs all tools
        """

    def tell(self, prompt: str, role: Role = "user"):
        """
        Adds the prompt to the bots message history without expecting any response

        Arguments:
            prompt:
                The prompt to send
            role:
                The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses
        """

    def chat(self, prompt: str, role: Role = "user") -> str:
        """
        Generates and returns the response from the chatbot
        This will remember all previous responses

        Arguments:
            prompt:
                The prompt to send
            role:
                The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses

        Returns:
            The response message content of the AI
        """

    def chat_stream(self, prompt: str, role: Role = "user") -> Iterator[str]:
        """
        Returns a generator for the response from the chatbot where each token (word) is the next object
        This will remember all previous responses

        Arguments:
            prompt:
                The prompt to send
            role:
                The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses

        Returns:
            The response message content of the AI
        """

    def chat_stream_raw(self, prompt: str, role: Role) -> Iterator[dict]:
        """
        Returns a generator for the raw response message from the chatbot
        This will remember all previous responses

        Arguments:
            prompt:
                The prompt to send
            role:
                The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses

        Returns:
            The response of the AI
        """

    def chat_raw(self, prompt: str, role: Role) -> dict:
        """
        Generates and returns the raw response message from the chatbot
        This will remember all previous responses

        Arguments:
            prompt:
                The prompt to send
            role:
                The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses

        Returns:
            The response of the AI
        """

    def flush(self) -> dict:
        """
        Prompts the AI to generate the next message

        Returns:
            The response of the AI

        #### WHEN MAKING SUBCLASS

        This is the primary function to overwrite for the ChatBot to function (along with flush_stream)

        It should

        1) Prompt the AI to generate a new response
        2) Add the message to the 'message_history'
        3) Return the **message** component of the response
        4) Add all tools calls to the 'queued_tools' variable
            1) The tools should be formatted as `{"name":func_name,"arguments":{arg1:arg1_value,arg2:arg2_value},"id":id}`
            2) The id is optional (only certain bots require it), only include it if the bot gave it
        """

    def flush_stream(self) -> Iterator[dict]:
        """
        Prompts the AI to generate the next message as a stream

        Returns:
            The response of the AI

        #### WHEN MAKING SUBCLASS

        This is the primary function to overwrite for the ChatBot to function (along with flush)

        It should

        1) Prompt the AI to generate a new response with streaming enabled
        2) Yield until the stream finishes (once done continue to 3-5)
        3) Add the message to the 'message_history'
        4) Return the **message** component of the response
        5) Add all tools calls to the 'queued_tools' variable
            1) The tools should be formatted as {"name":func_name,"arguments":[arg1,arg2],"id":id}
            2) The id is optional (only certain bots require it)
        """
