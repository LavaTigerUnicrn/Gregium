import shlex
import textwrap
import json
import traceback

class CommandTree:
    """
    A tree of commands that can be called easily
    
    Uses shell notation of calling
    `command arg1 arg2 --kwarg1 kwarg1Value --kwarg2 kwarg2Value`
    
    To call the command tree, call the tree object
    `(command_str)`
    
    Default commands:
    list : Shows a list of all commands
    help --command : Shows the help for a specific command
    """
        
    commands:dict
    use_trace:bool
    
    def __init__(self):
        """
        Generates a new CommandTree
        """
        
        self.commands = {"help":self.help,"list":self.list_commands,"trace":self.trace}
        use_trace = False
        
    def add_command(self,command):
        """
        Adds or updates a command in the tree
        
        Arguments:
            command: The command to add
        """
        
        # Add command
        self.commands[command.__name__] = command
        
    def help(self,command:str=None):
        """
        Gives help docstring for command
    
   	Uses shell notation of calling
    	`command arg1 arg2 --kwarg1 kwarg1Value --kwarg2 kwarg2Value`
    
    	To call the command tree, call the tree object
    	`(command_str)`
    
    	Default commands:
    	    list : Shows a list of all commands
    	    help --command : Shows the help for a specific command
            trace --enable : Sets the tracing for errors
        
        Arguments:
            command: The command to get help on
        """
        
        # Give help if command is none
        if command is None:
            
            command = "help"
        
        # Get command
        if command not in self.commands:
            return f"Unknown command: {command}"
        return f"({command}) command:\n{"\n".join([f"    {x}" for x in textwrap.dedent(self.commands[command].__doc__).strip().splitlines()])}"
    
    def list_commands(self):
        """
        Lists all commands
        """
        
        # List commands
        return "List of commands on current tree:\n    "+"\n    ".join(self.commands.keys())
    
    def trace(self,enable:bool):
        """
        Sets if the errors should be traced
        
        enable: The state 
        """
        
        self.use_trace = enable
        
    def __call__(self,command_str:str):
        """
        Runs the command based on the string
        
        Uses shell notation of calling
        `command arg1 arg2 --kwarg1 kwarg1Value --kwarg2 kwarg2Value`
        
        Default commands:
        list : Shows a list of all commands
        help --command : Shows the help for a specific command
        """
        
        # Split the command
        try:
            command_name,*split_command = shlex.split(command_str, posix=False)
        except Exception as e:
            return f"Command failed to parse: {e}"    
        
        # Check if command exists
        if command_name not in self.commands:
            return f"Unknown command: {command_name} (use help for help on commands)"
        
        # Get args and kwargs
        kwargs = {}
        args = []
        kwarg_name = None
        for argument in split_command:
            try:
                if argument.startswith("--"):
                    kwarg_name = argument[2:]
                elif kwarg_name:
                    try:
                        kwargs[kwarg_name] = json.loads(argument)
                    except:
                        kwargs[kwarg_name] = argument
                    kwarg_name = None
                else:
                    try:
                        args.append(json.loads(argument))
                    except:
                        args.append(argument)
            except Exception as e:
                return f"Command failed to parse arguments: {e}"
        if kwarg_name:
            return "Invalid command parameters, kwarg must have value"
        
        try:
            return self.commands[command_name](*args,**kwargs)
        except Exception as e:
            print(traceback.format_exc())
            return f"Command had an error: {e}"