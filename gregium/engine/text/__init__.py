
from pygame import Rect, Surface, freetype
from pygame.freetype import STYLE_DEFAULT

from .. import rendering
from ..typing import Color_RGB, Color_RGBA, Point2_I


class Font(freetype.Font):
    
    def __init__(self,file:str|None,size:float=0,font_index:int=0,resolution:int=0,ucs4:int=False):
        
        super().__init__(file,size,font_index,resolution,ucs4)
    
    @classmethod
    def from_freetype(cls,font:freetype.Font) -> "Font":
        """
        Migrates the freetype font to new font type
        
        Arguments:
            Font: The freetype font instance
        """
        
        # Generate new
        generated = cls(None)
        
        # Steal all attributes
        try:
            for item in dir(font):
                if "__" in item:
                    continue
                
                setattr(generated,item,getattr(font,item))
                
        except AttributeError:
            pass
        
        # Finish
        return generated
    
    def render_to_centered(
            self,
            surf: Surface,
            dest: Point2_I,
            text: str|None,
            fgcolor: Color_RGB|Color_RGBA|None = None,
            bgcolor: Color_RGB|Color_RGBA|None = None,
            style: int = STYLE_DEFAULT,
            rotation: int = 0,
            size: float = 0,
            area:Rect|None = None
        ) -> Rect:
        
        # Draw font
        generated,rectangle = self.render(text,fgcolor=fgcolor,bgcolor=bgcolor,style=style,rotation=rotation,size=size)
        
        # Get rect position
        position = (dest[0]-rectangle.w/2,dest[1]-rectangle.h/2)
        
        # Get clipping area
        text_rect = Rect(position[0],position[1],rectangle.w,rectangle.h)
        text_area = None
        if area is not None:
            text_area = rendering.clip_abs(text_rect,area)
        
        # Render rectangle
        surf.blit(generated,position,text_area)
        
        return rectangle
        
# Load arial font
ARIAL = Font.from_freetype(freetype.SysFont("Arial",50))