from argparse import ArgumentParser
from . import Ollama_ChatBot
from . import ai_tools

def help_text():
    print(f"\x1b[H\x1b[2J\nOllama LLM ({ARGS_GLOB.model})\nTools: {'enabled' if ARGS_GLOB.tools else 'disabled'}")
    print("\nThis can be used like a normal terminal chatbot")
    print("\n\n--Command Functions--")
    print("Some special command strings will result in debug settings, they must start with a '\\'\n")
    print("\\role {role name} Changes the role of the user of either 'u' for user or 's' for system")
    print("\\tell Changes the mode to tell (this won't result in a response)")
    print("\\chat Changes the mode to chat (this will result in a response)")
    print("\\reset Wipes all the memory of the model")
    print("\\cls Clears the terminal")
    print("\\exit Quits\n")

def main(args):
    global ARGS_GLOB,ROLE,CHAT
    
    ARGS_GLOB = args

    # Get ready
    print("Starting Up...")
    bot = Ollama_ChatBot(args.model)

    ROLE = "user"
    CHAT = True

    if args.tools:
        ai_tools.add_all_tools(bot)

    # Print help message
    help_text()

    def min_arguments(args,content):
        """
        Sets the minimum arguments for a given command
        
        Arguments:  
            args:
                The minimum argument counts
            content:
                The given content of the arguments
        """
        
        # Check for content and return accordingly
        if len(content) < args:
            print("[command] Too few arguments supplied")
            return False
        return True

    # Decode role letters to role
    roleCodes = {"u":"user","s":"system"}

    def interpret_special(prompt:str):
        """
        Interprets special prompts
        
        Arguments:
            prompt:
                The starting prompt
        """
        global ROLE,CHAT
        
        # Get rid of \\ prefix and split the prompt
        sequence = prompt.lstrip('\\').split(" ")
        
        # Split content and command
        if len(sequence) > 1:
            content = sequence[1:]
        command = sequence[0]
        
        # Change by command
        match command:
            case "role":
                
                # Set minimum arguments
                if min_arguments(1,content):
                    role = content[0]
                    
                    # Change role or error
                    if role in roleCodes:
                        ROLE = roleCodes[role]
                        print(f"[command] Role switched to '{ROLE}'")
                        
                    else:
                        print("[command] Unknown role")
            
            case "chat":
                
                # Change mode
                print("[command] Mode switched to 'chat'")
                CHAT = True
                
            case "tell":
                
                # Change mode
                print("[command] Mode switched to 'tell'")
                CHAT = False
                
            case "exit":
                
                # Quit
                print("Goodbye!")
                exit()
                
            case "reset":
                
                # Clear history
                print("[command] Memory has been cleared")
                bot.clear_history()
                
            case "cls":
                
                # Reset text
                help_text()
                
            case _:
                
                # Error on unknown command
                print("[command] Unknown command")
                
    while True:
        
        # Get user prompt
        prompt = input(f"[{ROLE}] ")
        
        # \\ Commands
        if prompt.startswith("\\"):
            interpret_special(prompt)
            continue
        
        # Other bot prompts
        if CHAT:
            print("[assistant] "+bot.chat(prompt,role=ROLE))
        else:
            bot.tell(prompt,role=ROLE)
            
if __name__ == "__main__":
    
    # Parse arguments
    parser = ArgumentParser("Gregium - Ollama LLM",description="An easy way of interacting with Ollama LLMs with python")
    parser.add_argument("--model","-m",type=str,default="granite3.3",help="The Ollama model to use (to install new ones use 'ollama pull {model name}')")
    parser.add_argument("--tools","-t",type=bool,default=False,help="Allows the AI to use additional tools (see `ai_tools` for full function list)")
    args = parser.parse_args()
    
    main(args)