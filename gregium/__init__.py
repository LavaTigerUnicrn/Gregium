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
    from . import imports
    from . import easing

    __all__ = [
        env,
        commandSystem,
        gambleCore,
        camera,
        buttons,
        terminalLogging,
        imports,
        easing,
    ]

    return __all__


VERSION = {"major": 0, "minor": 1, "patch": 11}
