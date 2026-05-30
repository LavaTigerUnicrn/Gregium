"""
A list of working tools for the AI to use

These allow things like getting information online, time, etc.
"""
import requests
import urllib.parse as parse
import json
from bs4 import BeautifulSoup
import time
from . import ChatBot
from ...settings import CUSTOM_SEARCH_API_KEY,CUSTOM_SEARCH_ENGINE_ID

API_KEY = CUSTOM_SEARCH_API_KEY
ENGINE_ID = CUSTOM_SEARCH_ENGINE_ID

def google_search(search:str):
    """
    Search up something on google and return the search as a json
    
    In the case where an error is returned it is likely the daily limit has been reached
    
    Args:
        search: The prompt to search on google
    
    Returns:
        str: The html content of the google page
    """
    
    # Notify search has happened
    print(f"Bot has searched for '{search}'")
    
    # Get formatted objects
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

def search_link(link:str) -> str:
    """
    This will search for a given link and return all the text content on that page
    
    Some pages may not allow the page to be read and will not return any useful information
    
    Args:
        link: The link to search for
        
    Returns:
        str: The found text on the page
    """
    
    # Get the page at a soup object
    soup = BeautifulSoup(requests.get(link).content.decode("utf-8"),"html.parser")

    # Get rid of script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Get all text on the page
    text = soup.get_text(separator="\n")

    # Clean up extra whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Return finished
    return "\n".join(lines)

def search_wikipedia(article:str):
    """
    This will search wikipedia for the closest relating article it can find
    
    Use for getting any general information on a topic
    
    Args:
        article: The article to search for
        
    Returns:
        str: The found text on the page
    """
    
    # Format link
    link = "https://en.wikipedia.org/w/index.php?search="+parse.quote(article)
    
    # Get the page at a soup object
    soup = BeautifulSoup(requests.get(link,headers={"User-Agent":"GregiumOllamaBot/0.0 (https://pypi.org/project/gregium/) gregium/0.0"}).content.decode("utf-8"),"html.parser")

    # Get rid of script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Get all text on the page
    text = soup.get_text(separator="\n")

    # Clean up extra whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Return finished
    return "\n".join(lines)

def get_time() -> str:
    """
    Gets the current time in 24 hour time
    
    Returns:
        str: The current time
    """
    
    return str(time.ctime(time.time()))

# List of tools
tools = [get_time,search_wikipedia,search_link,google_search]

def add_all_tools(bot:ChatBot):
    """
    Automatically adds all tools to the ChatBot
    
    Arguments:
        bot:
            The bot to add to
    """
    
    # Add all tool functions
    for tool in tools:
        bot.add_tool(tool)