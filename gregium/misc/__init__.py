import os
from typing import Literal
import importlib.util as import_util
import time
from io import BytesIO
import requests
from typing import get_args
from types import UnionType
import inspect

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

def load_audio(url:str) -> BytesIO:
    """
    Loads a audio file from the web and returns bytes
    
    (This can be directly used in `pygame.mixer.music` and `pygame.mixer.Sound`)
    
    Arguments:
        url:
            The exact url to the downloadable file
    """
    
    response = requests.get(url)
    bytes = BytesIO(response.content)
    
    return bytes

class ColInterp:
    
    def __init__(self,col1,col2,delta,steps,exact):
        
        # Store values
        self.col1 = col1
        self.col2 = col2
        self.delta = delta
        self.steps = steps
        self.exact = exact
        
    def __next__(self):
        
        # Move to next index
        self.i += 1
        
        # Stop on no more colors left
        if self.i >= self.steps:
            raise StopIteration()
        
        # Use end color on second to last item
        if self.i == self.steps-1:
            return self.col2
        
        # Otherwise get the current based on delta
        r,g,b = (self.col1[0] + self.delta[0] * self.i,self.col1[1] + self.delta[1] * self.i,self.col1[2] + self.delta[2] * self.i)
        
        # Return float version if exact, otherwise round to integers
        if self.exact:
        
            return (r,g,b)
            
        else:
            
            return (int(r),int(g),int(b))
        
    def __str__(self):
        
        return f"Color Interpolator {self.col1} => {self.col2}"
    
    def __len__(self):
        
        return self.steps

class _ColInterpGenerator():

    def __init__(self,col1,col2,delta,steps,exact):
        
        # Store values
        self.col1 = col1
        self.col2 = col2
        self.delta = delta
        self.steps = steps
        self.exact = exact
        
    def __iter__(self):
        
        # Generate iterator
        generated = ColInterp(self.col1,self.col2,self.delta,self.steps,self.exact)
        generated.i = -1
        
        return generated
    
def interp(color1:tuple[int,int,int],color2:tuple[int,int,int],steps:int,exact:bool=False):
    """
    Generates an interpolator to nicely move between two edge colors
    
    The output is an iterator of colors in which the first is the color1 and the last is the color2, with each next being a step towards the end
    
    ```for color in interp(red,green,10):...
    ```
    
    Arguments:
        color1:
            The starting color
        color2:
            The ending color
        steps:
            The number of steps it should take
        exact:
            If the output rgb values should be in exact floats instead of being rounded to integers
    """
    
    # Get the change in each color in each step
    delta = ((color2[0]-color1[0])/(steps-1),(color2[1]-color1[1])/(steps-1),(color2[2]-color1[2])/(steps-1))
    
    return _ColInterpGenerator(color1,color2,delta,steps,exact)

def static_function(func):
    """
    A decorator that ensure each input and output is the same as the annotations
    
    This will only check with a depth of 1, so things like `list[str]` will only check the list
    
    Unions may be used such as `str|int` in which it will check if any of the types are satisfied
    """

    # Get method annotations
    sig = inspect.signature(func)
    fixed_anot = {}
    
    # Get each parameter
    params = sig.parameters
    for name in params:
        
        # Get annotation (types) of parameters
        value = params[name].annotation

        # Break unions and save all types
        if isinstance(value,UnionType):
            value_fixed = get_args(value)
        else:
            value_fixed = (value,)
        
        fixed_anot[name] = value_fixed
    
    # Get annotation of return
    rtrn_anot = sig.return_annotation
    
    # Break unions and save all types
    if isinstance(rtrn_anot,UnionType):
            value_fixed = get_args(rtrn_anot)
    else:
        value_fixed = (rtrn_anot,)
        
    fixed_anot["return"] = value_fixed
    
    # Generated function that checks types
    def inner(*args,**kwargs):
        
        # Get all keys
        places = list(fixed_anot.keys())
        
        # Check each argument
        for i in range(len(args)):
            
            # Get types and name of given argument
            arg = args[i]
            gotten_n = places[i]
            gotten = fixed_anot[gotten_n]

            # Skip if no parameters
            found = gotten[0] is inspect._empty
            
            # Check if arguments are of the right type
            for got in gotten:
                
                if isinstance(arg,got):
                    
                    found = True
                    
            if not found:
                
                # Raise error for bad types
                raise TypeError(f"Expected type of '{gotten}' for argument '{gotten_n}' but found {type(arg)} instead")
        
        # Check keyword arguments
        for kwarg in kwargs:
            
            # Get types of given argument
            gotten = fixed_anot[kwarg]
            value = kwargs[kwarg]
            
            # Skip if no parameters
            found = gotten[0] is inspect._empty
            
            # Check if arguments are of the right type
            for got in gotten:
                
                if isinstance(value,got):
                    
                    found = True
                    
            if not found:
                
                # Raise error for bad types
                raise TypeError(f"Expected type of '{gotten}' for keyword argument '{kwarg}' but found {type(value)} instead")
        
        # Get output of the function
        output = func(*args,**kwargs)
        
        # Get types for return
        gotten = fixed_anot["return"]
        
        # Skip if no parameters
        found = gotten[0] is inspect._empty
        
        # Check if return is of the right type
        for got in gotten:
            
            if isinstance(output,got):
                
                found = True
                
        if not found:
            
            # Raise error for bad types
            raise TypeError(f"Expected function to output type '{gotten}' but found {type(value)} instead")

        # Finish
        return output
    
    # Return back decorated function
    return inner