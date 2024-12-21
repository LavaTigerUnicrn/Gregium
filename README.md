# ![gregiumNameHD](https://github.com/user-attachments/assets/bf3c96d2-e1aa-4117-91cb-93d896145211)

[![Pypi](https://img.shields.io/badge/pypi-v0.1.9-%233775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/gregium)
[![Github](https://img.shields.io/badge/github-0.1.9-%23181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/LavaTigerUnicrn/Gregium)
[![License](https://img.shields.io/badge/license-MIT-%233DA639?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://opensource.org/license/MIT)

> Basic readme of the Gregium library, for detail instructions see help of modules or classes

## Table of Contents

- [Table of Contents](#table-of-contents)
- [buttons](#buttons)
- [camera](#camera)
- [commandSystem](#commandsystem)
- [env](#env)
- [gambleCore](#gamblecore)
- [imports](#imports)
- [old](#old)
- [terminalLogging](#terminallogging)

## buttons

> Adds extra buttons not found in pyglet, such as push buttons from rects and text entry with borders

**Classes**  

- **PushButtonRect** - Istance of a push button based on a rect.
- **ToggleButtonRect** - Instance of a toggle button based on a rect.
- **SliderRect** - Instance of a slider made of a base and a knob rect.
- **BorderedTextEntry** - Instance of a text entry widget. Allows the user to enter and submit text.
- **MouseDistanceDetector** - Creates a widget that detects the mouse distance at any given position; it is reccomended to not have this in a frame so it's able to detect distance no matter what

## camera

> Camera class for easy scrolling and zooming.

**Classes**  

- **Camera** - A simple 2D camera that contains the speed and offset.
- **CenteredCamera** - A simple 2D camera class. 0, 0 will be the center of the screen, as opposed to the bottom left.

---

## commandSystem

> The original 'CLI' class in gregium

**Classes**  

- **CommmandSystem** - Make easy command interpreters that can be used outside, or inside terminal

---

## env

> The original module for loading an saving .grg (ENV) files

**Functions**  

- **load** - Loads ENV from .grg file using a path

---

## gambleCore

> Gambling

**Classes**  

- **Gambler** - A gambler that can communicate with GameInst's to bet chips on it
- **GameBase** - Base class for all gambling games
- **GameInst** - Base class for allgambling game instances
- **BlackjackInst** - Created by Blackjack table
- **Blackjack** - A Blackjack table for gambling
- **Casino** - A casino base capable of monitoring losses per table, dealing out chips, and more

---

## imports

> Additional tools for importing libraries

**Functions**  

- **import_from_file** - Imports a module by filename and returns the module instance

## old

> The (old) core of Gregium

See gregium.old README for specific guildlines

---

## terminalLogging

> An easy terminal logger capable of also saving to a file and timestamping

**Classes**  

- **Logger** -Generates a basic terminal logger

**Globals**  

- **PRIMARY** - The primary logger used in other gregium libraries
