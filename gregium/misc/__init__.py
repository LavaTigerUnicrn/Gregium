import os
from typing import Literal
import importlib.util as import_util
import time

Term_Type = Literal["powershell","cmd"]

def open_terminal(path:str,terminal_type:Term_Type="powershell"):
    """
    Quickly pops open terminal
    
    Arguments:
        path:
            The path to open terminal to
    """
    
    if terminal_type == "cmd":
        
        os.system(f"start cmd /K \"cd {path}\"")
        
    else:

        os.system(f"start powershell -NoExit -Command \"cd {path}\"")

def colorAscii(color:tuple[int,int,int]) -> str:
    """
    Generates an ASCII formatted string to color a pixel any color
   
    Arguments:
        color:
            The color of the ASCII
    """
   
    r,g,b = color
    return f"\x1b[38;2;{r};{g};{b}m"


def loading_bar(length:int,progress:float,completed_color:tuple[int,int,int]=(0,255,0)) -> str:
    """
    Generates an ASCII loading bar
    
    Arguments:
        length:
            The total length of the bar (in characters)
        progress:
            The progress of the bar [0-1]
        completed_color:
            The color of the filled ascii bar
    """
    
    curr_length = int(length*progress)
    
    return colorAscii(completed_color)+"@"*curr_length+"\x1b[0m"+"@"*(length-curr_length)

def loading_bar_adv(length:int,percent:float,start_time:float,completed_color:tuple[int,int,int]=(0,255,0)):
    """
    A slightly more advanced version of `loading_bar`
    
    Tracks current time and estimated time
    
    Arguments:
        length:
            The total length of the bar (in characters)
        progress:
            The progress of the bar [0-1]
        start_time:
            The epoch in which the thing started loading
        completed_color:
            The color of the filled ascii bar
    """
    
    filled = int(length*percent)
    remaining = length - filled
    curr_time = time.time()
    
    # Format time
    time_rem = (curr_time - start_time)
    time_str = str(int(time_rem))
    if percent != 0:
        guess_str = str(int(time_rem / percent) - int(time_rem))
    else:
        guess_str = "Unknown"
    
    return colorAscii(completed_color)+"@"*filled+"\x1b[0m"+"@"*remaining+f" ({int(percent*100):>3}%) Current: "+time_str+"s | Remaining: "+guess_str+"s"


def import_absolute(path:str):
    """
    Returns a module based on supplied path
    
    Arguments:
        path:
            The path to load from (should end in .py)
    """
    
    # Get name
    name = os.path.basename(path).removesuffix(".py")
    
    # Import
    spec = import_util.spec_from_file_location(name,path)
    module = import_util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Return output
    return module