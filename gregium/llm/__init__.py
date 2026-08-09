import logging
from collections.abc import Callable, Iterator
from typing import Any, Literal, TypeAlias

Role: TypeAlias = Literal["user", "system", "assistant", "tool"]

# Setup
logger = logging.getLogger(__name__)

class ChatBot:

    tools:list[Callable]
    message_history:list[dict[str,Any]]
    queued_tools:list[dict[str,Any]]

    def __init__(self):

        self.message_history = []
        self.queued_tools = []
        self.tools = []

    def clear_history(self) -> None:
        self.message_history = []

    def add_tool(self,tool: Callable) -> None:

        # Add tool
        self.tools.append(tool)

    def run_tool(self,tool_name:str,arguments:dict,id:str|None=None) -> None:

        # Get the tool to run
        for tool in self.tools:
            if tool.__name__ == tool_name:
                tool_inst = tool
                break
        
        # Run the function
        try:
            logger.info(f"Running tool [{tool_name}] with arguments: {arguments}")
            output = tool_inst(**arguments)
        except Exception as e:
            logger.exception("Tool failed to run")
            output = f"The tool {tool_name} failed to run\n{e}"
        
        # Return to the AI
        output = {"content":str(output),"role":"tool","tool_name":tool_name}
        if id is not None:
            output["id"] = id
        
        self.message_history.append(output)

    def run_tools(self) -> None:

        # Run all tools and clear
        for tool in self.queued_tools:

            id = None
            if "id" in tool:
                id = tool["id"]

            self.run_tool(tool["name"],tool["arguments"],id)

        self.queued_tools = []

    def tell(self,prompt:str,role:str="user"):

        # Format prompt
        prompt_formatted = {"role":role,"content":prompt}

        # Ensure queue is empty
        if len(self.queued_tools) > 0:
            raise BufferError("Tools queued have not been run yet, use `run_tools` before attempting to add to the message queue")

        # Add prompt to history
        self.message_history.append(prompt_formatted)

    def chat(self,prompt:str,role:str="user") -> str:

        # Take content attribute of response
        return self.chat_raw(prompt,role)["content"]

    def chat_stream(self,prompt:str,role:str="user") -> Iterator[str]:

        # Take content attribute of each response section
        out = (x["content"] for x in self.chat_stream_raw(prompt,role))
        return out

    def chat_raw(self,prompt:str,role:str="user") -> dict:

        # Tell and flush
        self.tell(prompt,role)
        return self.flush()

    def chat_stream_raw(self,prompt:str,role:str="user") -> Iterator[dict]:

        # Tell and flush stream
        self.tell(prompt,role)
        return self.flush_stream()

    def flush(self) -> dict:
        raise NotImplementedError()

    def flush_stream(self) -> Iterator[dict]:
        raise NotImplementedError() 
