"""
nt (windows) terminal inputs
"""
from .keycodes import *

# Dictionary of keycodes (For faster recall)
# \x1b streams
stream_x1b_basic = {b"H":UP,b"K":LEFT,b"P":DOWN,b"M":RIGHT,b"S":DELETE,b"R":INSERT,b"I":PAGE_UP,b"G":HOME,b"Q":PAGE_DOWN,b"O":END,b"s":CTRL_LEFT,b"t":CTRL_RIGHT,b"\x8d":CTRL_UP,b"\x91":CTRL_DOWN,"\x93":CTRL_DELETE,b"w":CTRL_HOME,b"u":CTRL_END,b"v":CTRL_PAGE_DOWN,b"\x86":CTRL_PAGE_UP,b"\x92":CTRL_INSERT,b"\x93":CTRL_DELETE}

# Alt and Fn Keys
stream_special = {b"\x98":ALT_UP,b"\xa0":ALT_DOWN,b"\x9d":ALT_RIGHT,b"\x9b":ALT_LEFT,b"\xa3":ALT_DELETE,b"\xa2":ALT_INSERT,"\x97":ALT_HOME,"\x9f":ALT_END,b"\x99":ALT_PAGE_UP,b"\xa1":ALT_PAGE_DOWN,b";":F1,b"<":F2,b"=":F3,b">":F4,b"T":SHIFT_F1,b"U":SHIFT_F2,b"V":SHIFT_F3,b"W":SHIFT_F4,b"^":CTRL_F1,b"_":CTRL_F2,b"`":CTRL_F3,b"a":CTRL_F4,b"\x9f":ALT_END,b"\x97":ALT_HOME}

# Shifted characters
stream_shift = {b"Hs":SHIFT_UP,b"Ks":SHIFT_LEFT,b"Ps":SHIFT_DOWN,b"Ms":SHIFT_RIGHT,b"Ss":SHIFT_DELETE}

# Basic characters
stream_basic = {b"\x08":BACKSPACE,b"\r":ENTER,b"\n":CTRL_ENTER,b"\x1b":ESC,b"\t":TAB,b"\x1a":UNDO,b"\x19":REDO,b"\x18":CUT,b"\x03":COPY,b"\x7f":CTRL_BACKSPACE,b"\x0c":CTRL_L,"\x06":FIND,b"\ts":SHIFT_TAB}

# Get input for a nt terminal (Windows)
def nt():
    
    def getch(flush:bool=True) -> bytes|str:
        
        # Flush previous inputs
        if flush:
            while msvcrt.kbhit() > 0:
                msvcrt.getch()
        
        # Get all of the pressed characters
        stream = [msvcrt.getch()]
        while msvcrt.kbhit() > 0:
            stream.append(msvcrt.getch())

        # First stream character
        root_stream = stream[0]
        
        # Handling 1 character inputs
        if len(stream) == 1:
            
            # Shift characters
            if keyboard.is_pressed("shift") and root_stream+b"s" in stream_basic:
                return stream_basic[root_stream+b"s"]

            # Get input char
            if root_stream in stream_basic:
                return stream_basic[root_stream]
            
            # Prevent stream from being in byte form
            try:
                if "\\" in repr(stream[0]):
                    return stream[0]
                return str(stream[0],"utf-8")
            except UnicodeDecodeError:
                # If decode fails, return blank
                return ""
        
        # Handling 2 character inputs
        else:
            
            # Second stream character
            instance = stream[1]
            
            # Match \xe0 instances
            if stream[0] == b"\xe0":
                # Shift characters
                if keyboard.is_pressed("shift") and instance+b"s" in stream_shift:
                    return stream_shift[instance+b"s"]
                if instance in stream_x1b_basic:
                    return stream_x1b_basic[instance]
                         
            # Match \x00 instances
            else:
                
                if instance in stream_x1b_basic:
                    return stream_x1b_basic[instance]
                
                # For alt keys and fn keys
                if instance in stream_special:
                    return stream_special[instance]
                            
        # Check if the key is multiple keys pressed too fast
        hasEscapeSequence = stream[0] in [b"\xe0",b"\x00"]
        if not hasEscapeSequence:
            
            # Join all parts of the stream
            try:
                joinedStream = "".join([str(x,"ascii") for x in stream])
            except UnicodeDecodeError:
                # If decode fails, return blank
                return ""
            
            return joinedStream
        
        # If key is indecipherable, return the entire stream
        return stream[0]+stream[1]
        
    def start():
        global terminal
        
        # Setup blessed terminal
        terminal = Terminal()

    def end():
        
        # Nothing has been changed
        pass
    
    def get_cursor_position():
        
        # Use blessed terminal to get position
        return terminal.get_location()
        
    # Return all of the generated functions and import the msvcrt library
    import msvcrt
    from blessed import Terminal
    import keyboard
    return getch,start,end,get_cursor_position
