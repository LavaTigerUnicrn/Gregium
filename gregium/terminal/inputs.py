# Import libraries
import os
from . import posix
from . import nt
from . import keycodes as keycodes
import sys
import time
from ..settings import DEFAULT_TERMINAL_CHOICE_HELP,TERMINAL_CAROUSEL
from typing import Any

# Set the python default input
pythonInput = input

# Set the python default print
pythonPrint = print

# Define new print
def print(text="",end:str="\n\r",Flush:bool=True):
    pythonPrint(text,end=end,flush=Flush)

# Get the system
system = os.name

# Get module for terminal type
inputDirectory = {"posix":posix.posix,"nt":nt.nt}

# Try to find the functions in the given terminal type
try:
    print(f"Loading terminal: {system}")
    getch,start,end,get_cursor_position = inputDirectory[system.lower()]()
    
except Exception:
    
    # If the terminal type isn't supported, allow user to enter another
    print(f"Terminal: {system} not supported")
    bootName = pythonInput(f"Manual boot\nNAME ({", ".join(list(inputDirectory.keys()))})> ")
    
    # Try to import new given terminal
    try:
        getch,start,end,get_cursor_position = inputDirectory[bootName.lower()]()
        
    # If failed again, give error message and quit
    except Exception as e:
        print(f"Boot of ({bootName}) failed: {type(e).__name__}; {e}")
        quit(1)

# Define clear function
def clear():
        
        # Clear screen, reset cursor, clear colors
        print("\x1b[2J\x1b[H\x1b[0m",end="")

# Generates options kwargs from a dictionary of options
def options_from_dict(options:dict[Any,dict[str,str]]) -> dict:
    
    gen_options = []
    gen_optionsName = []
    gen_optionsDesc = []
    
    # Load from each
    for option_key in options:
        
        option = options[option_key]
        
        # Get name
        name = str(option_key)
        if "name" in option:
            name = option["name"]
            
        # Get desc
        desc = ""
        if "desc" in option:
            desc = option["desc"]
            
        # Add to lists
        gen_options.append(option_key)
        gen_optionsName.append(name)
        gen_optionsDesc.append(desc)
        
    # Make kwarg and return
    return {"options":gen_options,"optionsName":gen_optionsName,"optionsDesc":gen_optionsDesc}

# Choosing function    
def choice(options:list[str],optionsName:list[str]|None=None,optionsDesc:list[str]|None=None,help:bool=DEFAULT_TERMINAL_CHOICE_HELP) -> str:
    
    # Fill in blank data
    if optionsName is None:
        optionsName = [str(x) for x in options]
    if optionsDesc is None:
        optionsDesc = [""]*len(options)
    
    # Set selected to the start
    selected = 0
    
    # Loop until an option is chosen
    while True:
        
        # Show choice help text
        if help:
            print("(Use arrow keys and enter)")
        
        # Lower and upper bounds
        lower = ((selected - int(TERMINAL_CAROUSEL/2)) if len(optionsName) > TERMINAL_CAROUSEL else 0)
        upper = (selected + int(TERMINAL_CAROUSEL/2)) % len(optionsName)
        
        # Get section
        selectedOptions = []
        if lower < 0 or upper < lower:
            selectedOptions = optionsName[lower:] + optionsName[:upper]
        else:
            selectedOptions = optionsName[lower:upper]
            
        if len(optionsName) <= TERMINAL_CAROUSEL:
            selectedOptions = optionsName
        
        # Show each option and the brackets around the hovered option
        for n,option in enumerate(selectedOptions):
            if n + lower == selected:
                print(f"\x1b[2K[{option}]{' - ' if optionsDesc[n] != '' else ''}{optionsDesc[n]}")
            else:
                print(f"\x1b[2K{option}  " + ' '*(3+len(optionsDesc[n])))
                
        # Get up down or enter input
        match getch():
            case keycodes.UP:
                selected -= 1
            case keycodes.DOWN:
                selected += 1
            case keycodes.ENTER:
                return options[selected]
        
        # Loop selected output
        selected = selected%len(options)
        
        # Set cursor back up to top of the choice menu
        print(f"\x1b[{1*int(help)+n+1}F",end="")
        
def input(text:str) -> str:
    print(text,end="")
    return input_single_line()

