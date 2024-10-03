"""
The core of Gregium
v0.2

See docs at: 
https://docs.google.com/document/d/1KtBRR3mXbcjt4zKhA5wF2QNwm-vt10tR8TIWEoapXyA/edit?usp=sharing
"""

# Pygame Imports
import pygame, pygame.freetype, pygame.image

# Other Required Imports
import math
import warnings
import zipfile
import os
import threading
import json
from pathlib import Path
from pynput import keyboard

# Declaring Globals
PATH = str(Path(__file__).parent.absolute())
WINDOW = None

# Initializing Pygame
pygame.init()

def init():
    """
    Will define the global WINDOW variable to the current 
    working window, required for many functions to run

    *pygame.display.set_mode() must be run first to create the window
    """

    # Redefines global "WINDOW" to be the current working surface
    global WINDOW
    WINDOW = pygame.display.get_surface()

def alignPos(pos:tuple[float,float], 
             align:str="topLeft") -> tuple[float,float]:
    """
    Aligns a position to a corner of the window, possible corners to align to include, 
    topRight, topLeft, bottomRight, bottomLeft, centerRight, 
    centerLeft, centerTop, centerBottom, and center, 
    each of which scale relative to the size of the window.
    The default position is topLeft and running alignPos 
    with topLeft returns the same value; 
    bottomRight is the opposite corner and will add the 
    total x & y values of the window respectively.

    Will raise error if gregium.init() is not run first
    """

    # Make sure there is a window specified
    if WINDOW != None:
        
        # Set corner based on the value of "align"
        match align:
            case "topRight":
                return (pos[0]+WINDOW.get_width(),
                        pos[1])
            case "topLeft":
                return pos
            case "bottomRight":
                return (pos[0]+WINDOW.get_width(),
                        pos[1]+WINDOW.get_height())
            case "bottomLeft":
                return (pos[0],
                        pos[1]+WINDOW.get_height())
            case "centerRight":
                return (pos[0]+WINDOW.get_width(),
                        pos[1]+(WINDOW.get_height()/2))
            case "centerLeft":
                return (pos[0],pos[1]+(WINDOW.get_height()/2))
            case "centerBottom":
                return (pos[0]+(WINDOW.get_width()/2),
                        pos[1]+WINDOW.get_height())
            case "centerTop":
                return (pos[0]+(WINDOW.get_width()/2),
                        pos[1])
            case _:
                return pos
                
    # If the window isn't loaded, throw an informational error
    else:
        raise Exception("Must run init first")

def rotate(origin:tuple[float,float], point:tuple[float,float], 
           angle:float) -> tuple[float,float]:
    """
    Will rotate a point counterclockwise around a given origin, 
    new point position is based on original distance to the origin, 
    angle must be given in degree form for function to work properly.

    *May have small rounding errors
    """

    # Converts the value of "angle" into radians
    ang = math.radians(angle)

    # Unpacks the "origin" and "point" variables
    ox, oy = origin
    px, py = point

    # Converts degrees to radians
    ang = math.radians(angle)

    # Split up point tuple
    ox, oy = origin
    px, py = point

    # Calculate new position based on angle
    qx = ox + math.cos(ang) * (px - ox) - math.sin(ang) * (py - oy)
    qy = oy + math.sin(ang) * (px - ox) + math.cos(ang) * (py - oy)

    # Return new position in the form of a tuple
    return (qx, qy)

def get_window_center() -> tuple[float,float]:
    """
    Returns the center of the current working window.

    *Will raise error if gregium.init() is not run first
    """

    # Get center & return
    return (WINDOW.get_width()/2,WINDOW.get_height()/2)

def position_center(original:tuple[float,float],
                    size:tuple[float,float]) -> tuple[float,float]:
    """
    Will return the coordinates required 
    (assuming shape is blitted from top-left corner) 
    in which the center of the object will be at original 
    for given size.

    *Not the same as get_center()
    """

    # Sutract size to make blitting pos (top-left) yield the center
    return (original[0]-(size[0]/2),original[1]-(size[1]/2))

