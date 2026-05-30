from . import llm
from .llm import ai_tools
from .stt import realtimestt as stt
from . import tts
import threading
from argparse import ArgumentParser
import logging
import os

def queue_checker(queue:tts.Queue):
    
    while True:
        
        queue.check_generate()
        queue.check_play()

def get_real(text:str):
    
    print("[You] "+text,end="\r")

def main(model,tools):
    
    # Yeah, that's right
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(logging.NullHandler())
    
    # Generate
    bot = llm.ChatBot(model)
    if tools:
        ai_tools.add_all_tools(bot)
    recorder = stt.generate_recorder(realtime_func=get_real)
    queue = tts.Queue()
    
    # Thread
    threading.Thread(target=queue_checker,args=(queue,),daemon=True).start()
    
    # Clear console
    print("\x1b[2J\x1b[H",end="")
    
    while True:
        
        print("[You] ",end="\r")
        
        text = recorder.text()
        
        print("[You] "+text)
        
        if "bye" in text.lower():
            
            os._exit(0)
            
        output = bot.chat(text)
        
        print("[Assistant] " + output)
        
        queue.generate(output)
        
if __name__ == "__main__":
    
    # Parser
    parser = ArgumentParser("Gregium - AI",description="A complete combination of all 3 Main Gregium AI functions")
    parser.add_argument("--model","-m",type=str,default="granite3.3",help="The Ollama model to use (to install new ones use 'ollama pull {model name}')")
    parser.add_argument("--tools","-t",type=bool,default=False,help="Allows the AI to use additional tools (see `ai_tools` for full function list)")
    args = parser.parse_args()
    
    main(model=args.model,tools=args.tools)