def ctrl_backspace(text:str) -> tuple[int,str]:
    
    # Cancel function if nothing in it
    if text == "":
        return (0,"")
    
    # Split the text by spaces, alphanumeric, and special
    split_list = []
    split_text = ""
    split_type = ""
    
    for ltr in text:
        ltr_type = "special"
        if ltr.isalnum():
            ltr_type = "alphanumeric"
        if ltr == "\t" or ltr == " ":
            ltr_type = "space"
        if ltr_type != split_type:
            split_type = ltr_type
            split_list.append(split_text)
            split_text = ""
            
        split_text += ltr
        
    split_list.append(split_text)
    
    # Remove automatically if single space
    deleted = 0
    if split_list[len(split_list)-1] == " ":
        split_list = split_list[:-1]
        deleted = 1
    
    # Remove last item and rejoin list    
    return len(split_list[len(split_list)-1])+deleted,"".join(split_list[:-1])

def ctrl_delete(text:str) -> tuple[int,str]:
    
    # Cancel function if nothing in it
    if text == "":
        return (0,"")
        
    # Split the text by spaces, alphanumeric, and special
    split_list = []
    split_text = ""
    split_type = ""
    
    for ltr in text:
        ltr_type = "special"
        if ltr.isalnum():
            ltr_type = "alphanumeric"
        if ltr == "\t" or ltr == " ":
            ltr_type = "space"
        if ltr_type != split_type:
            split_type = ltr_type
            split_list.append(split_text)
            split_text = ""
            
        split_text += ltr
        
    split_list.append(split_text)
    
    # Remove very first blank string
    split_list = split_list[1:]
    
    # Add blank string at the end to prevent errors
    split_list.append("")
    
    # Remove automatically if single space
    deleted = 0
    if split_list[0] == " ":
        split_list = split_list[1:]
        deleted = 1
    
    # Remove last item and rejoin list  
    return len(split_list[0])+deleted,"".join(split_list[1:])

def ctrl_left(text:str) -> int:
    
    return ctrl_backspace(text)[0]

def ctrl_right(text:str) -> int:
    
    return ctrl_delete(text)[0]
    
def input_single_line() -> str:
    
    # Make entered text blank
    entered = ""
    
    # Get the starting position
    start_y,start_x = get_cursor_position()
    start_y += 1
    start_x += 1
    
    # Set cursor position within text
    cursor_pos = 0
    
    # Keep checking until the enter key is pressed
    while True:
        
        # Get pressed characters
        got = getch()
        
        if type(got) is bytes:
            match got:
                
                # Backspace removes 1 character
                case keycodes.BACKSPACE:
                    entered = entered[0:cursor_pos][:-1] + entered[cursor_pos:]
                    cursor_pos -= 1
                    
                # Enter ends text input
                case keycodes.ENTER:
                    break
                
                # Ctrl + backspace removes multiple characters right to left
                case keycodes.CTRL_BACKSPACE:
                    
                    entered_end = entered[cursor_pos:]
                    removed,entered = ctrl_backspace(entered[0:cursor_pos])
                    entered += entered_end
                    cursor_pos -= removed
                
                # Ctrl + delete removes multiple characters left to right  
                case keycodes.CTRL_DELETE:
                    entered_beginning = entered[0:cursor_pos]
                    removed,entered = ctrl_delete(entered[cursor_pos:])
                    entered = entered_beginning + entered

                # Move with arrow keys
                case keycodes.LEFT:
                    
                    cursor_pos -= 1
                
                case keycodes.RIGHT:
                    
                    cursor_pos += 1
                    
                case keycodes.CTRL_LEFT:
                    
                    cursor_pos -= ctrl_left(entered[0:cursor_pos])
                    
                case keycodes.CTRL_RIGHT:
                    
                    cursor_pos += ctrl_right(entered[cursor_pos:])
                    
            # Clamp cursor position
            cursor_pos = max(min(cursor_pos,len(entered)),0)
                     
        else:
            
            # Add new character to entered at position [cursor_pos]
            entered = entered[0:cursor_pos] + str(got) + entered[cursor_pos:]
            
            # Move cursor forward
            cursor_pos += len(got)
            
        # Return cursor, clear line and print out the text, move cursor to where the cursor pos is
        print(f"\r\x1b[{start_y};{start_x}H\x1b[0K{entered}\x1b[{start_y};{cursor_pos+start_x}H",end="")
        
    # Add newline
    print()
    
    # Return the entered text
    return entered