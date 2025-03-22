def init():
    """
    Preloads all gregium modules
    """
    from . import env
    from . import commandSystem
    from . import gambleCore
    from . import camera
    from . import buttons
    from . import terminalLogging

    __all__ = [env, commandSystem, gambleCore, camera, buttons, terminalLogging]

    return __all__


VERSION = {"major": 0, "minor": 1, "patch": 10}
