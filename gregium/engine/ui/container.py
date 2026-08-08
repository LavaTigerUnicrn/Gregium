import pygame

from . import buttons
from .base import UIBase


class ContainerBase(UIBase):
    
    uses_custom_arrange:bool=False
    
    def __init__(self,rect:pygame.Rect):
        
        """
        The basic container, can orient all items within itself
        
        In the case where the items exceed the space of the container, they will be truncated
        
        Arguments:
            rect:
                The rect space of the container
        """
        
        # Generate
        super().__init__(rect)
        
    def blit(self,surf:pygame.Surface):
        """
        Render all buttons to pygame surface
        
        Arguments:
            surf:
                The surface to render to
        """
        
        # Arrange buttons
        if self.uses_custom_arrange:
            self.custom_arrange(self)
        else:
            self.arrange()
        
        # Render all buttons
        for child in self.children:
            
            child.blit(surf,self.rect)
            
    def arrange(self):
        """
        Arranges all children within itself
        
        The base container does nothing to them
        """
    
    def custom_arrange(self,_:"ContainerBase"):
        """
        The custom arrange function, this doesn't do anything
        """
    
    def set_custom_arrange(self,arrange_func):
        """
        Sets a new arrangement function
        
        Arguments:
            arrange_func:
                The new function to arrange objects
        """
        self.uses_custom_arrange = True
        self.custom_arrange = arrange_func
    
    def update(self,mouse_position:pygame.typing.Point,mouse_buttons:tuple[bool,bool,bool]):
        """
        Updates all contained buttons
        
        Arguments:
            mouse_position:
                The position of the mouse (x,y)
                
                (You can use pygame.mouse.get_pos() for input)
            mouse_buttons:
                The pressed buttons of the mouse [left, middle, right]
                
                (You can use pygame.mouse.get_pressed() for input)
        """
        
        # Update all buttons
        for button in self.children:
            
            if issubclass(type(button),UIBase):
            
                button.update(mouse_position,mouse_buttons)
            
class VBoxContainer(ContainerBase):
    
    def __init__(self,rect:pygame.Rect):
    
        """
        A container that orients all buttons stacked vertically within itself
        
        In the case where the items exceed the space of the container, they will be truncated
        
        Arguments:
            rect:
                The rect space of the container
        """
        
        # Generate
        super().__init__(rect)
        
    def arrange(self):
        """
        Arranges all children within itself vertically
        """
        
        # Count up total height
        total_height = 0
        
        for child in self.children:
            
            total_height += child.h
            
        # Get padding
        padding = (self.h - total_height) / len(self.children)
        
        # Space by padding
        y = self.y
        
        #self.children[0].y = 0
        # Move each object
        for child in self.children:
            
            child.y = int(y)
            
            y += padding + child.h