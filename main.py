# Use for testing functions
import gregium,pygame
import gregium.editor

# Declare a pygame window and initialize gregium
WINDOW = pygame.display.set_mode([1000,1000],pygame.NOFRAME)
gregium.init()

# Declare a gregium font and textBox

EDITOR_FONT_MAIN = gregium.Font.from_file(gregium.PATH+"\\editor\\Space_Mono\\SpaceMono-Regular.ttf")
BOX = gregium.textBox((-500,-50),size=(1000,100),suppliedFont=EDITOR_FONT_MAIN,text="yay!",align="center")

# Main loop
while not gregium.events["quit"]:

    # Refills window with black background
    WINDOW.fill((0,0,0))

    # Update gregium events
    gregium.clearEvent()
    for event in pygame.event.get():
        gregium.supplyEvent(event)

    # If enter is hit, detect typing and change box text accordingly
    if BOX.render() == "ENTER":
        print(f"enter hit! text: {BOX.text}")
    pygame.display.flip()

# Close gregium on quit
gregium.stop()