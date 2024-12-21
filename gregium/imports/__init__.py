import importlib, os, sys


def import_from_file(filepath: str, cache_imports: bool = True, use_cached:bool = True, overwrite_name:str = ""):
    """
    Imports a module by filename and returns the module instance
    
    Args:
        filepath:
            The path the module is located in (include .py extension)
        cache_imports:
            Enables imported modules to be cached to sys.modules under filename with .py removed or overwrite_name if applicable
        use_cached:
            Enables the script to use already imported modules under sys.modules
        overwrite_name:
            Replaces the name of the module in sys.modules to equal the overwrite_name value instead of filename with .py removed
    """
    name = os.path.basename(filepath).replace(".py", "") if overwrite_name == "" else overwrite_name
    if use_cached and name in sys.modules:
        return __import__(name)
    spec = importlib.util.spec_from_file_location(f"{name}", f"{filepath}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if cache_imports:
        sys.modules[name] = module
    return module