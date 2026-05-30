from .realtimestt import generate_recorder
import sys

def main():
    
    # Make recorder
    recorder = generate_recorder()
    
    # Start
    print("Say something")
    
    # Print back text
    print("You said: "+recorder.text())
    
    # Exit
    recorder.stop()
    recorder.abort()
    sys.exit(0)
    
if __name__ == "__main__":
    
    main()