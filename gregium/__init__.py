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
    # ?????????
    def __init__(self):
        """
        Only used in Font.from_sys() and Font.from_file() so that 
        extensions such as pylance or other python extensions that 
        complete will work correctly when initializing from the alternate methods.
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
        Font.from_sys() or Font.from_file() method.
        gregium.Font allows easier blitting and modification of 
        fonts pygame is unable to replicate.
        """
        self.font:pygame.freetype.Font = fontInst

    def blit(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None):
        """
        Will blit text to the main working window at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully left-aligned based on the pos parameter.

        *Will raise an error if gregium.init() is not run first
        """
        if altWindow == None:
            altWindow = WINDOW
        for layer,txt in enumerate(text.split("\n")):
            self.font.render_to(altWindow,(pos[0],pos[1]+(layer*size)),txt,fgcolor,bgcolor,size=size,rotation=angle)

    def blit_center(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None):
        """
        Will blit text to the main working window with center located at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully left-aligned based on the pos parameter.

        *Will raise an error if gregium.init() is not run first
        """
        if altWindow == None:
            altWindow = WINDOW
        for layer,txt in enumerate(text.split("\n")):
            fgr = self.font.get_rect(txt,size=size,rotation=angle)
            self.font.render_to(altWindow,position_center((pos[0],pos[1]+(layer*size)),(fgr.w,fgr.h)),txt,fgcolor,bgcolor,size=size,rotation=angle)

    def blit_true_center(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None):
        """
        Will blit text to the main working window with center located at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully center-aligned based on the pos parameter.

        *Will raise an error if gregium.init() is not run first
        """
        if altWindow == None:
            altWindow = WINDOW
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
    If image load fails empty surface will be returned as well as having a warning

    If you wish for only 1 image (being the edited) set the 'hasOneImage' tag to true
    """
    
    try:
        imageO = pygame.image.load(filePath)
        image = imageO
        if size != None:
            pygame.transform.scale(image,size)
        if rotation != None:
            pygame.transform.rotate(image,rotation)

    except:
        warnings.warn(f"Image: {filePath} not found")
        imageO = pygame.Surface((1,1))
        image = imageO
    
    if hasOneImage:
        return image
    return [imageO,image]

class Sprite:
    def __init__(self,filePath:str,sheetSize:tuple[int,int]=None):
        """
        Create a basic sprite for rendering
        """
        try:
            self.origImage = pygame.image.load(filePath).convert_alpha()
            self.width = self.origImage.get_width()
            self.height = self.origImage.get_height()
            self.rotation = 0
            self.inverted = False

            if sheetSize != None:
                self.is_sheet = True
                self.sheetSize = sheetSize
                self.sheetAnimTicks = 0
                self.sheetTick = 0
                self.imageRect = pygame.Rect(0,0,self.width,self.height)
                self.width /= self.sheetSize[0]
                self.height /= self.sheetSize[1]
            else:
                self.is_sheet = False
                self.sheetSize = (1,1)

            self.updateImage()
            
        except Exception as e:
            print(e)
            self.origImage = None
            self.is_sheet = False

    def updateImage(self):

        if self.origImage == None:
            return -1
        
        self.imageBlit = pygame.Surface((self.width,self.height),pygame.SRCALPHA)

        if self.is_sheet:
            self.imageRect.w = self.width
            self.imageRect.h = self.height
            self.imageBlit.blit(pygame.transform.scale(self.origImage,(self.width*self.sheetSize[0],self.height*self.sheetSize[1])),(0,0),self.imageRect)
        else:
            self.imageBlit.blit(pygame.transform.scale(self.origImage,(self.width*self.sheetSize[0],self.height*self.sheetSize[1])),(0,0))

        self.imageBlit = pygame.transform.rotate(self.imageBlit,self.rotation)
        self.imageBlitRect = self.imageBlit.get_rect()

    def tint_add(self,rgb:tuple[int,int,int]):
        if self.origImage == None:
            return -1
        
        self.imageBlit.fill(rgb,special_flags=pygame.BLEND_RGB_ADD)

    def tint_mult(self,rgb:tuple[int,int,int]):
        if self.origImage == None:
            return -1
        
        self.imageBlit.fill(rgb,special_flags=pygame.BLEND_RGB_MULT)

    def blit(self,window:pygame.Surface,xy:tuple[int,int]):
        if self.origImage == None:
            return -1
        
        window.blit(self.imageBlit,xy)

        return 1
    
    def blit_center(self,window:pygame.Surface,xy:tuple[int,int]):
        if self.origImage == None:
            return -1
        
        window.blit(self.imageBlit,(xy[0]-self.imageBlitRect.w/2,xy[1]-self.imageBlitRect.h/2))

        return 1
    
    def blit_pivot_center(self,window:pygame.Surface,xy:tuple[int,int],pivot:tuple[int,int],angle:float):
        if self.origImage == None:
            return -1
        
        newPoint = rotate(pivot,xy,angle)
        window.blit(self.imageBlit,(newPoint[0]-self.imageBlitRect.w/2,newPoint[1]-self.imageBlitRect.h/2))

        return 1
    
    def updateSheet(self):
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
        If showBoundingBox = True then a box outline will be pasted onto the main window being boundCollideCol on collision and boundApartColor when it isn't
        """
        has_collide = False
        rx = rect.x
        ry = rect.y
        if point[0] >= rx and point[1] >= ry and point[0] <= rx + rect.w and point[1] <= ry + rect.h:
            has_collide = True
        
        if showBoundingBox:
            if has_collide:
                pygame.draw.rect(WINDOW,boundCollideCol,rect,5)
            else:
                pygame.draw.rect(WINDOW,boundApartColor,rect,5)

        return has_collide

    @staticmethod
    def rect_to_rect(rect1:pygame.Rect,rect2:pygame.Rect,showBoundingBox:bool=False,boundCollideCol:tuple[int,int,int]=(0,255,0),boundApartColor:tuple[int,int,int]=(255,0,0)) -> bool:
        """
        Cheks for if each rect is colliding with another
        If showBoundingBox = True then a box outline will be pasted onto the main window being boundCollideCol on collision and boundApartColor when it isn't
        """
        has_collide = False
        
        raise NotImplementedError()

