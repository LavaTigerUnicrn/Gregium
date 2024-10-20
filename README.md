# Gregium v0.1.7

## Documentation

### init(clock:pygame.Clock)
Will define the global **WINDOW** (and other) variables to the current working window, required for many functions to run

*pygame.display.set_mode() must be run first to create the window
### alignPos(pos:tuple[float,float],align:str=”topLeft”) -> tuple[float,float]:
Aligns a position to a corner of the window, possible corners to align to include, topRight, topLeft, bottomRight, bottomLeft, centerRight, centerLeft, centerTop, centerBottom, and center, each of which scale relative to the size of the window.
The default position is topLeft and running alignPos with topLeft returns the same value; bottomRight is the opposite corner and will add the total x & y values of the window respectively.

*Will raise an error if gregium.init() is not run first

### animRGB(originalRGB:tuple[int,int,int],newRGB:tuple[int,int,int],steps:int) -> list
Makes a list of all rgb values in order to transition from originalRGB to newRGB

### rotate(origin:tuple[float,float], point:tuple[float,float], angle:float) -> tuple[float,float]
Will rotate a point counterclockwise around a given origin, new point position is based on original distance to the origin, angle must be given in degree form for function to work properly.

*May have small rounding errors
### get_window_center() -> tuple[float,float]
Returns the center of the current working window.

*Will raise error if gregium.init() is not run first
### position_center(original:tuple[float,float],size:tuple[float,float]) -> tuple[float,float]
Will return the coordinates required (assuming shape is blitted from top-left corner) in which the center of the object will be at original for given size.

*Not the same as get_center()
### get_center(original:tuple[float,float],size:tuple[float,float]) -> tuple[float,float]
Will return the center of the shape assuming the original is in the top left of the given size.

*Not the same as position_center()
### get_rect_center(rect:pygame.Rect) -> tuple[float,float]
Returns the center coordinates of the given pygame.Rect element based on its x, y coordinates and its width/height.
### FontType()
Only used in Font.from_sys() and Font.from_file() so that autocomplete extensions such as pylance will work correctly when working with the alternate methods.
### Font(fontInst:pygame.freetype.Font)
Defines a font instance from a pygame.freetype.font. Font must have been initialized using pygame.freetype.font, unless the Font.from_sys() or Font.from_file() methods are used. gregium Font allows easier blitting and modification of fonts, which vanilla pygame is unable to replicate.
#### Font.from_sys(fontName:str) -> Font
Will initialize the same font as the gregium. Font method but instead from a system font using the pygame.freetype.SysFont method.
#### Font.from_file(filePath:str) -> Font:
Will initialize the same font as the gregium. Font method but instead uses a font file path the same way the main gregium. Font is initialized via the pygame.freetype.Font method.
The following 3 methods will only work after font initialization.
#### blit(text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None)
Will blit text to the main working window at point pos unless altWindow is specified. all parameters are the same as pygame’s pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully left-aligned based on the pos parameter.

*Will raise an error if gregium.init() is not run first
### blit_center(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None)
Will blit text to the main working window with center located at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully left-aligned based on the pos parameter.

*Will raise an error if gregium.init() is not run first
### blit_true_center(self,text:str,pos:tuple[int,int],size:int=20,fgcolor:tuple[int,int,int]=(255,255,255),bgcolor:tuple[int,int,int]=None,angle:int=0,altWindow:pygame.Surface=None)
Will blit text to the main working window with center located at point pos unless altWindow is specified, all parameters are the same as normal pygame.freetype.Font.render() or pygame.freetype.Font.render_to() parameters; font will be fully center-aligned based on the pos parameter.

*Will raise an error if gregium.init() is not run first
### SpriteOnlyImg(filePath:str,size:tuple[int,int]=None,rotation:int=0,hasOneImage:bool=False) -> tuple[pygame.Surface,pygame.Surface]
Will generate a sprite with the image located at filePath, and with a size (in pixels) equivalent to the size parameter. (leaving blank will result in no change in size), image will also be rotated clockwise by the number of degrees specified. The returned tuple will be in the form of (original image, modified image) unless hasOneImage is specified as True; in that case, only the modified image is sent.

