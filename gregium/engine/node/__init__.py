import pygame
from ..vector import vector2
from ..rendering import clip_abs

class Node2D:
    
    _x:int
    _y:int
    _w:int
    _h:int
    _rect:pygame.Rect
    children:list["Node2D"]
    
    def __init__(self,rect:pygame.Rect):
        
        # Inputted values
        self._rect = rect
        
        # Properties
        self._x = rect.x
        self._y = rect.y
        self._w = rect.w
        self._h = rect.h
        
        # Children
        self.children = []
        
    def add_child(self,child:"Node2D"):
        
        self.children.append(child)
        
    def remove_child(self,child:"Node2D"):
        
        self.children.remove(child)
        
    def list_children(self):
        
        return self.children
    
    def blit(self,surf:pygame.Surface,rect:pygame.Rect):
        
        pass
    
    def relative_clipping(self,area:pygame.Rect):
        
        return clip_abs(self._rect,area)
        
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self,value:int):
        self._x = value
        self._rect.x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self,value:int):
        self._y = value
        self._rect.y = value
        
    @property
    def w(self):
        return self._w
    
    @w.setter
    def w(self,value:int):
        self._w = value
        self._rect.w = value
    
    @property
    def h(self):
        return self._h
    
    @h.setter
    def h(self,value:int):
        self._h = value
        self._rect.h = value
        
    @property
    def rect(self):
        return self._rect
    
    @rect.setter
    def rect(self,value:pygame.Rect):
        self._x = value.x
        self._y = value.y
        self._w = value.w
        self._h = value.h
        self._rect = value