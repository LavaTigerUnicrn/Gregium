"""
The basic types of logs

**These are meant to be as close as possible to the logging library**

To find parents automatically, set FIND_PARENTS to true
"""

import inspect
import os
from ..logger import write_log

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

FIND_PARENTS:bool = False

def info(text:str,*args,parent:str|None=None):
    """
    Log with level of INFO
    
    Arguments:
        text:
            Text to log
        args:
            Can be used as args for string formatted (just as logging)
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    if FIND_PARENTS and parent is None:
        parent = resolve_caller(inspect.stack()[1])
    
    write_log(text % args,"INFO",parent)
    
def warn(text:str,*args,parent:str|None=None):
    """
    Log with level of WARN
    
    Arguments:
        text:
            Text to log
        args:
            Can be used as args for string formatted (just as logging)
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    if FIND_PARENTS and parent is None:
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text % args,"WARN",parent)
    
def warning(text:str,*args,parent:str|None=None):
    """
    Log with level of WARN
    
    Arguments:
        text:
            Text to log
        args:
            Can be used as args for string formatted (just as logging)
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    if FIND_PARENTS and parent is None:
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text % args,"WARN",parent)
    
def error(text:str,*args,parent:str|None=None):
    """
    Log with level of ERROR
    
    Arguments:
        text:
            Text to log
        args:
            Can be used as args for string formatted (just as logging)
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    if FIND_PARENTS and parent is None:
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text % args,"ERROR",parent)
    
def exception(text:str,*args,parent:str|None=None):
    """
    Log with level of ERROR
    
    Arguments:
        text:
            Text to log
        args:
            Can be used as args for string formatted (just as logging)
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    if FIND_PARENTS and parent is None:
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text % args,"ERROR",parent)
    
def debug(text:str,*args,parent:str|None=None):
    """
    Log with level of DEBUG
    
    Arguments:
        text:
            Text to log
        args:
            Can be used as args for string formatted (just as logging)
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    if FIND_PARENTS and parent is None:
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text % args,"DEBUG",parent)
    
def critical(text:str,*args,parent:str|None=None):
    """
    Log with level of CRITICAL
    
    Arguments:
        text:
            Text to log
        args:
            Can be used as args for string formatted (just as logging)
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    if FIND_PARENTS and parent is None:
        parent = resolve_caller(inspect.stack()[1])
        
    write_log(text % args,"CRITICAL",parent)