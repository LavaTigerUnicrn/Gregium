"""
Live logging to file or stdout with timestamps 
"""

from typing import Literal
from io import TextIOWrapper
import sys
import time

OPEN_LOGGER:TextIOWrapper = open("log.log","w",encoding="utf-8") # TextIOWrapper to write logs to (can be file or stdout)
IS_STDOUT:bool = False # Toggle for ANSI color sequences (sequences are only used in stdout)
PATH:str = "log.txt" # The most recent path that has been set
    
def designate_file(path:str):
    """
    Reassigns the file to log to
    
    Arguments:
        path:
            The path to set the logger to
    """
    
    global OPEN_LOGGER,IS_STDOUT,PATH
    
    # Set path
    PATH = path
    
    # Open new path for writing
    OPEN_LOGGER = open(path,"w",encoding="utf-8")
    IS_STDOUT = False
    
def set_stdout():
    """
    Replaces the current logging file with the standard output
    """
    global OPEN_LOGGER,IS_STDOUT
    
    # Set logger to current standard output
    OPEN_LOGGER = sys.stdout
    IS_STDOUT = True

def clear():
    """
    Empties the current logging file or clears stdout
    """
    global OPEN_LOGGER
    
    # Use STDOUT clear code
    if IS_STDOUT:
        
        OPEN_LOGGER.write("\x1b[2J\x1b[H")

        # Flush log
        OPEN_LOGGER.flush()
        
        return
    
    OPEN_LOGGER = open(PATH,"w")
    OPEN_LOGGER.flush()
    
# Levels of writes to log
level = Literal["INFO","ERROR","WARN","DEBUG","CRITICAL"]

# Colors for each log level
level_colors = {"INFO":"\x1b[0m","ERROR":"\x1b[31m","WARN":"\x1b[33m","DEBUG":"\x1b[34m","CRITICAL":"\x1b[35m"}

def write_log(text:str,log_level:level="INFO",parent:str|None=None):
    """
    Writes to log and immediately flushes the log
    
    If the current open logger is stdout it will also
    add ANSI color sequences to the output
    
    Arguments:
        text:
            Text to log
        log_level:
            The level of the log to be (INFO, ERROR, or WARN ar recommended)
        parent:
            Optional parent filename to log (will appear like log level)
            *It's best to use __name__ in this argument
    """   
    
    # Find current timestamp
    timestamp:time.struct_time = time.localtime(time.time())
    timestamp_formatted:str = f"{timestamp.tm_hour:0>2}:{timestamp.tm_min:0>2}:{timestamp.tm_sec:0>2}"
    
    # Format parent if it exists
    if parent is not None:
        
        parent_formatted = f"{parent}/"
        
    else:
        
        parent_formatted = ""
        
    
    # Check if log level is a valid level
    if log_level not in level_colors:
        
        raise ValueError(f"Invalid logging level: {log_level}")
    
    # Add coloring to text if currently in stdout
    if IS_STDOUT:
        
        # Write to log
        OPEN_LOGGER.write(f"{level_colors[log_level]}[{timestamp_formatted}] [{parent_formatted}{log_level}] {text}\n\x1b[0m")
        
        # Flush log
        OPEN_LOGGER.flush()
        
        # End function
        return
    
    # Write to log
    OPEN_LOGGER.write(f"[{timestamp_formatted}] [{parent_formatted}{log_level}] {text}\n")
    
    # Flush log
    OPEN_LOGGER.flush()