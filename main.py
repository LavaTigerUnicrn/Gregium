#Use for testing functions
import gregium,pygame

# Open pygame window, initialize gregium
WINDOW = pygame.display.set_mode([1000,1000],pygame.NOFRAME)
CLOCK = pygame.Clock()

gregium.init(CLOCK)

# Initialize a gregium Font and textBox
BOX = gregium.textBox((-500,-50),size=(1000,100),text="yay!",align="center",rounding=15)

# Generate SPRITESHEETOBJ
SPRITESHEETOBJ = gregium.Sprite(gregium.PATH+"/gregiumAnimHD.png",(6,3))
SPRITESHEETOBJ.width,SPRITESHEETOBJ.height,SPRITESHEETOBJ.sheetAnimMS = 300,300,50

# Generate SPRITEOBJ
SPRITEOBJ = gregium.Sprite(gregium.PATH+"/gregiumHD.png")
SPRITEOBJ.width,SPRITEOBJ.height = 50,50
SPRITEOBJ.updateImage()
SPRITEOBJ.scrollModif = 0

bignum = 0
pygame.mouse.set_visible(False)

# Main loop
while not gregium.events.quit:

    # Fill the canvas with black
    WINDOW.fill((50,50,50))

    # Update gregium events
    gregium.events.clearEvent()
    for event in pygame.event.get():
        gregium.events.supplyEvent(event)

    # Scroll bye bye
    gregium.SCRLX += 1

    if SPRITESHEETOBJ.testColl(SPRITEOBJ):
        coll = (0,255,0)
    else:
        coll = (255,0,0)
    # Render SPRITESHEETOBJ
    SPRITESHEETOBJ.rotation += 0.01*CLOCK.get_time()
    SPRITESHEETOBJ.updateSheet()
    SPRITESHEETOBJ.updateImage()
    SPRITESHEETOBJ.blit_center(WINDOW,(SPRITESHEETOBJ.width/2,SPRITESHEETOBJ.height/2))

    # Render SPRITEOBJ
    SPRITEOBJ.blit_center(WINDOW,gregium.events.mousePos)

    pygame.draw.rect(WINDOW,coll,SPRITESHEETOBJ.imageBlitRect,5)
    pygame.draw.rect(WINDOW,coll,SPRITEOBJ.imageBlitRect,5)

    # Render KeysPressed
    gregium.SPACEMONO.blit_center(str(gregium.events.heldKeys),gregium.alignPos((0,100),"center"))
    bignum = max(bignum,CLOCK.get_fps())
    gregium.SPACEMONO.blit_center(str(bignum),gregium.alignPos((0,300),"center"))

    # If enter is pressed, detect typing and change the text in the textBox accordingly
    if BOX.render() == "ENTER":
        print(f"enter hit! text: {BOX.text}")

    # Render SPRITEOBJ
    SPRITEOBJ.blit_center(WINDOW,gregium.events.mousePos)

    # Update the window
    pygame.display.flip()
    CLOCK.tick(60)

# Stops gregium on quit
gregium.stop()