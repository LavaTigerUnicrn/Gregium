from . import settings_editor as editor
from ..terminal import inputs as inputs

if __name__ == "__main__":
    
    # Start input
    inputs.start()
    
    # Run editor
    editor.main()