def get_center(original:tuple[float,float],
                size:tuple[float,float]) -> tuple[float,float]:
    """
    Will return the center of the shape assuming the original 
    is in the top left of the given size.

    *Not the same as position_center()
    """
def get_rect_center(rect:pygame.Rect) -> tuple[float,float]:
    """
    Returns the center coordinates of the given pygame.Rect 
    element based on the x & y coordinates of it.
    """
    # Add width & height to rect to get center coordinates
    return (rect.x+rect.w/2,rect.y+rect.h/2)

#### ---- FONT HANDLER ---- ####
class FontType(type):
    def __init__(self):
        """
        Only used in Font.from_sys() and Font.from_file() so that 
        extensions such as pylance or other python extensions that 
        autocomplete will work correctly when initializing from the alternate methods.
        """
        self.font:pygame.freetype.Font = pygame.freetype.Font()
    
    def blit(self,text:str,pos:tuple[int,int],size:int=20,
             fgcolor:tuple[int,int,int]=(255,255,255),
             bgcolor:tuple[int,int,int]=None,
             angle:int=0):
        pass

    def blit_center(self,text:str,pos:tuple[int,int],size:int=20,
                    fgcolor:tuple[int,int,int]=(255,255,255),
                    bgcolor:tuple[int,int,int]=None,
                    angle:int=0):
        pass

    def blit_true_center(self,text:str,pos:tuple[int,int],size:int=20,
                         fgcolor:tuple[int,int,int]=(255,255,255),
                         bgcolor:tuple[int,int,int]=None,
                         angle:int=0):
        pass
    
class Font:
    def __init__(self,fontInst:pygame.freetype.Font):
        """
        Defines a font instance from a pygame.freetype.font, 
        font must have been initialized through pygame.freetype.font 
        unless using the 
        Font.from_sys() or Font.from_file() methods.
        gregium.Font allows easier blitting and modification of 
        fonts which pygame is unable to replicate.
        """
        self.font:pygame.freetype.Font = fontInst

    def blit(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None):
        """
        Will blit text to the main working window at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully left-aligned based on the pos parameter.

        *Will raise an error if gregium.init() is not run first
        """

        # Sets working window to the main window if nothing is specified
        if altWindow == None:
            altWindow = WINDOW

        # Blits text onto specified window (or default if no window is provided)
        for layer,txt in enumerate(text.split("\n")):
            self.font.render_to(altWindow,(pos[0],pos[1]+(layer*size)),txt,fgcolor,bgcolor,size=size,rotation=angle)

    def blit_center(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None):
        """
        Will blit text to the main working window with center located at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully left-aligned based on the pos parameter.

        *Will raise an error if gregium.init() is not run first
        """

        # Sets working window to the main window if nothing is specified
        if altWindow == None:
            altWindow = WINDOW

        # Blits center of the text onto coordinates in the specified window (or default if no window is provided)
        for layer,txt in enumerate(text.split("\n")):
            fgr = self.font.get_rect(txt,size=size,rotation=angle)
            self.font.render_to(altWindow,position_center((pos[0],pos[1]+(layer*size)),(fgr.w,fgr.h)),txt,fgcolor,bgcolor,size=size,rotation=angle)

    def blit_true_center(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None):
        """
        Will blit text to the main working window with center located at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully center-aligned based on the pos parameter.

        *Will raise an error if gregium.init() is not run first
        """

        # Sets working window to the main window if nothing is specified
        if altWindow == None:
            altWindow = WINDOW

        # ????????????? Not exactly sure
        splitTxt = text.split("\n")
        yOffS = ((len(splitTxt)-1)*size)/2
        for layer,txt in enumerate(splitTxt):
            fgr = self.font.get_rect(txt,size=size,rotation=angle)
            self.font.render_to(altWindow,position_center((pos[0],pos[1]+(layer*size)-yOffS),(fgr.w,fgr.h)),txt,fgcolor,bgcolor,size=size,rotation=angle)

    @classmethod
    def from_sys(self,fontName:str) -> FontType:
        """
        Will initialize the same font as the gregium.Font method but instead from a system font using the pygame.freetype.SysFont method.
        """
        return self(pygame.freetype.SysFont(fontName,20))
    
    @classmethod
    def from_file(self,filePath:str) -> FontType:
        """
        Will initialize the same font as the gregium.Font method but instead uses a font file path the same way the main gregium.Font is initialized via the pygame.freetype.Font method.
        """
        return self(pygame.freetype.Font(filePath,20))
        