*For memory reasons, it is recommended to almost always set hasOneImage to True. 
### Sprite(filePath:str,sheetSize:tuple[int,int]=None)
Creates a basic sprite for rendering, with a sprite image or sprite sheet loaded from the provided file path. If the sprite has an animation sheet, set the sheetSize argument to the (rows, columns) of the sprite sheet.
#### updateImage(self)
Redraws the sprite’s image and updates its position and orientation.

* The order should **always** be 
#1 updateImage() 
#2 updateDropShadow() only if applicable
#3 tint_add/tint_mult
#4 blit/blit_center/blit_pivot_center
#5 testColl/testCollR **unless you define the "pos" argument**
#### updateDropShadow(self)
Generates a drop shadow for the current frame of the sprite

* Required for any drop shadow to render at all and run every frame of drop shadow before blit
#### tint_add(self,rgb:tuple[int,int,int])
Tints the targeted sprite with a given RGB color.
#### tint_mult(self,rgb:tuple[int,int,int])
Multiplies each pixel on sprite by rgb tint

**For the following three methods, SCRLX and SCRLY represent variables that track the current scroll offset - e.g., scrolling 3px right means SCRLX += 3.
#### blit(self,window:pygame.Surface,xy:tuple[int,int],dropShadow:tuple[int,int]=(0,0))
Blits the targeted sprite onto the given surface. The top left of the sprite will be positioned at the provided coordinate pair PLUS the current SCRLX and SCRLY (x + SCRLX, y + SCRLY). Dropshadow argument controls the x and y offset of the dropshadow (0,0 does not render)
#### blit_center(self,window:pygame.Surface,xy:tuple[int,int],dropShadow:tuple[int,int]=(0,0))
Blits the targeted sprite onto the given surface. The center of the sprite will be positioned at the provided coordinate pair PLUS the current SCRLX and SCRLY (x + SCRLX, y + SCRLY). Dropshadow argument controls the x and y offset of the dropshadow (0,0 does not render)
#### blit_pivot_center(self,window:pygame.Surface,xy:tuple[int,int],pivot:tuple[int,int],angle:float,dropShadow:tuple[int,int]=(0,0))
Blits the targeted sprite onto the given surface. The center of the sprite will be positioned at the provided coordinate pair PLUS the current SCRLX and SCRLY (x + SCRLX, y + SCRLY). The sprite will be rotated around the coordinate point of the “pivot” argument by **COUNTERCLOCKWISE** by the number of degrees represented by the “angle” argument. Dropshadow argument controls the x and y offset of the dropshadow (0,0 does not render)

#### updateSheet(self)
Updates the active sprite in the spritesheet. This function should be used in the game loop and, in most cases, should be updated every frame. By changing the “sheetAnimMS” value it will change how long (in ms) it takes for each frame of the sprite to update

#### testColl(self,otherSprite,pos:tuple[int,int]=None,otherSpritePos:tuple[int,int]=None) -> bool
Tests to see if the sprite collides with another sprite 
(must be gregium.sprite type),
if either pos argument is not supplied it will use the most 
recent position blitted by the sprite as the position 
(scroll is taken into account)
#### testCollR(self,*otherRects:pygame.Rect,pos:tuple[int,int]=None) -> bool
Tests to see if the sprite collides with any other rects 
(must be pygame.Rect type)
if the pos argument is not supplied it will use the most 
recent position blitted by the sprite as the position 
(scroll is taken into account)

