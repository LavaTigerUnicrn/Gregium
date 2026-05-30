"""
More of a proof on concept, use at your own risk
"""

import sys
import math
from PIL import Image
import requests
from io import BytesIO
import pygame.surfarray as surfarray
import pygame

halfPi = math.pi / 2
pi = math.pi
brightness_map:str = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
brightness_map_disvisor:float = round(255/(len(brightness_map)-1),5)
brightness_map_mean_disvisor:float = round(255/(len(brightness_map)-1),5)*3

def getDirFromPos(y:int,x:int,half_width:float,half_height:float):
    if x == half_width:
        return halfPi + (pi if y-half_height < 0 else 0) 
    return math.atan((y-half_height)/(x-half_width)) + (pi if x-half_width < 0 else 0)
    
def getPosFromAngle(angle:float,distance:float) -> tuple[int,int]:
    """
    Angle should be in radians
    """
    return (distance*math.cos(angle),distance*math.sin(angle))
    
def colorRGBA(r:int,g:int,b:int,a:int=255) -> str:
    """
    Returns the correct pixel with color
   
    Arguments:
        r:
            Red value
        g:
            Green value
        b:
            Blue value
        a:
            Optional value, lower values make text darker (like less opacity)
    """
   
    return colorPixel((r,g,b,a))

def colorPixel(pixel:tuple[int,int,int,int],useAlphaPixel:bool) -> str:
    """
    Returns the correct pixel with color
   
    Arguments:
        pixel:
            Must have at least r,g,b,a* values
        useAlphaPixel:
            Ignores the alpha value of the pixel entirely 
    """
    
    if useAlphaPixel:
        alpha = pixel[3]
    else:
        alpha = 255
    r = min(pixel[0],alpha)
    g = min(pixel[1],alpha)
    b = min(pixel[2],alpha)
    symbol = brightness_map[min(max(math.ceil((r+g+b)/brightness_map_mean_disvisor),0),91)]
    return f"\x1b[38;2;{r};{g};{b}m{symbol}"

def compilePixelData(data:list[list[tuple[int,int,int,int]]],useAlphaPixel:bool) -> str:
    """
    Returns compiled string based on pixel data
    """
    string = ""
   
    for row in data:
        for pixel in row:
            string += colorPixel(pixel,useAlphaPixel)
        string += "\n"
   
    string = string[:-1] # To cut off last \n
   
    return string
 
def averageTuplesWeighted(tuple1:tuple,tuple2:tuple,weight1:int,weight2:int):
    return tuple([int((tuple1[i]*weight1+tuple2[i]*weight2)/2) if i < 3 else min(tuple1[i]+tuple2[i],255) for i in range(len(tuple1))])
 
