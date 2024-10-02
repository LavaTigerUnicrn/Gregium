"""
A basic editor for convenient navigation in Gregium
"""

import pygame
import gregium.env
import gregium
import sys

EDITPATH = gregium.PATH+"\\editor\\"
gregium.env.load(EDITPATH+"editor.grg",ignoreCWD=True)
ENV = gregium.env.ENV

def main():
    EDITOR_WINDOW = pygame.display.set_mode(ENV["WINDOW_SIZE"],pygame.RESIZABLE)
    EDITOR_WINDOW_SCALE = ENV["WINDOW_SIZE"]
    gregium.init()

    EDITOR_FONT_MAIN = gregium.Font.from_file(EDITPATH+"\\Space_Mono\\SpaceMono-Regular.ttf")

    IS_ACTIVE = True

    FORCE_NOT_QUIT = False
    NOT_QUIT_QUEUE = 0

    CLOCK = pygame.time.Clock()

    CONFIRM_ALERT = gregium.alertBox(suppliedFont=EDITOR_FONT_MAIN,buttons=("Yes","No"),title="title not set")

    ALERT = gregium.alertBox(suppliedFont=EDITOR_FONT_MAIN,buttons=("Ok",),title="title not set")

    while IS_ACTIVE:
        EDITOR_WINDOW.fill((0,0,0))
        if NOT_QUIT_QUEUE < 0:
            NOT_QUIT_QUEUE = 0
        gregium.clearEvent()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if FORCE_NOT_QUIT:
                    isChoosing = True
                    ALERT.title = "Quitting is not \navailable at this moment"
                    while isChoosing:
                        EDITOR_WINDOW.fill((0,0,0))
                        gregium.clearEvent()
                        for event in pygame.event.get():
                            gregium.supplyEvent(event)
                        if ALERT.render() == "Ok":
                            isChoosing = False
                        pygame.display.flip()

                        CLOCK.tick(ENV["MAX_FPS"])
                elif NOT_QUIT_QUEUE == 0:
                    isChoosing = True
                    CONFIRM_ALERT.title = "Are you sure you\nwant to quit?"
                    while isChoosing:
                        EDITOR_WINDOW.fill((0,0,0))
                        gregium.clearEvent()
                        for event in pygame.event.get():
                            gregium.supplyEvent(event)
                        match CONFIRM_ALERT.render():
                            case "Yes":
                                IS_ACTIVE = False
                                isChoosing = False
                            case "No":
                                isChoosing = False
                        pygame.display.flip()
                else:
                    isChoosing = True
                    CONFIRM_ALERT.title = "Are you sure you\nwant to quit?\nSome things may be \ninterrupted"
                    while isChoosing:
                        EDITOR_WINDOW.fill((0,0,0))
                        gregium.clearEvent()
                        for event in pygame.event.get():
                            gregium.supplyEvent(event)
                        match CONFIRM_ALERT.render():
                            case "Yes":
                                IS_ACTIVE = False
                                isChoosing = False
                            case "No":
                                isChoosing = False
                        pygame.display.flip()
            gregium.supplyEvent(event)
        
        pygame.mouse.set_system_cursor(0)

        pygame.display.flip()

        CLOCK.tick(ENV["MAX_FPS"])

    gregium.stop()