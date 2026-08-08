import inspect
from collections.abc import Callable


def func_from_annotation(function:Callable) -> dict:
    """
    Generates a func dict from a function
    
    The function MUST NOT have any ** or * args
    
    See `add_numbers` function for example
    
    Arguments:  
        function: The function to annotate
    """
    
    # Get values
    signature = inspect.signature(function)
    if function.__doc__ is None:
        raise ValueError("No docstring was created for function")
    doc:str = function.__doc__
    name:str = function.__name__
    
    # Split doc by section
    split_doc = [x.strip().lower() for x in doc.splitlines()]
    arg_index = split_doc.index("args:")
    rtrn_index = split_doc.index("returns:")
    
    # Get parameter descriptions
    param_desc_str = split_doc[arg_index+1:rtrn_index]
    param_desc = {}
    
    for param in param_desc_str:
        
        param_name = param.split(" ")[0]
        param_description = param.split(":")[1].strip()
        
        param_desc[param_name] = param_description
    
    # Format parameters
    parameters = signature.parameters
    required_parameters = list(filter(lambda x:parameters[x].default is inspect._empty,parameters.keys()))
    formatted_parameters = {}
    type_keys = {list:"array", bool:"boolean", int:"integer", None:"null", float:"number", dict:"object", str:"string"}
    for parameter,param_val in parameters.items():
        formatted_parameters[parameter] = {"type":type_keys[param_val.annotation],"description":param_desc[parameter]}
    
    final_format = {"type":"function","function":{"name":name,"description":"\n".join(split_doc[:arg_index] + split_doc[rtrn_index:]),"parameters":{"type":"object","properties":formatted_parameters},"required_parameters":required_parameters}}
    
    return final_format


### Example Function
def add_numbers(a:int, b:int=3) -> int:
    """
    Adds two numbers together
    
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        str: The sum of the numbers
    """
    
    return a + b