#### ---- SPRITE HANDLER ---- ####
def SpriteOnlyImg(filePath:str,size:tuple[int,int]=None,rotation:int=0,hasOneImage:bool=False) -> tuple[pygame.Surface,pygame.Surface]:
    """
    Generates an Image-Only sprite without class information
    First Surface is original image (for repeat changing)
    Second Surface is modified image to current settings, if nothing is applied both surfaces will be the same
    If image load fails, empty surface will be returned as well as having a warning

    If you wish for only 1 image (being the edited) set the 'hasOneImage' tag to true
    """
    
    try:
        # Loads the image based on the given file path
        imageO = pygame.image.load(filePath)
        image = imageO

        # Transforms the scale/rotation of the image if specified
        if size != None:
            pygame.transform.scale(image,size)
        if rotation != None:
            pygame.transform.rotate(image,rotation)

    # Warns user if the filepath is invalid
    except:
        warnings.warn(f"Image: {filePath} not found")
        imageO = pygame.Surface((1,1))
        image = imageO
    
    # Returns only the edited image, if user specifies to
    if hasOneImage:
        return image
    
    # Returns the original and edited image
    return [imageO,image]

class Sprite:
    def __init__(self,filePath:str,sheetSize:tuple[int,int]=None):
        """
        Create a basic sprite for rendering
        """

        try:
            # Loads the image and sets up variables of the class
            self.origImage = pygame.image.load(filePath).convert_alpha()
            self.width = self.origImage.get_width()
            self.height = self.origImage.get_height()
            self.rotation = 0
            self.inverted = False

            # Sets up spritesheets for animation as specified by the user
            if sheetSize != None:
                self.is_sheet = True
                self.sheetSize = sheetSize
                self.sheetAnimTicks = 0
                self.sheetTick = 0
                self.imageRect = pygame.Rect(0,0,self.width,self.height)
                self.width /= self.sheetSize[0]
                self.height /= self.sheetSize[1]

            # Disables sprite sheets and animation
            else:
                self.is_sheet = False
                self.sheetSize = (1,1)

            # Updates the sprite's image
            self.updateImage()
            
        # If an invalid argument is passed, nullify the image
        except Exception as e:
            print(e)
            self.origImage = None
            self.is_sheet = False

    def updateImage(self):
        """
        Updates the image for animation/movement
        """

        # Return with a failed exit code if there is no image
        if self.origImage == None:
            return -1
        
        # ????????
        self.imageBlit = pygame.Surface((self.width,self.height),pygame.SRCALPHA)

        # If spritesheets are enabled, display the next sprite
        if self.is_sheet:
            self.imageRect.w = self.width
            self.imageRect.h = self.height
            self.imageBlit.blit(pygame.transform.scale(self.origImage,(self.width*self.sheetSize[0],self.height*self.sheetSize[1])),(0,0),self.imageRect)
        
        # Otherwise, redisplay the sprite
        else:
            self.imageBlit.blit(pygame.transform.scale(self.origImage,(self.width*self.sheetSize[0],self.height*self.sheetSize[1])),(0,0))

        # Reposition the sprite and reset the sprite's Rect value
        self.imageBlit = pygame.transform.rotate(self.imageBlit,self.rotation)
        self.imageBlitRect = self.imageBlit.get_rect()

    def tint_add(self,rgb:tuple[int,int,int]):
        """Tint the sprite with the given color"""
        
        # Return with a failed exit code if there is no image
        if self.origImage == None:
            return -1
        
        # Tints the sprite with the rgb color
        self.imageBlit.fill(rgb,special_flags=pygame.BLEND_RGB_ADD)

    def tint_mult(self,rgb:tuple[int,int,int]):
        """??????"""

        # Return with a failed exit code if there is no image
        if self.origImage == None:
            return -1
        
        # ??????? idk difference between the tint single and mult
        # Also nolan should ther be a return 1 here
        self.imageBlit.fill(rgb,special_flags=pygame.BLEND_RGB_MULT)

    def blit(self,window:pygame.Surface,xy:tuple[int,int]):

        # Return with a failed exit code if there is no image
        if self.origImage == None:
            return -1
        
        # Blits the sprite using existing class variables and arguments
        window.blit(self.imageBlit,xy)

        return 1
    
    def blit_center(self,window:pygame.Surface,xy:tuple[int,int]):

        # Return with a failed exit code if there is no image
        if self.origImage == None:
            return -1
        
        # Blits the sprite's center at the given coordinates
        window.blit(self.imageBlit,(xy[0]-self.imageBlitRect.w/2,xy[1]-self.imageBlitRect.h/2))

        return 1
    
    def blit_pivot_center(self,window:pygame.Surface,xy:tuple[int,int],pivot:tuple[int,int],angle:float):

        # Return with a failed exit code if there is no image
        if self.origImage == None:
            return -1
        
        # ????????? idk difference with this p
        newPoint = rotate(pivot,xy,angle)
        window.blit(self.imageBlit,(newPoint[0]-self.imageBlitRect.w/2,newPoint[1]-self.imageBlitRect.h/2))

        return 1
    
    def updateSheet(self):
        """
            Updates the active sprite in the spritesheet
        """

        # ?????????? NEeds commenting i sorta get it but not fuly
        if self.sheetTick >= self.sheetAnimTicks:
            self.sheetTick = 0
            self.imageRect.x += self.width
            if self.imageRect.x >= self.width*self.sheetSize[0]:
                self.imageRect.x = 0
                self.imageRect.y += self.height

            if self.imageRect.y >= self.height*self.sheetSize[1]:
                self.imageRect.y = 0
        self.sheetTick += 1

