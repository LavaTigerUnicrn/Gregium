"""
POSIX (macOS,linux,etc.) terminal inputs
"""
from .keycodes import *
import sys
import re
import os

# Dictionary of keycodes (For faster recall)
# Shifted streams
stream_modified = {"5A":CTRL_UP,"5B":CTRL_DOWN,"5C":CTRL_RIGHT,"5D":CTRL_LEFT,"2A":SHIFT_UP,"2B":SHIFT_DOWN,"2C":SHIFT_RIGHT,"2D":SHIFT_LEFT,"5H":CTRL_HOME,"5F":CTRL_END,"2E":SHIFT_NUMPAD_CENTER,"5E":CTRL_NUMPAD_CENTER,"3E":ALT_NUMPAD_CENTER,"3H":ALT_HOME,"3F":ALT_END,"3A":ALT_UP,"3B":ALT_DOWN,"3C":ALT_RIGHT,"3D":ALT_LEFT,"2P":SHIFT_F1,"2Q":SHIFT_F2,"2R":SHIFT_F3,"2S":SHIFT_F4,"5P":CTRL_F1,"5Q":CTRL_F2,"5R":CTRL_F3,"5S":CTRL_F4}

# Normal single char streams
stream_basic = {"\x7f":BACKSPACE,"\r":ENTER,"\x1b":ENTER,"\t":TAB,"\x1a":UNDO,"\x19":REDO,"\x18":CUT,"\x03":PASTE,"\x08":CTRL_BACKSPACE,"\x16":PASTE,"\x0c":CTRL_L,"\x06":FIND}

# \x1b streams
stream_x1b = {"Z":SHIFT_TAB,"A":UP,"B":DOWN,"C":RIGHT,"D":LEFT,"F":END,"H":HOME,"E":NUMPAD_CENTER,"P":F1,"Q":F2,"R":F3,"S":F4}

# Navigation keys
stream_nav = ("INSERT","DELETE","","PAGE_UP","PAGE_DOWN")
stream_nav_modif = {"5~":"CTRL_","2~":"SHIFT_","3~":"ALT_"}

# Get input for a POSIX terminal (macOS,linux,etc.)
def posix():
        
    def getch(flush:bool=True) -> bytes|str:
        
        # Flush previously pressed keys
        if flush:
            
            termios.tcflush(sys.stdin, termios.TCIFLUSH)

        # Get the pressed characters
        stream = [sys.stdin.read(1)]
        
        # If start of sequence is '\x1b' check for other escapes
        if stream[0] == "\x1b":
            
            # Disable blocking (let the stdin instantly finish without enter key press)
            fd = sys.stdin.fileno()
            old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
            
            # Clear '[' character
            sys.stdin.read(1)
            
            # Get new character and add if it is not blank
            newChar = sys.stdin.read(1)
            if newChar != "":
                stream.append(newChar)
                
            # For shift arrow keys and ctrl arrow keys
            if newChar == "1":
                
                # Clear ';' character
                sys.stdin.read(1)
                
                # Get last 2 characters
                stream.append(sys.stdin.read(2))
                
                # Reset blocking
                fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)

                # Decipher the key if possible
                if stream[2] in stream_modified:
                    return stream_modified[stream[2]]
                else:
                    return "".join(stream)
                
            # Other navigation keys
            if newChar in ["5","6","3","2"]:
                
                # Get tilda
                sys.stdin.read(1)
                
                # Test if it has a modifier
                additional_sequence = sys.stdin.read(2)
                
                # Combine keys
                key_nav = stream_nav[int(stream[1])-2]
                if additional_sequence in stream_nav_modif:
                    key_nav = stream_nav_modif[additional_sequence] + key_nav
                                    
                # Reset blocking
                fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
                
                # Convert the string into keycode
                return eval(key_nav)
            
            # Reset blocking
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
    
        # Handling 1 character inputs
        if len(stream) == 1:
            if stream[0] in stream_basic:
                return stream_basic[stream[0]]
            else:
                return stream[0]
                
        # Handling \x1b inputs
        if stream[1] in stream_x1b:
            return stream_x1b[stream[1]]
                
        return "".join(stream)
        
    def start():
        
        global old
        
        # Get old settings
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        
        # Set tty settings
        tty.setraw(fd)
        
        # Make sure the terminal resets on finish
        atexit.register(end)
        
    def end():
        
        # Reset settings
        termios.tcsetattr(sys.stdin.fileno(),termios.TCSADRAIN,old)
        
    def get_cursor_position():
        
        # Write the escape sequence
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        
        # Get the output
        buffer = sys.stdin.read(1)
        
        # Read all of the return
        while buffer[-1] != "R":
            buffer += sys.stdin.read(1)
        
        # Get the information from buffer
        matched:re.Match[str] = re.match(r"^\x1b\[(\d*);(\d*)R",buffer)
        groups = matched.groups()
        
        # Return y,x (shifted due to nt terminal)
        return int(groups[0])-1,int(groups[1])-1
    
    # Return all of the generated functions and import the curses library
    import termios
    import tty
    import fcntl
    import atexit
    return getch,start,end,get_cursor_position