"""
A ChatBot using Ollama

Use .hf for HuggingFace version
"""

import logging
from collections.abc import Iterator
from typing import Any

from ..verification import verify_exists
from . import ChatBot

verify_exists("ollama","ollama")

import ollama

logger = logging.getLogger(__name__)

class OllamaChatBot(ChatBot):
    """
    A ChatBot using Ollama
    """

    model:str
    'The model name'
    message_history:list[dict[str,Any]|ollama.Message]
    "The message history, can contain Ollama messages or normal dictionaries (same format)"

    def __init__(self,model:str):
        """
        A ChatBot using Ollama

        Arguments:
            model:
                The model name
        """

        super().__init__()
        self.model = model

    def flush(self) -> ollama.Message:

        response:ollama.ChatResponse = ollama.chat(self.model,self.message_history,tools=self.tools)
        message = response.message

        # Queue tools
        if message.tool_calls is not None:
            for tool in message.tool_calls:

                self.queued_tools.append({"name":tool.function.name,"arguments":tool.function.arguments})

        return message

    def flush_stream(self) -> Iterator[ollama.Message]:

        response:Iterator[ollama.ChatResponse] = ollama.chat(self.model,self.message_history,tools=self.tools,stream=True)

        # Get all tokens in the response
        for token in response:

            message = token.message

            if token.done:

                # Queue tools
                if message.tool_calls is not None:
                    for tool in message.tool_calls:
                
                        self.queued_tools.append({"name":tool.function.name,"arguments":tool.function.arguments})

                return message
            else:
                yield message