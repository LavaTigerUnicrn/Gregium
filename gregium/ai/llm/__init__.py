"""
A LLM with Ollama capabilities

Use `.huggingface` for the huggingface version
"""
import ollama
from typing import Literal
from ...settings import DEFAULT_MODEL
from ... import settings
import json
import requests
from . import tool_loader

Role = Literal["user","system","assistant","tool"]

class ChatBot:
    model:str
    message_history:list[ollama.Message]
    tools:list
    
    def __init__(self,model:str=DEFAULT_MODEL):
        """
        A chatbot using Ollama
        
        Arguments:
            model:
                The Ollama model name
        """
        
        self.model = model
        self.message_history = []
        self.tools = []
    
    def clear_history(self) -> None:
        """
        Wipes all remembered chat history with the model
        
        This includes all messages or responses from any roles
        
        This does not clear tools
        """
        self.message_history = []
        
    def add_tool(self,tool) -> None:
        """
        Adds a tool to the given bot
        
        Arguments:
            tool:
                The python function that will be converted into an AI tool
                
                This must follow Google style docstrings
                https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
                
        Examples:
            def add_two_numbers(a: int, b: int) -> int:
            
            Add two numbers together.

            Args:

                a: First number to add
                b: Second number to add

            Returns:

                int: The sum of a and b

            '''

            return a + b
        """
        
        # Add tool
        self.tools.append(tool)
    
    def run_tool(self,tool_name:str,arguments:dict,id:str|None=None):
        """
        Runs a tool and automatically returns to the AI
        
        Arguments:
            tool_name:
                The name of the tool to run
               
                This must have already been added to the bot
            argument:
                The tool kwargs
            id:
                The id of the tool call (some don't need this)
                
        Returns:    
            str: The response of the AI after the tool has been run
        """
        
        # Get the tool to run
        for tool in self.tools:
            if tool.__name__ == tool_name:
                tool_inst = tool
                break
        
        # Run the function
        try:
            output = tool_inst(**arguments)
        except Exception as e:
            print(e)
            output = "The tool failed to run, perhaps there is a missing or incorrect argument?"
        
        # Return to the AI
        output = {"content":str(output),"role":"tool"}
        if tool is not None:
            output["id"] = id
        
        self.message_history.append(output)
    
    def tell(self,prompt:str,role:Role="system") -> None:
        """
        Tells the chatbot something without expecting any response
        
        Arguments:
            prompt:
                The prompt to send
            role: 
                The role the prompt is coming from (this should almost always be 'system')
                user - The person chatting
                assistant - The AI bot
                system - For setting model attributes (how the model should act) on the current instance, this has the highest power
                tool - For tool responses
        """
        
        # Format prompt
        prompt_formatted = ollama.Message(role=role,content=prompt)

        # Add prompt to history
        self.message_history.append(prompt_formatted)
    
    def chat(self,prompt:str,role:Role="user",output_raw:bool=False,skip_send:bool=False) -> str:
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
            output_raw:
                Will output the full raw data of the output content as opposed to just the message
            skip_send:
                Will output using current messages, not new message
                
        Returns:
            The response message content of the AI
        """

        # Format prompt
        prompt_formatted = ollama.Message(role=role,content=prompt)

        # Add prompt to history
        if not skip_send:
            self.message_history.append(prompt_formatted)
    
        # Get AI response
        response = ollama.chat(model=self.model,messages=self.message_history,tools=self.tools)
        message = response["message"]
        
        # Add response to history
        self.message_history.append(message)
        
        # If response calls a tool, use that tool
        if "tool_calls" in message:
            
            # Get all the tools
            tool_calls = message["tool_calls"]
            
            # Run each tool
            for call in tool_calls:
                
                # Get a response from the final tool call
                self.run_tool(call["function"]["name"],call["function"]["arguments"])
            response = self.chat("",output_raw=True,skip_send=True)
            message = response["message"]
        
        # Return response
        if output_raw:
            return response
        return message["content"]
    

# Get headers and URL
API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADER = {
    "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
}

def query(model:str,messages:list[dict],tools:list|None=None):
    """
    Requests output from huggingface servers
    
    Arguments:
        model:
            The API link of the huggingface model
        messages:
            The previous messages in a dictionary
        tools:
            The tools for the AI to use   
    """
    
    # Format payload
    payload = {"messages":messages,"model":model}
    
    # Fix tools (if present)
    if tools is not None:
        
        tools_list = []
        for tool in tools:
            
            tools_list.append(tool_loader.func_from_annotation(tool))
            
        payload["tools"] = tools_list
    
    # Query 
    response = requests.post(API_URL, headers=HEADER, json=payload)
    return response.json()

class HF_ChatBot(ChatBot):
    
    message_history:list[dict]
    
    def __init__(self,model:str):
        """
        Makes a new chatbot using Huggingface
        
        Arguments:
            model:
                The API link of the huggingface model, for example: Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway
                This can generally be found on the page under "deploy"
        """
        
        self.model = model
        self.message_history = []
        self.tools = []
        
    def tell(self,prompt:str,role:Role="system") -> None:
        
        # Format prompt
        prompt_formatted = {"role":role,"content":prompt}

        # Add prompt to history
        self.message_history.append(prompt_formatted)
        
    def chat(self,prompt:str,role:Role="user",output_raw:bool=False,skip_send:bool=False) -> str:

        # Format prompt
        prompt_formatted = {"role":role,"content":prompt}

        # Add prompt to history
        if not skip_send:
            self.message_history.append(prompt_formatted)
    
        # Get AI response
        response = query(model=self.model,messages=self.message_history,tools=self.tools)
        message = response["choices"][0]["message"]
        
        # Add response to history
        self.message_history.append(message)
        
        # If response calls a tool, use that tool
        if "tool_calls" in message and message["tool_calls"] != []:
            
            # Get all the tools
            tool_calls = message["tool_calls"]
            
            # Run each tool
            for call in tool_calls:
                
                # Get a response from the final tool call
                self.run_tool(call["function"]["name"],json.loads(call["function"]["arguments"]),id=call["id"])
            response = self.chat("",output_raw=True,skip_send=True)
            message = response["choices"][0]["message"]
        
        # Return response
        if output_raw:
            return response
        return message["content"]