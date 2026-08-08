from pygame import Rect, Surface

from ..vector import vector2

class Node2D:
    
    _x:int
    _y:int
    _w:int
    _h:int
    _position:vector2
    rect:Rect
    children:list[Node2D]
    
    def __init__(self,rect:Rect):
        """
        The base of all 2D objects
        
        Arguments:
            rect:
                The rectangle for the node to be
        """
        
    def add_child(self,child:Node2D):
        """
        Add a child to the node
        
        Arguments:
            child:
                The child to add
        """
        
    def remove_child(self,child:Node2D):
        """
        Remove a child from the node
        
        Arguments:
            child:
                The child to remove
        """
        
    def list_children(self) -> list[Node2D]:
        """
        Lists all children of the node
        """
    
    def blit(self,surf:Surface,rect:Rect):
        """
        The default blit, this should be overridden by another blit function
        
        Arguments:
            surf:
                The surface to render to
            rect:
                The rect space to truncate the object at
        """
        
    def relative_clipping(self,area:Rect):
        """
        Generates a new clipping mask for pygame to use to clip objects
        
        Arguments:
            area:
                The original area for the clipping mask (absolute)
        """
        
    @property
    def x(self) -> int:
        """
        The X location of the object
        """
    
    @x.setter
    def x(self,value:int): ...
    
    @property
    def y(self) -> int:
        """
        The Y location of the object
        """
    
    @y.setter
    def y(self,value:int): ...
        
    @property
    def w(self) -> int:
        """
        The width of the object
        """
    
    @w.setter
    def w(self,value:int): ...
    
    @property
    def h(self) -> int:
        """
        The height of the object
        """
    
    @h.setter
    def h(self,value:int): ...