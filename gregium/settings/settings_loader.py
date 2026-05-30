"""
Tools for settings
"""
from typing import Literal
import json
from pathlib import Path

Language = str

TTS_Voice = str

class RGB:
    """
    A value of color in (R,G,B) format (int,int,int)
    """
    pass   

LOADED_SETTINGS:dict|None = None

def load_settings():
    """
    Loads all settings and stores in loaded_settings
    """
    
    global LOADED_SETTINGS
    
    # Get path
    path = str(Path(__file__).parent.absolute()) + "/settings.json"
    
    # Load settings to JSON
    try:
        with open(path,"r") as r:
        
            LOADED_SETTINGS = json.load(r)
    except FileNotFoundError:
        with open(path,"w") as w:
            
            w.write("{\"$schema\":\"./settings-schema.json\"}")
            
        LOADED_SETTINGS = {}

    # Make sure settings are stable    
    fix_settings()
        
def save_settings():
    """
    Saves all settings stored in loaded_settings
    """
    
    global LOADED_SETTINGS
    
    # Get path
    path = str(Path(__file__).parent.absolute()) + "/settings.json"
    
    # Load settings to JSON
    with open(path,"w") as w:
        
        json.dump(LOADED_SETTINGS,w,indent=4)
        
def fix_settings():
    """
    Fills in all unknown values to JSON based on schema
    """
    
    global LOADED_SETTINGS
    
    # Load settings if missing
    if LOADED_SETTINGS is None:
        
        load_settings()
        
    assembled_keys = get_settings_schema()
    
    # Scan the created json
    for key in assembled_keys:
        
        # Get value
        default = assembled_keys[key]
        
        # Check if key exists
        try:
            
            read_dict_from_path(LOADED_SETTINGS,key)
            
        except:
            
            # If it doesn't, set value
            key_parent = ".".join(key.split(".")[:-1])
            key_root = key.split(".")[-1]
            
            read_dict_from_path(LOADED_SETTINGS,key_parent)[key_root] = default
            
def reset_settings():
    """
    Resets all values to JSON based on schema
    """
    
    global LOADED_SETTINGS
    
    # Load settings if missing
    if LOADED_SETTINGS is None:
        
        load_settings()
        
    assembled_keys = get_settings_schema()
    
    # Scan the created json
    for key in assembled_keys:
        
        # Get value
        default = assembled_keys[key]
            
        # Cancel for blank
        if key == "":
            
            continue
        
        # Set value
        key_parent = ".".join(key.split(".")[:-1])
        key_root = key.split(".")[-1]
        
        read_dict_from_path(LOADED_SETTINGS,key_parent)[key_root] = default
            
def get_settings_schema():
    """
    Gets all the key paths and default values of every setting
    """
    
    # Get path
    path = str(Path(__file__).parent.absolute()) + "/settings-schema.json"
    
    # Load settings to JSON
    with open(path,"r") as r:
        
        settings_default:dict = json.load(r)
        
    # Recurse scan for default values
    read_keys = ["",]
    assembled_keys = {}
    
    # Read and assemble defaults
    while len(read_keys) > 0:
        
        # Get next key
        key = read_keys[-1]
        value = read_dict_from_path(settings_default,key)
        read_keys.pop()
        
        # Only continue if key is correct
        if type(value) is not dict:
            continue
        
        # Get type
        key_type = value["type"]
        
        if key_type == "object":
            
            # Get properties
            new_keys = [(key+".properties."+x).lstrip(".") for x in value["properties"].keys()]
            read_keys = read_keys + new_keys
            
            # Add to key assembly
            assembled_keys[key.replace("properties.","")] = {}

        else:
            
            # Add to key assembly
            assembled_keys[key.replace("properties.","")] = value["default"]
            
    return assembled_keys

def get_settings_types():
    """
    Gets all the key paths and types of every setting
    """
    
    # Get path
    path = str(Path(__file__).parent.absolute()) + "/settings-schema.json"
    
    # Load settings to JSON
    with open(path,"r") as r:
        
        settings_default:dict = json.load(r)
        
    # Recurse scan for default values
    read_keys = ["",]
    assembled_keys = {}
    
    # Read and assemble defaults
    while len(read_keys) > 0:
        
        # Get next key
        key = read_keys[-1]
        value = read_dict_from_path(settings_default,key)
        read_keys.pop()
        
        # Only continue if key is correct
        if type(value) is not dict:
            continue
        
        # Get type
        key_type = value["type"]
        
        if key_type == "object":
            
            # Get properties
            new_keys = [(key+".properties."+x).lstrip(".") for x in value["properties"].keys()]
            read_keys = read_keys + new_keys
            
            # Add to key assembly
            assembled_keys[key.replace("properties.","")] = {}

        else:
            
            # Add to key assembly (use add_type if present)
            if "add_type" in value:
                assembled_keys[key.replace("properties.","")] = value["add_type"]
            else:
                assembled_keys[key.replace("properties.","")] = value["type"]
            
    return assembled_keys     
            
def read_dict_from_path(read:dict,path:str):
    """
    Reads a place in a dictionary from a path
    
    Arguments:
        read: The dictionary to be read
        path: The path to read (format of foo.baz.bar)
    """
    
    # Edge case of blank path
    if path == "":
        return read
    
    # Split path by dots
    path:list = path.split(".")
        
    # Go through path
    while len(path) > 0:
        section = path[0]
        path = path[1:]
        read = read[section]
        
    return read

def list_voices_dict() -> dict:
    """
    Lists out every voice in dictionary form
    """
    
    # Get path
    path = str(Path(__file__).parent.absolute()) + "/tts_voices.txt"
    
    # Load voices
    with open(path,"r") as r:
        
        voices:list[str] = r.read().split("\n")
        
    # Combine voice into dict
    voice_dict:dict[str,list] = {}
    for voice in voices:
        
        # Add each voice
        split_voice = voice.split("-")
        voice_name = split_voice[0]
        
        if voice_name not in voice_dict:
            
            voice_dict[voice_name] = []
            
        voice_dict[voice_name].append(voice.replace(voice_name+"-",""))
        
    return voice_dict