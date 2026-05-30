"""
The basic types of logs

It is recommended to use "from basic_logs import *" 
in order to use the log levels most easily
"""

from ..logger import write_log

def info(text:str,parent:str|None=None):
    """
    Log with level of INFO
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    write_log(text,"INFO",parent)
    
def warn(text:str,parent:str|None=None):
    """
    Log with level of WARN
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    write_log(text,"WARN",parent)
    
def warning(text:str,parent:str|None=None):
    """
    Log with level of WARN
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    write_log(text,"WARN",parent)
    
def error(text:str,parent:str|None=None):
    """
    Log with level of ERROR
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    write_log(text,"ERROR",parent)
    
def exception(text:str,parent:str|None=None):
    """
    Log with level of ERROR
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    write_log(text,"ERROR",parent)
    
def debug(text:str,parent:str|None=None):
    """
    Log with level of DEBUG
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    write_log(text,"DEBUG",parent)
    
def critical(text:str,parent:str|None=None):
    """
    Log with level of CRITICAL
    
    Arguments:
        text:
            Text to log
        parent:
            Optional parent to log (will appear like log level)
            
            *It's best to use __name__ in this argument
    """
    
    write_log(text,"CRITICAL",parent)