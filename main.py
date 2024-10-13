#Use for testing functions
import gregium,pygame,gregium.editor

# Open pygame window, initialize gregium
WINDOW = pygame.display.set_mode([1000,1000],pygame.NOFRAME)
gregium.init()

# Initialize a gregium Font and textBox
BOX = gregium.textBox((-500,-50),size=(1000,100),text="yay!",align="center",rounding=15)

# Main loop
while not gregium.events["quit"]:

    # Fill the canvas with black
    WINDOW.fill((0,0,0))

    # Update gregium events
    gregium.clearEvent()
    for event in pygame.event.get():
        gregium.supplyEvent(event)

    print(gregium.events["heldKeys"])

    # If enter is pressed, detect typing and change the text in the textBox accordingly
    if BOX.render() == "ENTER":
        print(f"enter hit! text: {BOX.text}")

    # Update the window
    pygame.display.flip()

# Stops gregium on quit
gregium.stop()