#### scale(self,scale:float=None,width:float=None,height:float=None) -> 1
Scales the sprite by scale argument factor, there should be only 1 input unless you are changing both width and height (don't do scale & width or scale & height it will not work correctly) If either width or height is blank it is assumed to use automatic and will scale based on the other changed value

### ziphandle
#### zipFolder(folder:str,zipPath:str) -> None
Zips a folder given by the path of zipPath without using recursion.

### events
A class storing all the events, call gregium.events.[event name here] to get an event
#### clearEvent()
Resets all events to default values (use before event loop)
#### supplyEvent(event:pygame.event.Event)
Updates gregium’s event object with pygame events. Events supplied must be from elements returned by pygame.event.get(). For instance, simply use <for event in pygame.event.get()> and call this function with <event> as an argument.
onPress(key)
Module only function, binds all keypresses and events to a respective value
keyHandler()
Module only function, catches all key press events to be processed by on_press funciton

### button(pos:tuple[float,float],size:tuple[float,float],color:tuple[int,int,int]=(255,255,255),outline:tuple[int,int,int]=(0,0,0),outlineThick:int=5,suppliedFont:Font=None,text:str="",textCol:tuple[int,int,int]=(0,0,0),textSize:int=25,colorHighlight:tuple[int,int,int]=(200,200,200),outlineHighlight:tuple[int,int,int]=(55,55,55),align:str="topLeft",rounding:int=0)
Generates a simple button. The following arguments can be provided to customize the button:
- pos: a tuple that determines the (x, y) coordinates of where to place the top left corner of the button.
- size: a tuple that determines the width and height of the button, respectively.
- color: an RGB tuple that fills the button with the given RGB color. Defaults to (255, 255, 255), which is white.
- outline: an RGB tuple that fills the button’s border with the given RGB color. Has no effect if outlineThick is zero, i.e. there is no border.
- outlineThick: an integer that determines the thickness of the button’s border in pixels. Defaults to five (5) pixels.
- suppliedFont: a Font object that should be set up with gregium’s Font instantiator. Defaults to None, which will load the SpaceMono font.
- text: a string that represents text inside the button. By default, there is no text.
- textCol: an RGB tuple that specifies what color the text should be. Defaults to (0, 0, 0), which is black.
- textSize: an integer that represents the size of the text in standard text size (1/72th of an inch equals 1 text size point).
- colorHighlight: an RGB tuple that fills in the background of only the text with the provided RGB color. Defaults to (200, 200, 200), which is gray.
- outlineHighlight: an RGB tuple that fills the outline of the text with the given RGB color. Defaults to (55, 55, 55), which is dark gray.
- align: a string that specifies how the text should be aligned within the button.
- rounding: acts as a border radius for the button. The number assigned to rounding is proportional to the curvature of the button.
#### render(self)
Renders a button and returns an int from 0-3 representing the following:
        0: no collision
        1: mouse hovers over the button
        2: mouse clicked on collision (pressed up and down)
        3: mouse only pressed down on collision
### defaultButtonRender(self:button):
The default rendering for a gregium button, 
    any alternatives must change BUTTONRENDERFUNC and have 1 
    argument (name can be anything) and will pass in the button class
### textBox(self,pos:tuple[float,float],size:tuple[float,float],color:tuple[int,int,int]=(255,255,255),outline:tuple[int,int,int]=(0,0,0),outlineThick:int=5,suppliedFont:Font=SPACEMONO,text:str="",textCol:tuple[int,int,int]=(0,0,0),textSize:int=25,colorHighlight:tuple[int,int,int]=(200,200,200),outlineHighlight:tuple[int,int,int]=(55,55,55),align:str="topLeft",maxTextLength:int=-1,rounding:int=0)
Generates a simple text box. The following arguments can be provided to customize the text box:
- pos: a tuple that determines the (x, y) coordinates of where to place the top left corner of the text box.
- size: a tuple that determines the width and height of the text box, respectively.
- color: an RGB tuple that fills the text box with the given RGB color. Defaults to (255, 255, 255), which is white.
- outline: an RGB tuple that fills the text box’s border with the given RGB color. Has no effect if outlineThick is zero, i.e. there is no border.
- outlineThick: an integer that determines the thickness of the text box’s border in pixels. Defaults to five (5) pixels.
- suppliedFont: a Font object that should be set up with gregium’s Font instantiator. Defaults to None, which will load the SpaceMono font.
- text: a string that represents text inside the text box. By default, there is no text.
- textCol: an RGB tuple that specifies what color the text should be. Defaults to (0, 0, 0), which is black.
- textSize: an integer that represents the size of the text in standard text size (1/72th of an inch equals 1 text size point).
- colorHighlight: an RGB tuple that fills in the background of only the text with the provided RGB color. Defaults to (200, 200, 200), which is gray.
- outlineHighlight: an RGB tuple that fills the outline of the text with the given RGB color. Defaults to (55, 55, 55), which is dark gray.
- align: a string that specifies how the text should be aligned within the text box.
- maxTextLength: an integer that limits how many characters a user can type into the text box.
- rounding: acts as a border radius for the text box. The number assigned to rounding is proportional to the curvature of the text box.
#### render(self)
Renders a text box and updates its text if the user has hit enter and has started typing in it. render() also enforces a maximum text length, disallowing the user to type more than the limit provided.

### alertBox(suppliedFont:Font,buttons:tuple=("ok",),title:str=None,color:tuple[int,int,int]=(0,0,0),outline:tuple[int,int,int]=(255,255,255),textCol:tuple[int,int,int]=(255,255,255))
Generates an alert box with supplied buttons. The following arguments can be utilized to customize the alert:
- suppliedFont: a gregium Font object that alters the font of alert text.
- buttons: a tuple with as many strings as desired, strings will be converted to buttons and spread horizontally across the box, if the amount of buttons is only 1, use (‘buttonText’,) as opposed to (‘buttonText’) to prevent errors in generation. These buttons will be - displayed on the alert as options to click on. An example of buttons that can be added are “Accept” or “Deny” buttons.
- title: a string containing the title that will be displayed on the alert. The alert’s title can be multi-line if \\n is put in the string. Defaults to None.
- color: an RGB tuple that will fill the background color of the entire alert box with that RGB color. Defaults to (0, 0, 0), which is white.
- outline: an RGB tuple of the outline of the alert box. Defaults to (255, 255, 255), which is black.
- textCol: an RGB tuple that will change the text color using that RGB color. Defaults to (255, 255, 255), which is black.
#### render(self)
Renders an alert with the previously provided buttons. Returns the pressed button if one is clicked. Returns 0 if no buttons are pressed.

### cmdParseSeg(segment:str,requestedType:str,min="N/A",max="N/A")
A function for parsing strings, integers, floats, and json.
In the case of a string, the function removes double-quotes.
In the case of an int or float, the function makes sure that the value is within the interval [min, max].
In the case of JSON, the function converts the JSON into a usable python object.

### CLI(tree:dict={})
Make easy command-line interpreters that can be used outside or inside the terminal.

#### addCmd(self,commandDict:dict)
Add a new command! Syntax is as follows
        

{ 
"name":
      {
"root": {"type": "*", "var": "test", "next": "foo"},
"foo":{"type": "*", "var": "test2", "next": "etc"} 
      }
}

Types include, str, json, int, float, literal, func
int & float can have a minumim/maximum value provided
literals must have a list of outputs
Func must have a "run" key instead of next and var and the "run" key must have the function as its value.
        You can input multiple commands as well. In the syntax example above, only one is provided, that being “name”. Add a comma and another object with the contents of the command. Repeat commands will not get overwritten; instead, they will throw an error.
#### helpcmd(self,*args)
Generates a help message for commands. If no arguments are provided, calling helpcmd simply returns a list of all existing commands. To return with help for a specific command, pass the name of the command as an argument when calling helpcmd.
#### run(self,cmd:str) -> tuple[int,str]
Reads a full command from a string, which should be the name of the commands. Calling this function returns one of two exit codes: 
(error, return) on error
(0, return) on success
stop()
Properly stops the gregium engine.