#### ---- ZIP HANDLER ---- ####
class zip:
    
    @staticmethod
    def zipFolder(folder:str,zipPath:str) -> None:
        """
        Zips a folder without recursion
        """
        with zipfile.ZipFile(zipPath,"w") as zip:
            for file in os.listdir(folder):
                zip.write(folder+"\\"+file)
    
#### ---- COLLISION HANDLER ---- ####
class collide:
    @staticmethod
    def point_to_rect(rect:pygame.Rect,point:tuple[float,float],showBoundingBox:bool=False,boundCollideCol:tuple[int,int,int]=(0,255,0),boundApartColor:tuple[int,int,int]=(255,0,0)) -> bool:
        """
        Cheks for if each rect is colliding with a point
        If showBoundingBox is True, then a box outline will be pasted onto the main window being boundCollideCol on collision and boundApartColor when it isn't
        """

        # Initializing variables
        has_collide = False
        rx = rect.x
        ry = rect.y

        # If the point is inside the Rect, updated has_collide to True
        if point[0] >= rx and point[1] >= ry and point[0] <= rx + rect.w and point[1] <= ry + rect.h:
            has_collide = True

        # Draw the bounding box if specified by user
        if showBoundingBox:
            if has_collide:
                pygame.draw.rect(WINDOW,boundCollideCol,rect,5)
            else:
                pygame.draw.rect(WINDOW,boundApartColor,rect,5)

        # Return if the rect collided with the point
        return has_collide

    @staticmethod
    def rect_to_rect(rect1:pygame.Rect,rect2:pygame.Rect,showBoundingBox:bool=False,boundCollideCol:tuple[int,int,int]=(0,255,0),boundApartColor:tuple[int,int,int]=(255,0,0)) -> bool:
        """
        Cheks for if each rect is colliding with another
        If showBoundingBox = True then a box outline will be pasted onto the main window being boundCollideCol on collision and boundApartColor when it isn't
        """
        has_collide = False
        
        raise NotImplementedError()