class Surface:
    width:int
    height:int
    alpha:int
    useAlphaPixels:bool
    data:list
    
    def __init__(self,width:int,height:int,forceNoData:bool=False,useAlphaPixels:bool=True):
        """
        Generates a new surface that is able to be blitted to another or viewed with __str__
        
        Arguments:
            width:
                The width of the surface
            height:
                The height of the surface
            forceNoData:
                Generates the surface blank if true (data must be added manually)
            useAlphaPixels:
                If set to false will stop looking for an alpha pixels and treat all as if they were full
                
                This will still generate alpha pixels when applicable
        """
        self.width:int = width
        self.height:int = height
        self.alpha:int = 1
        self.useAlphaPixels = useAlphaPixels
        
        if not forceNoData:
            self.data:list[list[tuple[int,int,int,int]]] = [[(0,0,0,255) for w in range(width)] for h in range(height)]
    
    def set_alpha(self,value:int):
        """
        Sets the alpha override (0-1)
        THIS IS NOT THE SAME AS PIXEL ALPHA VALUE
        """
        self.alpha = value
        
    def blit(self,surface:"Surface",coordinates:tuple[int,int]):
        surface_width = surface.width
        surface_height = surface.height
        data = self.data.copy()
        width = self.width
        height = self.height
        surface_data = surface.data.copy()
        x_modif = int(coordinates[0])
        y_modif = int(coordinates[1])
        alpha = surface.alpha*2
        if alpha == 0:
            return
        else:
            for y in range(surface_height):
                if y+y_modif >= height:
                    return
                for x in range(surface_width):
                    if x+x_modif >= width:
                        break
                    data_pos = surface_data[y][x]
                    # Add in missing alpha
                    if len(data_pos) < 4:
                        data_pos = list(data_pos)+[255,]
                    alphaModif = alpha*(data_pos[3]/255)
                    data[y+y_modif][x+x_modif] = averageTuplesWeighted(data_pos,data[y+y_modif][x+x_modif],alphaModif,2-alphaModif)

        self.data = data
        
    def blit_center(self,surface:"Surface",coordinates:tuple[int,int]):
        self.blit(surface,(coordinates[0]-surface.width/2,coordinates[1]-surface.height/2))
        
    def fill(self,color:tuple[int,int,int,int]):
        if len(color) < 4:
            color = tuple(list(color) + [255,])
        data = self.data
        for y in range(self.height):
            for x in range(self.width):
                data[y][x] = color
        self.data = data  
    
    def subsurface(self,left:int,right:int,top:int,bottom:int) -> "Surface":
        data = self.data
        height = self.height
        new_surface = Surface(right-left,bottom-top,forceNoData=True)
        new_data = []
        for y in range(height):
            new_data.append(data[y][left:right])
        new_data = new_data[top:bottom]
        new_surface.data = new_data
        return new_surface
        
    def __str__(self):
       
        return compilePixelData(self.data,self.useAlphaPixels)

WINDOW:Surface = Surface(0,0)
        
        
class display:
    @staticmethod
    def set_mode(width:int,height:int):
        """
        Generate window
        """
        global WINDOW
        WINDOW = Surface(width,height)
        return WINDOW
    @staticmethod
    def write(ratio:int=1):
        """
        Write data to terminal (Must call flip after)
        
        This does not work on CMD terminal, use `display.write_flip_safe()` instead
        
        Arguments:
            ratio:
                The ratio of width to height of each character (on most terminals is about 0.6)
        """
        sys.stdout.write("\x1b[H\x1b[2\x1b[3J\x1b[3J")
        if ratio == 1:
            sys.stdout.write(WINDOW.__str__())
        else:
            sys.stdout.write(transform.scale(WINDOW,(WINDOW.width,int(WINDOW.height*ratio))).__str__())

    @staticmethod
    def flip():
        """
        Flush terminal (Must be called after write)
        """
        sys.stdout.flush()
        
    @staticmethod
    def write_flip_safe(ratio:int=1,clr_terminal:bool=True):
        """
        Write and flip data to CMD terminal
        
        This is much slower than `display.write()` but will work consistently
        
        Arguments:
            ratio:
                The ratio of width to height of each character (on most terminals is about 0.6)
            clr_terminal:
                Will clear the terminal on each update (this may cause flickering)
        """
        if clr_terminal:
            sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
        else:
            sys.stdout.write("\x1b[H")
        if ratio == 1:
            generated = WINDOW.__str__()
        else:
            generated = transform.scale(WINDOW,(WINDOW.width,int(WINDOW.height*ratio))).__str__()
            
        for line in generated.split("\n"):
            sys.stdout.write(line+"\n")
            sys.stdout.flush()


class image:
    @staticmethod
    def load_pygame(surf:pygame.Surface) -> Surface:
        """
        Converts a pygame surface into ascii surface
        
        This needs to be flipped across the x and rotated 90 degrees in order to render properly
        
        Arguments:
            surf: 
                The pygame surface
        """
        new_surf = Surface(surf.width,surf.height,True,False)
        new_surf.data = surfarray.array3d(surf).tolist()
        return new_surf
        
    @staticmethod
    def load_web(url:str) -> Surface:
        """
        Loads an image from the web
        
        Arguments:
            url:
                The url to load from
        """
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return image.load_pil(img)
    
    @staticmethod
    def load_pil(image:Image.Image) -> Surface:
        """
        Loads an image from a pillow image instance
        
        Arguments:
            image:
                The pillow image instance
        """
        width,height = image.width,image.height
        img = image.convert("RGBA").load()
        surface = Surface(width,height,True)
        surface_data = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(img[x,y])
            surface_data.append(line)
        surface.data = surface_data
        return surface

