import pygame
from ..text import ARIAL,Font
from .base import UIBase
from .. import rendering

class Button(UIBase):
    
    color:pygame.Color
    hover_color:pygame.Color
    clicked_color:pygame.Color
    clicked:bool
    hovered:bool
    
    def __init__(self,rect:pygame.Rect,color:pygame.Color=(128,128,128),hover_color:pygame.Color=(255,255,255),clicked_color:pygame.Color=(128,128,128),click_function=None):
        """
        A button to easily render to pygame window
        
        Arguments:
            rect:
                The rectangle of the button
            color:
                The default color of the button
            hover_color:
                The color of the button when hovered
            clicked_color:
                The color of the button when clicked
            click_function:
                The function to run when the button is clicked
        """
        
        # Inputted values
        self.color = color
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        
        # Set click function
        if click_function is not None:
            self.click_function = click_function
        
        # Default values
        self.hovered = False
        self.clicked = False
        
        # Generate
        super().__init__(rect)
        
    def blit(self,surf:pygame.Surface,rect:pygame.Rect|None=None):
        """
        Render button to pygame surface
        
        Arguments:
            surf:
                The surface to render to
            rect:
                The rect space to truncate the object at
        """
        
        # Choose color
        color = self.color
        if self.hovered:
            color = self.hover_color
        if self.clicked:
            color = self.clicked_color
        
        # Render
        pygame.draw.rect(surf,color,self.rect)
        
    def click_function(self):
        
        pass
        
    def bind_click(self,click_func):
        """
        Binds a new click function
        
        Arguments:  
            click_func:
                The function to run on click
        """
        
        self.click_function = click_func
        
        
    def update(self,mouse_position:pygame.typing.Point,mouse_buttons:tuple[bool,bool,bool]):
        """
        Updates button status
        
        Arguments:
            mouse_position:
                The position of the mouse (x,y)
                
                (You can use pygame.mouse.get_pos() for input)
            mouse_buttons:
                The pressed buttons of the mouse [left, middle, right]
                
                (You can use pygame.mouse.get_pressed() for input)
        """
        
        # Split position and buttons
        m_x,m_y = mouse_position
        left, _, _ = mouse_buttons
        
        # Disable clicking
        if not left:
            
            self.clicked = False
        
        # Skip is button is no longer highlighted
        if not self.rect.collidepoint(m_x,m_y):
            
            self.hovered = False
            
            return
        
        self.hovered = True
        
        # Execute click if button is clicked
        if left:
            
            self.clicked = True
            self.click_function()
            
class TextButton(Button):
    
    text:str
    font:Font
    fgcolor:pygame.Color
    size:int
    
    def __init__(self,rect:pygame.Rect,text:str,color:pygame.Color=(128,128,128),hover_color:pygame.Color=(255,255,255),clicked_color:pygame.Color=(128,128,128),click_function=None,font:Font=ARIAL,fgcolor:pygame.Color=(0,0,0),size:int=25):
        """
        A button to easily render to pygame window
        
        Arguments:
            rect:
                The rectangle of the button
            text:
                The text on the button
            color:
                The default color of the button
            hover_color:
                The color of the button when hovered
            clicked_color:
                The color of the button when clicked
            click_function:
                The function to run when the button is clicked
            font:
                The font to use (otherwise it will use arial)
            fgcolor:
                The color of the font text
            size:
                The size of the font
        """
        
        # Inputted values
        self.font = font
        self.text = text
        self.fgcolor = fgcolor
        self.size = size

        # Generate
        super().__init__(rect,color,hover_color,clicked_color,click_function)
        
    def blit(self,surf:pygame.Surface,area:pygame.Rect|None=None):
        """
        Render button to pygame surface
        
        Arguments:
            surf:
                The surface to render to
            area:
                The rect space to truncate the object at (this should be absolute)
        """
        
        # Choose color
        color = self.color
        if self.hovered:
            color = self.hover_color
        if self.clicked:
            color = self.clicked_color
        
        # Make area relative to object
        if area is not None:
            rect_area = self.relative_clipping(area)
            # Render
            pygame.draw.rect(surf,color,rendering.clip_rect(self.rect,rect_area))
        else:
            # Alternate Render (No Clip)
            pygame.draw.rect(surf,color,self.rect)
        
        # Render text
        text_position = (self.x+self.w/2,self.y+self.h/2)
        self.font.render_to_centered(surf,text_position,text=self.text,fgcolor=self.fgcolor,size=self.size,area=area)
