"""
Standardized settings of gregium
"""
from .settings_helper import settings_loader
from .settings_helper.settings_loader import Language,TTS_Voice
import os
from .logger.basic_logs import *
from dotenv import load_dotenv
load_dotenv()

required_env = ["GOOGLE_API_TOKEN","GOOGLE_SEARCH_ENGINE_TOKEN","HF_TOKEN"]

for token in required_env:
    if token not in os.environ:
        warn(f"{token} not found in .env",__name__)
        os.environ["GOOGLE_API_TOKEN"] = ""
    
### SETTINGS
# Load and fix settings
settings_loader.load_settings()

## STT
LANGUAGE:Language = settings_loader.LOADED_SETTINGS["stt"]["lang"] # Language to use for STT

## TTS
TTS_VOICE:TTS_Voice = settings_loader.LOADED_SETTINGS["tts"]["tts_voice"] # Default TTS Voice to use
# Go To: https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462 for a list of voices

## AI
DEFAULT_MODEL:str = settings_loader.LOADED_SETTINGS["ai"]["default_model"]

## AI Tools
CUSTOM_SEARCH_API_KEY:str = os.environ["GOOGLE_API_TOKEN"] # The API key to use for google searches
CUSTOM_SEARCH_ENGINE_ID:str = os.environ["GOOGLE_SEARCH_ENGINE_TOKEN"] # The engine to use for google searches
# Go To: https://console.cloud.google.com/apis/api/customsearch.googleapis.com and https://developers.google.com/custom-search/v1/overview for a detailed overview

## Huggingface AI
HUGGINGFACE_API_KEY:str = os.environ["HF_TOKEN"]

## Terminal
DEFAULT_TERMINAL_CHOICE_HELP:bool = settings_loader.LOADED_SETTINGS["terminal"]["help_enabled"] # If the custom terminal choice should give the help text
TERMINAL_CAROUSEL:int = settings_loader.LOADED_SETTINGS["terminal"]["carousel_length"]