# Set up object with events
events = {"other":{},"quit":False,"mouseDown":False,"mouseUp":False,"mousePos":(0,0),"keyInput":"","highlighted":True}

def clearEvent():
    """Resets events to defaults ???????? needs a check definiely"""
    global events
    events = {"other":{},"quit":False,"mouseDown":False,"mouseUp":False,"mousePos":pygame.mouse.get_pos(),"keyInput":events["keyInput"],"highlighted":events["highlighted"]}
def supplyEvent(event:pygame.event.Event):
    """
    Gives pygame events to gregium (events supplied must be from pygame.from.event.get() from each for iteration, to put it simply use <for event in pygame.event.get()> and use this function with event as param)
    """
    global events

    # Update the global events variable based on the value of "event"
    match event.type:
        case pygame.QUIT:
            events["quit"]
        case pygame.MOUSEBUTTONDOWN:
            events["mouseDown"] = True
        case pygame.MOUSEBUTTONUP:
            events["mouseUp"] = True
        case pygame.WINDOWFOCUSGAINED:
            events["highlighted"] = True
        case pygame.WINDOWFOCUSLOST:
            events["highlighted"] = False
        case _:
            events["other"][event.type] = True

def on_press(key):
    """?????"""
    global events

    # ??????? what is highilighted exactlh?
    if events["highlighted"]:
        try:
            events["keyInput"] += key.char

        # ??????????
        except AttributeError:
            if key == keyboard.Key.backspace:
                events["keyInput"] = events["keyInput"][:-1]
            elif key == keyboard.Key.space:
                events["keyInput"] += " "

def keyHandler():
    """??????"""
    with keyboard.Listener(on_press=on_press) as listener:
        global listenerE
        listenerE = listener
        listener.join()
        
threading.Thread(target=keyHandler,args=()).start()

#### ---- BUTTON HANDLER ---- ####
class button:
    def __init__(self,pos:tuple[float,float],size:tuple[float,float],color:tuple[int,int,int]=(255,255,255),outline:tuple[int,int,int]=(0,0,0),outlineThick:int=5,suppliedFont:Font=None,text:str="",textCol:tuple[int,int,int]=(0,0,0),textSize:int=25,colorHighlight:tuple[int,int,int]=(200,200,200),outlineHighlight:tuple[int,int,int]=(55,55,55),align:str="topLeft"):
        """
        Generates a simple button at pos with outline (if a thickness is provided) and text (if font and text are provided)
        """

        # Initialize class variables
        self.pos = list(pos)
        self.align = align
        rectPos = alignPos(pos,align)
        self.rect = pygame.Rect(rectPos[0],rectPos[1],size[0],size[1])
        self.outlineCol = outline
        self.outlineColH = outlineHighlight
        self.color = color
        self.colorH = colorHighlight
        self.textCol = textCol
        self.text = text
        self.fontSize = textSize
        self.fontS = suppliedFont
        self.renderText = len(text)>0 and suppliedFont != None
        self.renderOutline = outlineThick > 0
        self.outlineThick = outlineThick
        self.hasClicked = False

    def render(self):
        """
        Renders button with resulting int being
        0: no collision
        1: mouse collision
        2: mouse clicked on collision (pressed up and down)
        3: mouse pressed down on collision
        """

        # Initializing variables, checking for collision with current mouse position
        rtrn = 0
        rectPos = alignPos(self.pos,self.align)
        self.rect.x,self.rect.y = rectPos[0],rectPos[1]
        coll = collide.point_to_rect(self.rect,events["mousePos"])

        # Check if mouse is simply hovering over the react
        if coll and not self.hasClicked:
            pygame.draw.rect(WINDOW,self.colorH,self.rect)
            if events["mouseDown"]:
                self.hasClicked = True
            
            # Draw an outline if a thickness was provided
            if self.renderOutline:
                pygame.draw.rect(WINDOW,self.outlineColH,self.rect,self.outlineThick)
            
            rtrn = 1
        
        else:
            # Draw and render the rectangle onto the window
            pygame.draw.rect(WINDOW,self.color,self.rect)

            # Draw an outline if a thickness was provided
            if self.renderOutline:
                pygame.draw.rect(WINDOW,self.outlineCol,self.rect,self.outlineThick)

        # Check if a click event is active
        if self.hasClicked:
            rtrn = 3

            # Check if the click is completed (mouse is pressed and released)
            if coll and events["mouseUp"]:
                rtrn = 2
                self.hasClicked = False
            elif events["mouseUp"] or not coll:
                self.hasClicked = False

        # Render text if text and font were provided
        if self.renderText:
            self.fontS.blit_true_center(self.text,get_rect_center(self.rect),self.fontSize,fgcolor=self.textCol)

        return rtrn
    
