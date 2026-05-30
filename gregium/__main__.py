import argparse
from .library_checker import verify_lib

class FakeArgParser():
    
    def __init__(self,**kwargs):
        """
        An argument parser that emulates the Argparse arguments
        """
        
        # Assign values
        for arg in kwargs:
            arg_value = kwargs[arg]
            
            setattr(self,arg,arg_value)
        

if __name__ == "__main__":
    
    # Make parser
    parser = argparse.ArgumentParser(prog="Gregium",description="An example of Gregium functions")
    
    # Add verify argument
    parser.add_argument("--verify",action="store_true",help="Makes Gregium verify all libraries before running")
    parser.add_argument("--settings",action="store_true",help="Runs settings changer on Gregium")
    
    # Parse
    args = parser.parse_args()
    
    # Verify libraries
    if args.verify:
        
        verify_lib()
        print("All modules verified")
        quit()
    
    # Import
    from .terminal import inputs as inp
    from .terminal import keycodes
    import ollama
    
    if args.settings:
        
        # Start settings
        inp.start()
        inp.clear()
        from .settings import settings_editor as settings_main
        settings_main.main()
    
    # Start inputs
    inp.start()

    # Clear console
    inp.clear()

    # Welcome users and give choice of what to do
    inp.print("Welcome to gregium!\n")
    chosen = inp.choice(["LLM Testing","TTS Testing","RVC TTS Testing","STT Testing","Combined Testing","Settings","Exit"],optionsDesc=["An interactive LLM using Ollama","Testing the Edge-TTS Text-To-Speech","Testing the RVC Text-To-Speech","Testing Speech-to-Text","Combines STT, TTS, and LLM together into one","Change settings","Quit the program"])

    # Action based on choice
    match chosen:
        case "LLM Testing":
            
            # Settings for LLM
            inp.print("\nModel")
            model = inp.choice([x["model"] for x in ollama.list()["models"]])
            inp.print("\nUse additional tools?")
            tools = inp.choice([True,False],["Yes","No"])
            
            # Stop custom inputs
            inp.print("Please wait...\n")
            inp.end()
            
            # Set parser arguments
            fake_parser = FakeArgParser(tools=tools,model=model)
            
            # Start LLM
            from .ai.llm import __main__ as llm_main
            llm_main.main(fake_parser)
            
        case "TTS Testing":
            
            # Stop custom inputs
            inp.print("Please wait...\n")
            inp.end()
            
            # Start TTS
            from .ai.tts import __main__ as tts_main
            tts_main.main()
            
        case "RVC TTS Testing":
            
            # Import model lister
            inp.print("Please wait...\n")
            from .ai.tts import list_models
            
            # Get user to choose model
            inp.print("Choose a model")
            
            model = inp.choice(list_models())
            
            # Stop custom inputs
            inp.print("Please wait...\n")
            inp.end()
            
            # Start TTS
            from .ai.tts import __main__ as tts_main
            tts_main.main_rvc(model)
            
        case "STT Testing":
            
            # Stop custom inputs
            inp.print("Please wait...\n")
            inp.end()
            
            # Start STT
            from .ai.stt import __main__ as stt_main
            stt_main.main()
            
        case "Combined Testing":
            
            # Settings for LLM
            inp.print("\nModel")
            model = inp.choice([x["model"] for x in ollama.list()["models"]])
            inp.print("\nUse additional tools?")
            tools = inp.choice([True,False],["Yes","No"])
            
            # Stop custom inputs
            inp.print("Please wait...\n")
            inp.end()
            
            # Start AI
            from .ai import __main__ as ai_main
            ai_main.main(model,tools)
            
        case "Settings":
            
            # Start settings
            from .settings import settings_editor as settings_main
            settings_main.main()
        
        case "Exit":
            
            # Quit immediately
            inp.end()
            quit()

    # End program
    inp.end()