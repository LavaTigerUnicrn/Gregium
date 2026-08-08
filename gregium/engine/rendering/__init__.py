from pygame import Rect

def clip_abs(rect:Rect,area:Rect):
    """
    Generates a new clipping mask for pygame to use to clip objects
    
    Arguments:
        rect:
            The rect space of the object, this should start at the top-left corner of the surface and end at the bottom right (absolute)
        area:
            The original area for the clipping mask (absolute)
    """

    area_left = max(area.x-rect.x,0)
    area_top = max(area.y-rect.y,0)
    area_width = area.w - rect.x + area.x
    area_height = area.h - rect.y + area.y
    
    return Rect(area_left,area_top,area_width,area_height)

def clip_rect(rect:Rect,area:Rect) -> Rect:
    """
    Clip a rectangle into area bounds
    
    rect:
        The rect to clip
    area:
        The rect space to truncate the object at (this should be relative)
    """
    
    # Clip rect
    new_x = rect.x
    if area.x > rect.x:
        new_x = area.x
    new_y = rect.y
    if area.y > rect.y:
        new_y = area.y
        
    # Clip rect size
    new_w = min(rect.w,area.w)
    new_h = min(rect.h,area.h)
    
    # Generate new rect
    return Rect(new_x,new_y,new_w,new_h)