events = {"other":{},"quit":False,"mouseDown":False,"mouseUp":False,"mousePos":(0,0),"keyInput":"","highlighted":True}
def clearEvent():
    global events
    events = {"other":{},"quit":False,"mouseDown":False,"mouseUp":False,"mousePos":pygame.mouse.get_pos(),"keyInput":events["keyInput"],"highlighted":events["highlighted"]}
def supplyEvent(event:pygame.event.Event):
    """
    Gives pygame events to gregium (events supplied must be from pygame.from.event.get() from each for iteration, to put it simply use <for event in pygame.event.get()> and use this function with event as param)
    """
    global events
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
    global events
    if events["highlighted"]:
        try:
            events["keyInput"] += key.char
        except AttributeError:
            if key == keyboard.Key.backspace:
                events["keyInput"] = events["keyInput"][:-1]
            elif key == keyboard.Key.space:
                events["keyInput"] += " "

def keyHandler():
    with keyboard.Listener(on_press=on_press) as listener:
        global listenerE
        listenerE = listener
        listener.join()
        
threading.Thread(target=keyHandler,args=()).start()

#### ---- BUTTON HANDLER ---- ####
class button:
    def __init__(self,pos:tuple[float,float],size:tuple[float,float],color:tuple[int,int,int]=(255,255,255),outline:tuple[int,int,int]=(0,0,0),outlineThick:int=5,suppliedFont:Font=None,text:str="",textCol:tuple[int,int,int]=(0,0,0),textSize:int=25,colorHighlight:tuple[int,int,int]=(200,200,200),outlineHighlight:tuple[int,int,int]=(55,55,55),align:str="topLeft"):
        """
        Generates a simple button at pos with outline if outlinethick is above 0 and text if font and text are supplied
        """
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

        rtrn = 0
        rectPos = alignPos(self.pos,self.align)
        self.rect.x,self.rect.y = rectPos[0],rectPos[1]
        coll = collide.point_to_rect(self.rect,events["mousePos"])
        if coll and not self.hasClicked:
            pygame.draw.rect(WINDOW,self.colorH,self.rect)
            if self.renderOutline:
                pygame.draw.rect(WINDOW,self.outlineColH,self.rect,self.outlineThick)
            if events["mouseDown"]:
                self.hasClicked = True
            rtrn = 1
        else:
            pygame.draw.rect(WINDOW,self.color,self.rect)
            if self.renderOutline:
                pygame.draw.rect(WINDOW,self.outlineCol,self.rect,self.outlineThick)
        if self.hasClicked:
            rtrn = 3
            if coll and events["mouseUp"]:
                rtrn = 2
                self.hasClicked = False
            elif events["mouseUp"] or not coll:
                self.hasClicked = False

        if self.renderText:
            self.fontS.blit_true_center(self.text,get_rect_center(self.rect),self.fontSize,fgcolor=self.textCol)

        return rtrn
    
class alertBox:
    def __init__(self,suppliedFont:Font,buttons:tuple=("ok",),title:str=None,color:tuple[int,int,int]=(0,0,0),outline:tuple[int,int,int]=(255,255,255),textCol:tuple[int,int,int]=(255,255,255)):
        """
        Generates alert box with supplied buttons, title can be multi-lined with \\n usage
        """
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
        Render alert, will return 0 on no buttons pressed and the pressed button on clicked
        """

        outP = 0
        wc = get_window_center()
        self.box.x,self.box.y = wc[0]-350,wc[1]-250
        pygame.draw.rect(WINDOW,self.color,self.box)
        pygame.draw.rect(WINDOW,self.outline,self.box,5)
        self.font.blit_center(self.title,(wc[0],wc[1]-200),size=40)
        for n, buttonN in enumerate(self.buttons):
            self.button.pos[0],self.button.pos[1] = (((self.buttonW+20)*n)+wc[0]-330),wc[1]+130
            self.button.text = buttonN
            self.button.hasClicked = self.buttonClickData[n]
            if self.button.render() == 2:
                outP = buttonN
            self.buttonClickData[n] = self.button.hasClicked

        return outP

def cmdParseSeg(segment:str,requestedType:str,min="N/A",max="N/A"):
        match requestedType:
            case "str":
                return segment.replace("\"","")
            case "int":
                try:
                    segNum = int(segment)
                    if min != "N/A":
                        if not segNum >= min:
                            return (6,"Value outside of accepted range")
                    if max != "N/A":
                        if not segNum <= max:
                            return (6,"Value outside of accepted range")
                    return segNum
                except:
                    return (5,"Could not make into an Integer")
            case "float":
                try:
                    segNum = float(segment)
                    if min != "N/A":
                        if not segNum >= min:
                            return (6,"Value outside of accepted range")
                    if max != "N/A":
                        if not segNum <= max:
                            return (6,"Value outside of accepted range")
                    return segNum
                except:
                    return (7,"Could not make into an Float")
            case "json":
                try:
                    return json.loads(segment)
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
        cmdList = ""
        if len(args) > 0:
            cmdD = self.cmds[args[0]]
            for cmdSeg in cmdD:
                cmdList += f"{cmdSeg}:{cmdD[cmdSeg]}\n"
            return f'{args[0]}:\n{cmdList}'
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
    listenerE.stop()
    quit()