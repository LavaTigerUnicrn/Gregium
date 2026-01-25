"""
Allows for rendering ASCII at the maximum possible speed to terminal without any extra computation
"""
import pygame
import pygame.surfarray as surfarray
import os

def color_pixel(r:int,g:int,b:int) -> str:
    """
    Colors a single pixel in ASCII
    
    Arguments:
        r:
            Red
        g:
            Green
        b:
            Blue
    """
    
    return f"\x1b[38;2;{r};{g};{b}m@"

def render_pygame(surface:pygame.Surface):
    """
    Renders a pygame surface directly to stdout
    
    This needs to be flipped across the x and rotated 90 degrees in order to render properly
    
    Arguments:
        surface:
            The pygame surface
    """
    
    # Convert to list
    surflist = surfarray.array3d(surface).tolist()
    
    print("\x1b[0;0H",end="")
    
    for row in surflist:
        
        comb_row = ""
        
        for col in row:
            
            r,g,b = col
            comb_row += color_pixel(r,g,b)
            
        print(comb_row)