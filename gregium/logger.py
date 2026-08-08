import logging
import sys


class StdoutFormatter(logging.Formatter):
    """
    Custom formatter for adding colors to stdout
    """
    
    level_colors:dict[int,str] = {logging.DEBUG:"\x1b[38;5;245m",logging.INFO:"\x1b[38;5;10m",logging.WARNING:"\x1b[38;5;11m",logging.ERROR:"\x1b[38;5;196m",logging.CRITICAL:"\x1b[38;5;129m"}
    
    level_formatters:dict[int,logging.Formatter] = {}
    
    default_formatter = logging.Formatter(fmt="\x1b[38;5;20m[%(asctime)s]\x1b[0m [%(name)s/%(levelname)s] %(message)s",datefmt="%H:%M:%S")
    
    for level,color in level_colors.items():
        
        level_formatters[level] = logging.Formatter(fmt=f"\x1b[38;5;20m[%(asctime)s]\x1b[0m [%(name)s/{color}%(levelname)s\x1b[0m] %(message)s",datefmt="%H:%M:%S")
    
    def format(self,record:logging.LogRecord):
        
        if record.levelno in self.level_formatters:
        
            return self.level_formatters[record.levelno].format(record)
        
        else:
            
            return self.default_formatter.format(record)

def style(filename:str|None=None,mode:str="w",stdout:bool=False,level:int=logging.WARNING):
    """
    Enables gregium-style logging formatting
    
    You can use any combination of settings
    
    Arguments:
        filename:
            The path to log to
        mode:
            The mode the path should log in (generally should be w to clear log but can also be a to add to the end of the file)
        stdout:
            To log to standard output (terminal)
        level:
            The minimum logging level to log (using setLevel)
    """
    
    handlers = []
    
    # Make stdout handler
    if stdout:
        
        stdout_handler = logging.StreamHandler(sys.stdout)
        
        stdoutFormatter = GeneratedStdoutFormatter

        stdout_handler.setFormatter(stdoutFormatter)
        
        stdout_handler.setLevel(level)
                
        handlers.append(stdout_handler)
    
    # Make file handler
    if filename is not None:
        
        file_handler = logging.FileHandler(filename=filename,mode=mode)
        
        file_handler.setFormatter(logging.Formatter(fmt="[%(asctime)s] [%(name)s/%(levelname)s] %(message)s",datefmt="%H:%M:%S"))
        
        file_handler.setLevel(level)
        
        handlers.append(file_handler)

    # Set settings and handlers
    logging.basicConfig(format="[%(asctime)s] [%(name)s/%(levelname)s] %(message)s",datefmt="%H:%M:%S",handlers=[stdout_handler,file_handler],level=level)

def addLevel(level:int,levelName:str,levelColor:tuple[int,int,int]=(255,255,255)):
    """
    Associate 'levelName' with 'level'.

    This is used when converting levels to text during message formatting.
    
    Also adds a color when printing to standard output (terminal)
    """
    
    # Add name
    logging.addLevelName(level,levelName)
    
    # Make color
    r,g,b = levelColor
    
    color_code = f"\x1b[38;2;{r};{g};{b}m"
    
    # Add color value
    GeneratedStdoutFormatter.level_colors[level] = color_code
    
    # Add color formatter
    GeneratedStdoutFormatter.level_formatters[level] = logging.Formatter(fmt=f"\x1b[38;5;20m[%(asctime)s]\x1b[0m [%(name)s/{color_code}%(levelname)s\x1b[0m] %(message)s",datefmt="%H:%M:%S")

# Make stdout formatter
GeneratedStdoutFormatter = StdoutFormatter()