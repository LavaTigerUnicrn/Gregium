#Use for testing functions
import gregium,pygame

WINDOW = pygame.display.set_mode([1000,1000],pygame.NOFRAME)
gregium.init()

EDITOR_FONT_MAIN = gregium.Font.from_file(gregium.PATH+"\\editor\\Space_Mono\\SpaceMono-Regular.ttf")
BOX = gregium.textBox((-500,-50),size=(1000,100),suppliedFont=EDITOR_FONT_MAIN,text="yay!",align="center")
while not gregium.events["quit"]:
    WINDOW.fill((0,0,0))

    gregium.clearEvent()
    for event in pygame.event.get():
        gregium.supplyEvent(event)

    if BOX.render() == "ENTER":
        print(f"enter hit! text: {BOX.text}")
    pygame.display.flip()

gregium.stop()