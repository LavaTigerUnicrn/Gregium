"""
Lets you change the settings of Gregium easily
"""
from ..terminal import inputs as inp
from ..terminal import keycodes
from . import settings_loader as loader
import ollama

def confirm() -> bool:
    """
    Quick confirmation
    """
    
    inp.print("Are you sure?")
    
    return inp.choice([True,False],["Yes","No"])

def main():
    
    # Settings path
    section = ""
    
    # Read settings file
    types = loader.get_settings_types()
    
    # Load TTS voices
    tts_voices = loader.list_voices_dict()
    
    # Traverse settings
    while True:
        
        # Clear terminal
        inp.clear()
        
        if section:
            
            # Print setup
            inp.print("Choose setting")
            
            # Get possible sections
            setting_section = loader.LOADED_SETTINGS[section]
            settings = list(setting_section.keys())
            
            # Merge value
            chosen = inp.choice(["\u9991",]+settings,["Back",]+[x + " = " + str(setting_section[x]) for x in settings])
            
            # TODO: Add additional options like save, repair, reset
            
            # Action
            match chosen:
                
                case "\u9991":
                    
                    # Return
                    section = ""
                    
                case _:
                    
                    # Change setting
                    # Get path of setting
                    setting_path = section+"."+chosen
                    
                    setting_type = types[setting_path]
                    
                    # Special type actions
                    match setting_type:
                        
                        case "llama_model":
                            
                            # Choose Ollama model
                            inp.print("Choose model")
                            
                            chosen_model = inp.choice([x["model"] for x in ollama.list()["models"]])
                            
                            setting_section[chosen] = chosen_model
                            
                        case "boolean":
                            
                            # Choose boolean
                            inp.print("Choose value for {chosen}")
                            
                            chosen_value = inp.choice([True, False])
                            
                            setting_section[chosen] = chosen_value
                            
                        case "tts_voice":
                            
                            # Choose tts voice
                            lang = inp.input("Enter voice language code (such as en)")
                            
                            lang_keys = list(tts_voices.keys())
                            
                            # Edge case
                            if lang not in lang_keys:
                                
                                possible_choices = list(filter(lambda x: x[0] == lang[0],lang_keys))
                                
                                if len(possible_choices) == 0:
                                    
                                    inp.print("Language not recognized")
                                
                                    inp.getch()
                                
                                    continue
                                
                                inp.print("Language not recognized did you mean")
                            
                                lang = inp.choice(possible_choices)
                            
                            # Choose voice
                            inp.print("Choose voice")
                            
                            voice = inp.choice(tts_voices[lang])
                            
                            # Update voice
                            setting_section[chosen] = lang+"-"+voice
                        
                        case _:
                            
                            # Generic value setting
                            setting_section[chosen] = inp.input(f"Enter value for {chosen}?")
            
        else:
            
            # Print setup
            inp.print("Choose section")
            
            # Get possible sections
            possible_sections = list(loader.LOADED_SETTINGS.keys())
            possible_sections.remove("$schema")
            
            # Choose section
            chosen = inp.choice(["Exit","Save","Revert","Reset","Repair",""]+possible_sections)
            
            match chosen:
                case "Exit":
                    
                    quit()
                    
                case "Save":
                    
                    if confirm():
                        
                        loader.save_settings()
                    
                case "Revert":
                    
                    if confirm():
                        
                        loader.load_settings()

                case "Reset":
                    
                    if confirm():
                        
                        loader.reset_settings()
                    
                case "Repair":
                    
                    if confirm():
                        
                        loader.fix_settings()
                    
                case _:
                    
                    section = chosen