class alertBox:
    def __init__(self,suppliedFont:Font,buttons:tuple=("ok",),title:str=None,color:tuple[int,int,int]=(0,0,0),outline:tuple[int,int,int]=(255,255,255),textCol:tuple[int,int,int]=(255,255,255)):
        """
        Generates alert box with supplied buttons, title can be multi-lined with \\n usage
        """

        # Initializing class variables
        self.buttons = buttons
        wc = get_window_center()
        self.color = color
        self.outline = outline
        self.box = pygame.Rect(wc[0]-350,wc[1]-250,700,500)
        self.buttonW = (660-(20*(len(buttons)-1)))/len(buttons)
        self.button = button((0,wc[1]+130),(self.buttonW,100),color,outline,text="Loading...",textCol=textCol,suppliedFont=suppliedFont)
        self.buttonClickData = [False for x in range(len(buttons))]
        self.title = title
        self.font = suppliedFont

    def render(self):
        """
        Render an alert. Will return 0 on no buttons pressed. Returns the pressed button if one is clicked
        """

        # Prepare and draw the alert
        outP = 0
        wc = get_window_center()
        self.box.x,self.box.y = wc[0]-350,wc[1]-250
        pygame.draw.rect(WINDOW,self.color,self.box)
        pygame.draw.rect(WINDOW,self.outline,self.box,5)
        self.font.blit_center(self.title,(wc[0],wc[1]-200),size=40)

        # Loop through all given buttons
        for n, buttonN in enumerate(self.buttons):
            self.button.pos[0],self.button.pos[1] = (((self.buttonW+20)*n)+wc[0]-330),wc[1]+130
            self.button.text = buttonN
            self.button.hasClicked = self.buttonClickData[n]

            # If a button is clicked, output that button
            if self.button.render() == 2:
                outP = buttonN
            self.buttonClickData[n] = self.button.hasClicked

        return outP

def cmdParseSeg(segment:str,requestedType:str,min="N/A",max="N/A"):
    """Function for parsing strings, integers, floats, and json"""

    # Check for different types of the material to parse
    match requestedType:

        case "str":
            # Remove all double quotes in strings
            return segment.replace("\"","")

        case "int":
            try:
                # Make sure the integer is within the range of (min, max)
                segNum = int(segment)
                if min != "N/A":
                    if segNum < min:
                        return (6,"Value outside of accepted range")
                if max != "N/A":
                    if segNum > max:
                        return (6,"Value outside of accepted range")
                return segNum
            
            # Return with exit code 5 if argument was invalid
            except:
                return (5,"Could not make into an Integer")
            
        
        case "float":
            try:
                # Make sure the float is within the range of (min, max)
                segNum = float(segment)
                if min != "N/A":
                    if not segNum >= min:
                        return (6,"Value outside of accepted range")
                if max != "N/A":
                    if not segNum <= max:
                        return (6,"Value outside of accepted range")
                return segNum
            
            # Return with exit code 7 if argument was invalid
            except:
                return (7,"Could not make into an Float")
            
        case "json":
            try:
                # Return a parsed python object of the given segment
                return json.loads(segment)
            
            # Return with exit code 8 if something fails (usually an invalid json)
            except Exception as e:
                return (8,"Json error: "+e)
                
