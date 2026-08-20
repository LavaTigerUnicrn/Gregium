import logging
from collections.abc import Callable, Iterator
from typing import Any, Literal, TypeAlias

Role: TypeAlias = Literal["user", "system", "assistant", "tool"]

# Setup
logger = logging.getLogger(__name__)

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

        self.message_history = []
        self.queued_tools = []
        self.tools = []

    def clear_history(self) -> None:
        """
        Wipes all memory of the bot (does not clear tools)
        """
        self.message_history = []

    def add_tool(self,tool: Callable) -> None:
        """
        Adds a tool to the given bot that it can call whenever
        
        :param tool: The python function that will be converted into an AI tool
        
                This must follow specific docstring format (Including the name 'args' and 'returns')
        :type tool: Callable
        
        .. code-block:: python3

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

        # Add tool
        self.tools.append(tool)

    def run_tool(self,tool_name:str,arguments:dict[str,Any],id:str|None=None) -> None:
        """
        Runs the tool and adds the output to the current message history (as a dict)
        
        Does not re-prompt the bot once the tool has been run
        
        :param tool_name: The name of the tool to run
        
            This must have already been added to the bot
        :type tool_name: str
        :param arguments: The tool kwargs
        :type arguments: dict[str,Any]
        :param id: The id of the tool call
        
            Some bots don't include the 'id' so it isn't required unless the bot specifically wants it
        :type id: int, optional
        """

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
        """
        Runs all queued tools
        """

        # Run all tools and clear
        for tool in self.queued_tools:

            id = None
            if "id" in tool:
                id = tool["id"]

            self.run_tool(tool["name"],tool["arguments"],id)

        self.queued_tools = []

    def tell(self,prompt:str,role:Role="user"):
        """
        Adds the prompt to the bots message history without expecting any response
        
        :param prompt: The prompt to send
        :type prompt: str
        :param role: The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses
        :type role: str, optional
        """

        # Format prompt
        prompt_formatted = {"role":role,"content":prompt}

        # Ensure queue is empty
        if len(self.queued_tools) > 0:
            raise BufferError("Tools queued have not been run yet, use `run_tools` before attempting to add to the message queue")

        # Add prompt to history
        self.message_history.append(prompt_formatted)

    def chat(self,prompt:str,role:Role="user") -> str:
        """
        Generates and returns the response from the chatbot
        This will remember all previous responses
        
        :param prompt: The prompt to send
        :type prompt: str
        :param role: The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses
        :type role: str, optional
        
        :return: The response message content of the AI
        :rtype: str
        """

        # Take content attribute of response
        return self.chat_raw(prompt,role)["content"]

    def chat_stream(self,prompt:str,role:Role="user") -> Iterator[str]:
        """
        Returns a generator for the response from the chatbot where each token (word) is the next object
        This will remember all previous responses
        
        :param prompt: The prompt to send
        :type prompt: str
        :param role: The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses
        :type role: str, optional
        
        :return: The response message content of the AI
        :rtype: Iterator[str]
        """

        # Take content attribute of each response section
        out = (x["content"] for x in self.chat_stream_raw(prompt,role))
        return out

    def chat_raw(self,prompt:str,role:Role="user") -> dict:
        """
        Generates and returns the raw response message from the chatbot
        This will remember all previous responses
        
        :param prompt: The prompt to send
        :type prompt: str
        :param role: The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses
        :type role: str, optional
        
        :return: The response of the AI
        :rtype: dict
        """

        # Tell and flush
        self.tell(prompt,role)
        return self.flush()

    def chat_stream_raw(self,prompt:str,role:Role="user") -> Iterator[dict]:
        """
        Returns a generator for the raw response message from the chatbot
        This will remember all previous responses
        
        :param prompt: The prompt to send
        :type prompt: str
        :param role: The role the prompt is coming from (this should almost always be 'user')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses
        :type role: str, optional
        
        :returns: The response of the AI
        :rtype: Iterator[dict]
        """

        # Tell and flush stream
        self.tell(prompt,role)
        return self.flush_stream()

    def flush(self) -> dict:
        """
        Prompts the AI to generate the next message
        
        :returns: The response of the AI
        :rtype: dict

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
        raise NotImplementedError()

    def flush_stream(self) -> Iterator[dict]:
        """
        Prompts the AI to generate the next message as a stream
        
        :returns: The response of the AI
        :rtype: Iterator[dict]

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
        raise NotImplementedError() 
