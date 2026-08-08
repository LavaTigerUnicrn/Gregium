"""
A list of working tools for the AI to use

These allow things like getting information online, time, etc.
"""
import json
import time
from urllib import parse

import requests

API_KEY:str = ""
ENGINE_ID:str = ""

def update_keys(api_key:str,engine_id:str):
    """
    Updates the API keys for google "custom search"
    
    Go To: https://console.cloud.google.com/apis/api/customsearch.googleapis.com and https://developers.google.com/custom-search/v1/overview for a detailed overview
    """
    
    global API_KEY,ENGINE_ID
    
    API_KEY = api_key
    ENGINE_ID = engine_id

def google_search(search:str):
    """
    Search up something on google and return the search as a json
    
    In the case where an error is returned it is likely the daily limit has been reached
    
    **MAKE SURE THAT YOU RUN `update_keys()` TO SET THE API KEYS**
    
    Args:
        search: The prompt to search on google
    
    Returns:
        str: The html content of the google page
    """
    
    # Notify search has happened
    print(f"Bot has searched for '{search}'")
    
    # Get formatted objects
    if API_KEY == "" or ENGINE_ID == "":
        
        raise ValueError("Either the API_KEY or ENGINE_ID have not been set, use `update_keys()` to set the keys")
    
    formatted_key = parse.quote(API_KEY)
    formatted_request = parse.quote(search)
    formatted_engine_id = parse.quote(ENGINE_ID)
    
    # Search
    read = json.loads(requests.get(f"https://www.googleapis.com/customsearch/v1?q={formatted_request}&num=10&start=0&cx={formatted_engine_id}&key={formatted_key}").content.decode('utf-8'))
    
    # Format nicely
    out = "Here is a list of results\n"
    for item in read["items"]:
        out += item["title"] + "\n" + item["link"] + "\n" + item["snippet"] + "\n\n"
    
    # Return search formatted output
    return out

def get_time() -> str:
    """
    Gets the current time in 24 hour time
    
    Returns:
        str: The current time
    """
    
    return time.ctime()