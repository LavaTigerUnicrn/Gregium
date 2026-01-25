def main():

    print("Please wait...")

    from . import Queue

    # Make a queue
    queue = Queue()
    queue.wipe_dir()

    # Get user input
    text = input("\x1b[H\x1b[2JEnter some text\n")

    # Generate
    print("Please wait...")
    queue.generate(text)

    while not queue.has_completed():
        
        queue.check_play()
        queue.check_generate()

def main_rvc(model_name:str):

    print("Please wait...")

    from . import load_model

    # Make a queue
    queue = load_model(model_name)
    queue.wipe_dir()

    # Get user input
    text = input("\x1b[H\x1b[2JEnter some text\n")

    # Generate
    print("Please wait...")
    queue.generate(text)

    while not queue.has_completed():
        
        queue.check_play()
        queue.check_generate()
        
if __name__ == "__main__":
    
    main()