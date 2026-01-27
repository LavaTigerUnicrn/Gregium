"""
Formats text using Markdown syntax

Uses discord-like syntax

Small change(s) from default markdown:

"__" now underlines text and not bolding

Supports:
* ~~Strikethrough~~ (~~)
* **Bolding** (**)
* *Italicization* (*)
* ***Bold & Italicization*** (***)
* <u>Underline</u> (__)
* `Blocks` (`)
"""

import re

class MarkdownError(Exception):
    pass

# Generate regex pattern
char_delimiters:list[str] = ["***","**","*","__","~~","`"]
regex_delimiters:list[str] = ["\\"+"\\".join(list(x)) for x in char_delimiters]
regex_pattern:str = f"({'|'.join(regex_delimiters)})"

def format(text:str) -> str:
    """
    Formats the text using modified markdown notation
    
    Uses discord-like syntax

    Small change(s) from default markdown:
    
    "__" now underlines text and not bolding
    
    Arguments:
        text:
            The text to format
            
    Supports:
    * ~~Strikethrough~~ (~~)
    * **Bolding** (**)
    * *Italicization* (*)
    * ***Bold & Italicization*** (***)
    * <u>Underline</u> (__)
    * `Blocks` (`)
    """
    
    generated_text = ""
    
    # Split by regex and remove all blanks
    split_text:list[str] = [x for x in re.split(regex_pattern,text) if x]
    
    # Possible markdown tags
    ital = False
    bold = False
    bold_ital = False
    under = False
    strike = False
    block = False
    
    # Begin parsing
    for text in split_text:
        
        # Check for tags
        match text:
            
            # Italicization
            case "*":
                
                # Block '***' within '*'
                if bold_ital:
                    
                    raise MarkdownError("Cannot toggle italicization (*) within bold-italicization (***) mode")
                
                # Toggle
                if ital:
                    
                    generated_text += "\x1b[23m"
      
                else:
                    
                    generated_text += "\x1b[3m"
                    
                ital = not ital
                
            # Bold
            case "**":
                
                # Block '***' within '**'
                if bold_ital:
                    
                    raise MarkdownError("Cannot toggle bold (**) within bold-italicization (***) mode")
                
                # Toggle
                if bold:
                    
                    generated_text += "\x1b[22m"
                        
                else:
                    
                    generated_text += "\x1b[1m"
                    
                bold = not bold
                
            # Bold - Italicization
            case "***":
                
                # Block '**' within '***'
                if bold:
                    
                    raise MarkdownError("Cannot toggle bold-italicization (***) within bold (**) mode")
                
                # Block '*' within '***'
                if ital:
                    
                    raise MarkdownError("Cannot toggle bold-italicization (***) within italicization (*) mode")
                
                # Toggle
                if bold_ital:
                    
                    generated_text += "\x1b[22;23m"
                        
                else:
                    
                    generated_text += "\x1b[1;3m"
                    
                bold_ital = not bold_ital
                
            # Underline
            case "__":
                
                # Toggle
                if under:
                    
                    generated_text += "\x1b[24m"
                        
                else:
                    
                    generated_text += "\x1b[4m"
                    
                under = not under
                
            # Strikethrough
            case "~~":
                
                # Toggle
                if strike:
                    
                    generated_text += "\x1b[29m"
                    
                else:
                    
                    generated_text += "\x1b[9m"
                    
                strike = not strike
                    
            # Code blocks
            case "`":
                
                # Toggle
                if block:
                    
                    generated_text += "\x1b[27m"
                    
                else:
                    
                    generated_text += "\x1b[7m"
                    
                block = not block
            
            # All other text
            case _:
                
                generated_text += text
                
    return generated_text