class transform:
    @staticmethod
    def scale(original:Surface,coordinates:tuple[int,int]) -> Surface:
        width = coordinates[0]
        height = coordinates[1]
        x_ratio = original.width/width
        y_ratio = original.height/height
        
        new = Surface(width,height,True)
        new_data = []
        data = original.data.copy()
        for y in range(height):
            row = []
            for x in range(width):
                row.append(data[int(y*y_ratio)][int(x*x_ratio)])
            new_data.append(row)
            
        new.data = new_data
        return new
    
    @staticmethod
    def rotate(original:Surface,angle_degree:float) -> Surface:
        angle_radian = math.radians(angle_degree)
        width = original.width
        height = original.height
        half_height = height/2
        half_width = width/2
        data = original.data
        
        new_width = 0
        new_height = 0
        
        a1 = getDirFromPos(height,width,half_width,half_height) - angle_radian
        a2 = getDirFromPos(0,width,half_width,half_height) - angle_radian
        a3 = getDirFromPos(0,0,half_width,half_height) - angle_radian
        a4 = getDirFromPos(height,0,half_width,half_height) - angle_radian
        
        radius = math.sqrt((height-half_height)**2+(width-half_width)**2)
        x1,y1 = getPosFromAngle(a1,radius)
        x2,y2 = getPosFromAngle(a2,radius)
        x3,y3 = getPosFromAngle(a3,radius)
        x4,y4 = getPosFromAngle(a4,radius)
        
        min_x = min(x1,x2,x3,x4)
        min_y = min(y1,y2,y3,y4)
        max_x = max(x1,x2,x3,x4)
        max_y = max(y1,y2,y3,y4)
        
        new_width = math.ceil(max_x - min_x)
        new_height = math.ceil(max_y - min_y)
        
        new_half_width = new_width / 2
        new_half_height = new_height / 2
        new_surface = Surface(new_width,new_height,forceNoData=True)
        new_data = []

        orig_data = original.data.copy()
        for y in range(new_height):
            row = []
            for x in range(new_width):
                angle = getDirFromPos(y,x,new_half_width,new_half_height) # I LOVE A2T
                distance = math.sqrt((x-new_half_width)**2+(y-new_half_height)**2)
                angle += angle_radian
                new_x,new_y = getPosFromAngle(angle,distance)
                new_x = int(new_x+half_width)
                new_y = int(new_y+half_height)
                
                if width-1 < new_x or new_x < 0:
                    row.append((0,0,0,0))
                    continue
                if height-1 < new_y or new_y < 0:
                    row.append((0,0,0,0))
                    continue
                row.append(data[new_y][new_x])
            new_data.append(row)
        new_surface.data = new_data
        return new_surface
        
    @staticmethod
    def auto_trim(original:Surface) -> Surface:
        width = original.width
        height = original.height
        data = original.data.copy()
        trim_l = width
        trim_r = 0
        trim_u = height
        trim_d = 0
        for y in range(height):
            for x in range(width):
                if data[y][x][3] == 0:
                    continue
                
                trim_l = min(trim_l,x-1)
                trim_d = max(trim_d,y+1)
                trim_r = max(trim_r,x+1)
                trim_u = min(trim_u,y-1)
                
        # Ensure none is below 0 (or above width/height)
        trim_l = max(trim_l,0)
        trim_r = min(trim_r,width)
        trim_u = max(trim_u,0)
        trim_d = min(trim_d,height)
                
        return original.subsurface(trim_l,trim_r,trim_u,trim_d)
        
    @staticmethod
    def grayscale(original:Surface) -> Surface:
        width = original.width
        height = original.height
        
        new = Surface(width,height,True)
        new_data = []
        for pixelRow in original.data.copy():
            row = []
            for pixel in pixelRow:
                row.append(tuple([sum(pixel[:-1])/3,]*3+[pixel[3],]))
            new_data.append(row)

        new.data = new_data
        return new