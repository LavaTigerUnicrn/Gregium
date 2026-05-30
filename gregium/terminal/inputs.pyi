from typing import Any

def clear():
    """
    Clears the terminal window, resets text effects, and homes cursor
    """
def getch(flush:bool=True) -> str|bytes:
    """
    Gets the next pressed input on the terminal
    
    Arguments:
        flush:
            Whether or not to flush the previous inputs when getch starts
    """
def start():
    """
    Gets the terminal ready for getch
    """
def end():
    """
    Reset the terminal to default settings
    """
def input(text:str="") -> str:
    """
    Input for any text
    
    Arguments:
        text:
            Starting text to print before input starts
    """
def options_from_dict(options:dict[Any,dict[str,str]]) -> dict[str,str]:
    """
    Automatically generates the keyword arguments for options,optionsName, and optionsDesc using a dictionary
    
    To use correctly the format should be
    
    ```
    choices = {
        "choice one": {"name":"Hello!"}
        "choice two": {"desc":"Goodbye"}
    }
    
    # Ensure to use '**' right before the call to work correctly
    # The options, options_name, and options_desc kwargs will be filled in
    # any other kwargs may be used as normal
    chosen = choice(**options_from_dict(choices),...)
    
    ```
    
    Dictionary format
    {value:{"name":name,"desc":description}}
    
    Schema can be missing and will be auto-filled
    {value:{}}
    {value:{"name":name}}
    {value:{"desc":description}}
    
    Arguments:
        options: The dictionary of options
    """
def choice(options:list[Any],optionsName:list[str]|None=None,optionsDesc:list[str]|None=None,help:bool=True|False,customEscOut:Any|None=None) -> Any:
    """
    Makes a choice input for given choices in terminal
    
    Arguments:
        options:
            The valid choices (this is also the possible outputs)
        optionsName:
            The names of the choices that are listed (must be the same length as options)
        optionsDesc:
            The hover description of the choices (must be the same length as options)
        help:
            Whether or not the help text should show
        customEscOut:
            A custom output for if the user presses esc
    """
def choice_centered(options:list[Any],optionsName:list[str]|None=None,optionsDesc:list[str]|None=None,help:bool=True|False,startLine:int=None) -> Any:
    """
    Makes a choice input for given choices in terminal
    
    Arguments:
        options:
            The valid choices (this is also the possible outputs)
        optionsName:
            The names of the choices that are listed (must be the same length as options)
        optionsDesc:
            The hover description of the choices (must be the same length as options)
        help:
            Whether or not the help text should show 
        start_line:
            The first line the choice should start on (otherwise will use current cursor position)
    """
def input_single_line():
    """
    Inputs text on the same line as the cursors current position
    """
def get_cursor_position() -> tuple[int,int]:
    """
    Gets the current location of the text cursor (y,x)
    """
def print(text="",end:str="\n",flush:bool=True):
    """
    Replacement print function
    
    Arguments:
        text:
            Text to print
        end:
            End text of the print function
        flush:
            Whether to flush stdout
    """
def ctrl_backspace(text:str) -> tuple[int,str]:
    """
    Emulates ctrl + backspace of windows
    
    Returns tuple of [characters removed,new string]
    
    Arguments:
        text:
            The text to apply control backspace to
    """
def ctrl_delete(text:str) -> tuple[int,str]:
    """
    Emulates ctrl + delete of windows (starts from the start of text)
    
    Returns tuple of [characters removed,new string]
    
    Arguments:
        text:
            The text to apply control backspace to
    """
def ctrl_left(text:str) -> int:
    """
    Finds the cursor shift to the left of using ctrl+left on the end of text
    
    Arguments:
        text:
            The text to find the cursor position of
    """
    
def ctrl_right(text:str) -> int:
    """
    Finds the cursor shift to the right of using ctrl+right on the start of text
    
    Arguments:
        text:
            The text to find the cursor position of
    """
def get_terminal_length() -> int:
    """
    Gets the length of the terminal in characters
    
    Will clear terminal
    
    **THIS MAY NOT WORK ON POSIX**
    """
def get_terminal_height() -> int:
    """
    Gets the height of the terminal in characters
    
    Will clear terminal
    
    **THIS MAY NOT WORK ON POSIX**
    """
def verify_terminal_length(min_size:int) -> bool:
    """
    Ensures terminal is of a certain length
    
    Arguments:
        min_size:
            The minimum width the terminal is allowed ot be (characters)
            
    Will return True if terminal has passed check
    
    **THIS MAY NOT WORK ON POSIX**
    """
def centered_print(text:str,flush:bool=True,line:int=1):
    """
    Prints text in the center of the screen on line
    
    Newlines will all be aligned at center
    
    **MUST RUN `get_size` BEFORE CENTERED PRINTING**
    
    Arguments:
        text:
            Text to print
        line:
            Line to write text on
        flush:
            Whether to flush stdout
    """
def get_size() -> tuple[int,int]:
    """
    Gets the size of the terminal and stores for `centered_print` function
    
    Outputs size in form of (width,height)
    """
HEIGHT:int # Height of the terminal (only after calling get_size)
WIDTH:int # Width of the terminal (only after calling get_size)