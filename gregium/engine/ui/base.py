import pygame
from ..node import Node2D

class UIBase(Node2D):
    
    def update(self,mouse_position:pygame.typing.Point,mouse_buttons:tuple[bool,bool,bool]):
        """
        Updates UI status using mouse stats
        
        Arguments:
            mouse_position:
                The position of the mouse (x,y)
                
                (You can use pygame.mouse.get_pos() for input)
            mouse_buttons:
                The pressed buttons of the mouse [left, middle, right]
                
                (You can use pygame.mouse.get_pressed() for input)
        """