#Use for testing functions
import gregium,pygame,gregium.editor

# Open pygame window, initialize gregium
WINDOW = pygame.display.set_mode([1000,1000],pygame.NOFRAME)
gregium.init()

# Initialize a gregium Font and textBox
BOX = gregium.textBox((-500,-50),size=(1000,100),text="yay!",align="center",rounding=15)

SPRITESHEETOBJ = gregium.Sprite(gregium.PATH+"/gregiumAnimHD.png",(6,3))
SPRITESHEETOBJ.width,SPRITESHEETOBJ.height,SPRITESHEETOBJ.sheetAnimTicks = 300,300,5

CLOCK = pygame.Clock()

# Main loop
while not gregium.events["quit"]:

    # Fill the canvas with black
    WINDOW.fill((0,0,0))

    # Update gregium events
    gregium.clearEvent()
    for event in pygame.event.get():
        gregium.supplyEvent(event)

    # Render SPRITESHEETOBJ
    SPRITESHEETOBJ.updateSheet()
    SPRITESHEETOBJ.updateImage()
    SPRITESHEETOBJ.blit(WINDOW,(1,1))

    # If enter is pressed, detect typing and change the text in the textBox accordingly
    if BOX.render() == "ENTER":
        print(f"enter hit! text: {BOX.text}")

    # Update the window
    pygame.display.flip()
    CLOCK.tick(60)

# Stops gregium on quit
gregium.stop()