class CLI:
    def __init__(self,tree:dict={}):
        """
        Make easy command interpreters that can be used outside, or inside terminal
        """
        self.cmds = tree

    def addCmd(self,commandDict:dict):
        """
        add a new command! Syntax is as follows
        {"name":{"root":{"type":"*","var":"test","next":"foo"},"foo":{"type":"*","var":"test2","next":"etc"}}}

        *Types include, str, json, int, float, literal, func
        int & float can have min and max
        literal must have a list of outputs
        func must have a "run" variable instead of next and var and the "run" variable must have the function in it
        you can imput multiple commands by having multiple in the furthest outside dict
        repeat commands will not get overwritten but will instead throw an error
        """
        for cmd in commandDict:
            self.cmds[cmd] = commandDict[cmd]

    def helpcmd(self,*args):
        """Generate a help message for using commands"""

        cmdList = ""

        # Return a specific help message for a given command
        if len(args) > 0:
            cmdD = self.cmds[args[0]]
            for cmdSeg in cmdD:
                cmdList += f"{cmdSeg}:{cmdD[cmdSeg]}\n"
            return f'{args[0]}:\n{cmdList}'
        
        # Return a list of every existing command
        for cmd in self.cmds:
            cmdList += f'{cmd}\n'
        return f'Commands:\n{cmdList}Type help (command) for specific syntax'
    
    def run(self,cmd:str) -> tuple[int,str]:
        """
        Read a full command from a string and output code (error, return) or (0, return) on sucess
        """

        #Initial split
        newCmd = cmd.split(" ")

        #Recombine strings and json
        cmdRun = []
        isOpenStr = False
        openJsonIndex = 0
        sectionComb = ""

        for section in newCmd:
            sectionComb += section
            wasOpenStr = False
            for ltr in section:
                if wasOpenStr and openJsonIndex == 0:
                    return (1,"String must end at parameter end") 
                if ltr == "\"":
                    isOpenStr = not isOpenStr
                    if not isOpenStr:
                        wasOpenStr = True
                if ltr == "{" and not isOpenStr:
                    openJsonIndex += 1
                if ltr == "}" and not isOpenStr:
                    openJsonIndex -= 1
                if openJsonIndex < 0:
                    return (2,"Closed json before opening")
            if not isOpenStr and openJsonIndex == 0:
                cmdRun.append(sectionComb)
                sectionComb = ""
            else:
                sectionComb += " "
        if openJsonIndex > 0:
            return (3,"Not all json instances have been closed")
            
        #Help command
        if cmdRun[0] == "help":
            if len(cmdRun) > 1:
                if cmdRun[1] in self.cmds:
                    return self.helpcmd(cmdRun[1])
                else:
                    return self.helpcmd()
            else:
                return self.helpcmd()

        #Run command
        if cmdRun[0] in self.cmds:
            isReadingStart = False
            nextIndex = "root"
            cmd = self.cmds[cmdRun[0]]
            supArgs = {}
            for item in cmdRun:
                if isReadingStart:
                    match cmd[nextIndex]["type"]:
                        case "literal":
                            nextFound = cmd[nextIndex]["next"]
                            if item in nextFound:
                                nextIndex = item
                            else:
                                return (9,"Could not find next literal")
                        case "func":
                            return (10,"Too many arguments")
                        case _:
                            relMin = "N/A"
                            relMax = "N/A"
                            if "min" in cmd[nextIndex]:
                                relMin = cmd[nextIndex]["min"]
                            if "max" in cmd[nextIndex]:
                                relMax = cmd[nextIndex]["max"]
                            parsedSeg = cmdParseSeg(item,cmd[nextIndex]["type"],relMin,relMax)
                            if type(parsedSeg) != tuple:
                                supArgs[cmd[nextIndex]["var"]] = parsedSeg
                                nextIndex = cmd[nextIndex]["next"]
                            else:
                                return parsedSeg
                isReadingStart = True
            if nextIndex != "func":
                return (11,"Not enough arguments")
            return cmd[nextIndex]["run"](kwargs=supArgs)
                
        else:
            return (4, "Command not found")

def stop():
    """Stops the gregium engine"""
    listenerE.stop()
    quit()