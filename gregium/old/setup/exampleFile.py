# Import Libs
import pygame,gregium

# Set up Window and Clock
WINDOW = pygame.display.set_mode([1920,1080],pygame.RESIZABLE|pygame.DOUBLEBUF)
CLOCK = pygame.Clock()

# Pass value to gregium
gregium.init(CLOCK)

### PUT GLOBALS HERE ###

# Event Loop
while True:

    # Clear Screen
    WINDOW.fill((0,0,0))

    # Reset events
    gregium.events.clearEvent()

    # Event Loop
    for event in pygame.event.get():

        # Give events to gregium
        gregium.events.supplyEvent(event)

    # If quit was hit then exit
    if gregium.events.quit:
        gregium.stop()

    ### PUT RENDERING HERE ###

    # Flip diplay and tick clock
    pygame.display.flip()
    CLOCK.tick(60)