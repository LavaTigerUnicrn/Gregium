"""
The 3 basic levels of logs to file

info
error
warn

It is recommended to use "from basic_logs import *" 
in order to use the log levels most easily
"""

import inspect
from ..logger import write_log
import os

def resolve_caller(frame:inspect.FrameInfo) -> str:
    """
    Attempts to find the library location from which a file has been called from
    """
    
    # Get filename
    filename = frame.filename
    
    # Get current working directory
    cwd = os.getcwd()

    # Strip to relative
    filename = filename.replace(cwd,"")
    
    # Remove extra \ at start
    filename = filename.lstrip("\\")
    
    # Format similar to python
    filename = filename.replace(".py","").replace("\\",".")
    
    # Remove __init__ if present
    filename = filename.replace(".__init__","")
    
    return filename

def info(text:str,parent:str|None=None):
    """
    Log with level of INFO
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            If no parent is given it will try to automatically find
            
            *It's best to use __name__ in this argument
    """
    # Attempt to find parent
    if parent == None:
        
        parent = resolve_caller(inspect.stack()[1])
    
    write_log(text,"INFO",parent)
    
def warn(text:str,parent:str|None=None):
    """
    Log with level of WARN
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            If no parent is given it will try to automatically find
            
            *It's best to use __name__ in this argument
    """
    # Attempt to find parent
    if parent == None:
        
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text,"WARN",parent)
    
def error(text:str,parent:str|None=None):
    """
    Log with level of ERROR
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            If no parent is given it will try to automatically find
            
            *It's best to use __name__ in this argument
    """
    # Attempt to find parent
    if parent == None:
        
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text,"ERROR",parent)
    
def debug(text:str,parent:str|None=None):
    """
    Log with level of DEBUG
    DEBUG levels should only be used temporarily for debugging purposes
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            If no parent is given it will try to automatically find
            
            *It's best to use __name__ in this argument
    """
    # Attempt to find parent
    if parent == None:
        
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text,"DEBUG",parent)
    
def critical(text:str,parent:str|None=None):
    """
    Log with level of CRITICAL
    CRITICAL levels should only be used in cases where continuation of the program is impossible
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            If no parent is given it will try to automatically find
            
            *It's best to use __name__ in this argument
    """
    # Attempt to find parent
    if parent == None:
        
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text,"CRITICAL",parent)