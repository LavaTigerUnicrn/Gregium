"""
A ChatBot using HuggingFace

Use .ollama for Ollama version
"""

import logging

import requests

from . import ChatBot
from . import tool_loader

logger = logging.getLogger(__name__)

# Get headers and URL
API_URL = "https://router.huggingface.co/v1/chat/completions"
"The API url to HuggingFace"

API_KEY: str | None = None
"The API key for HuggingFace"

def set_hf_key(api_key: str):
    """
    Sets the global API key so that the api_key parameter can be left out in HuggingFace functions

    https://huggingface.co/settings/tokens
    """

    global API_KEY

    API_KEY = api_key


def chat_hf(
    model: str,
    messages: list[dict],
    tools: list | None = None,
) -> dict:
    """
    Requests output from HuggingFace servers

    Arguments:
        model:
            The API link of the HuggingFace model
        messages:
            The previous messages in a dictionary
        tools:
            The tools for the AI to use
    """


    if API_KEY is None:
        raise ValueError(
            "API key not specified, call `set_hf_key()` to set"
        )

    api_key = API_KEY

    # Make header
    header = {
        "Authorization": f"Bearer {api_key}",
    }

    # Format payload
    payload = {"messages": messages, "model": model}

    # Fix tools (if present)
    if tools is not None:

        tools_list = []
        for tool in tools:

            tools_list.append(tool_loader.func_from_annotation(tool))

        payload["tools"] = tools_list

    # Query
    response = requests.post(API_URL, headers=header, json=payload)
    return response.json()


class HFChatBot(ChatBot):
    """
    A ChatBot using HuggingFace
    """

    api: str
    "The api link"

    def __init__(self, api: str):
        """
        A ChatBot using HuggingFace

        Arguments:
            model:
                The API link of the HuggingFace model, for example: Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway
                This can generally be found on the page under "deploy" (if it isn't present then it doesn't exist)
        """

        super().__init__()
        self.api = api

    def flush(self) -> dict:

        response: dict = chat_hf(
            self.api, self.message_history, tools=self.tools
        )
        message = response[0]["message"]

        # Queue tools
        if message["tool_calls"] is not None:
            for tool in message["tool_calls"]:

                self.queued_tools.append(
                    {"name": tool["function"]["name"], "arguments": tool["function"]["arguments"],"id": tool["id"]}
                )

        return message

    def flush_stream(self) -> None:

        raise NotImplementedError("No method to stream HuggingFace")