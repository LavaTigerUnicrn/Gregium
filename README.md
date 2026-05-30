# ![gregiumNameHD](https://github.com/user-attachments/assets/bf3c96d2-e1aa-4117-91cb-93d896145211)

[![PyPi](https://img.shields.io/badge/pypi-v2.1.1-%233775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/gregium)
[![Github](https://img.shields.io/badge/github-2.1.1-%23181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/LavaTigerUnicrn/Gregium)
[![License](https://img.shields.io/badge/license-MIT-%233DA639?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://opensource.org/license/MIT)
[![Discord](https://img.shields.io/badge/discord-LTU-%235865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/SeKhDF4m5W)
[![Wiki](https://img.shields.io/badge/wiki-informational?style=for-the-badge&logo=gitbook&logoColor=white)](https://github.com/LavaTigerUnicrn/Gregium/wiki)

> Completely remade and ready to not work when you need it most

## Table of Contents

- [AI](#ai)
  - [LLM](#llm)
  - [TTS](#tts)
  - [STT](#stt)
- [ASCII](#ascii)
- [Commands](#commands)
- [Engine](#engine)
- [Logger](#logger)
- [Markdown](#markdown)
- [Misc](#misc)
- [Server](#server)
- [Settings](#settings)
- [Terminal](#terminal)
- [Library Checker](#library-checker)

## Quick Start

You first need to install Gregium to use Gregium.
This shouldn't come as a surprise as it doesn't magically appear on your computer.

Install Command:

> pip install gregium

To run Gregium testing examples, simply use

> python -m gregium

For an interactive test through all the Gregium functions

## Version Conflicts

Gregium has an automatic version conflict resolver called "library_checker"

In the case where you get any issues with packages on Gregium, use

> python -m gregium --verify

To automatically check for libraries

## Help

If you need help on anything, have ideas, or found any bugs with Gregium feel free to join the [Discord](https://discord.gg/SeKhDF4m5W) for assistance or submit an issue to the repository

## AI

An easy way to interface with various types of AI

### LLM

Easy LLM using `ChatBot` that allows for interface of Ollama and HuggingFace.

#### Ollama

> Make sure [Ollama](https://ollama.com) is installed before using this.
> Note that Ollama is locally hosted and may have large resource usage on lower-end devices.

```python
from gregium.ai.llm import Ollama_ChatBot

# Set the model (otherwise will use Gregium default)
MODEL_NAME = "gregium3.3:latest"

# Generate the bot
bot = Ollama_ChatBot(MODEL_NAME)

# Setup query (tell returns no response)
bot.tell("Say the meaning of a sentence given by the user",role="system")

# Chat with bot (chat returns response from bot)
output = bot.chat("To be or not to be, that is the question.")

print(output)
```

#### HuggingFace

> Make sure the environment variable `HF_TOKEN` is set and loaded before using.
> Get a HuggingFace token at [HuggingFace token](https://huggingface.co/settings/tokens).
> Note that not all HuggingFace models will work and using online HuggingFace models have a limit of free prompts.

```python
from gregium.ai.llm import HF_ChatBot

# Set the model (find under deploy tab on a HuggingFace model)
MODEL_NAME = "Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway"

# Generate the bot
bot = HF_ChatBot(MODEL_NAME)

# Setup query (tell returns no response)
bot.tell("Say the meaning of a sentence given by the user",role="system")

# Chat with bot (chat returns response from bot)
output = bot.chat("To be or not to be, that is the question.")

print(output)
```

#### Additional AI Tools

Many AI models support "tools" (basically just calling a function through the AI), Gregium allows for automatic parsing of most tools and automatically calls them as well

> Note that some models may have issues if sending content and tool calls at the same time

Gregium has a list of already pre-made tools for various actions, such as search queries or time getting (these can be buggy and should be used more a proof of concept)

```python
from gregium.ai.llm import ChatBot
from gregium.ai.ai_tools import add_all_tools

# Set the model (otherwise will use Gregium default)
MODEL_NAME = "gregium3.3:latest"

# Generate the bot
bot = ChatBot(MODEL_NAME)

# Add tools to bot
add_all_tools(bot)

# Ask the bot to use time tool
output = bot.chat("What is the current time?")

print(output)
```

If you wish to use a different AI provider not found on HuggingFace or Ollama, you can use `gregium.ai.llm.tool_loader` `func_from_annotation` function in order to easily parse a function to be run by most AI models

### STT

Fast and efficient STT using [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT)

> Note that Gregium only adds ease of use functions, not any recorder bindings themselves

```python
import gregium.ai.stt as stt

# You must run in main to not get an error
if __name__ == "__main__":

    # Make a new recorder 
    # (this will automatically use the user language if not set)
    recorder = stt.generate_recorder()

    # Wait for the use to say "hello"
    message = stt.wait_word(recorder,"hello")

    # Print out message
    print(message)

```

### TTS

Threaded queues of Edge-TTS and RVC models

#### Edge-TTS

> Note that Edge-TTS is not guaranteed to work all of the time

```python
from gregium.ai.tts import Queue,dispatch_checker_thread
import time

# Generate queue (if not voice is set will use Gregium default)
queue = Queue()

# Start queue threading (to check generation and play)
dispatch_checker_thread(queue)

# Queue text
queue.generate("Hello, World!")

# Wait for queue to be done
while not queue.has_completed():
    time.sleep(1)
```

#### RVC

> Note that RVC can be slow and use high GPU cost

```python
from gregium.ai.tts import load_model,dispatch_checker_thread
import time

# Generate queue (voice is Gregium default)
# Model must be found in models folder
# models/{model_name}/{model_name}.pth
# models/{model_name}/{model_name}.index
# Index is not required but helps make it sound better
queue = load_model("test")

# Start queue threading (to check generation and play)
dispatch_checker_thread(queue)

# Queue text
queue.generate("Hello, World!")

# Wait for queue to be done
while not queue.has_completed():
    time.sleep(1)
```

## Ascii

Allows for rendering ASCII to the terminal.

> Note that on windows is may be somewhat odd behavior on certain terminals

### Rendering

```python
import gregium.ascii_render as render

# Generate window
WINDOW = render.display.set_mode(250,250)

# Load image
url = "https://github.com/user-attachments/assets/bf3c96d2-e1aa-4117-91cb-93d896145211"
image = render.image.load_web(url)

# Scale and rotate image
image = render.transform.scale(image,(100,100))
image = render.transform.rotate(image,45)

# Trim image
image = render.transform.auto_trim(image)

# Blit image
WINDOW.blit(image,(0,0))

# Flip (safe is slower but works on CMD prompt)
render.display.write_flip_safe()
```

### Raw Render

Raw render is faster but with less definition.

> Only supports render from pygame surface

```python
import gregium.ascii_render.raw_render as render
import pygame
pygame.init()

# Make red surface
surf = pygame.Surface()
surf.fill((255,255,255))

# Render
render.render_pygame(surf)
```

## Commands

A tree of commands that can be called using shell notation.

```python
import gregium.command_tree as tree

# Generate new tree
cmd_tree = tree.CommandTree()

# Make a custom function
def add_numbers(a:int, b:int):
    """
    Adds numbers
    """

    return a + b

# Add to tree
cmd_tree.add_command(add_numbers)

# Call tree
output = cmd_tree("add_numbers 3 --b 4")

# 7
print(output)

```

## Engine

> Engine is a WIP, use at your own risk

## Logger

An alternate to logging that allows for file logging or stdout logging with colorations.

```python
import gregium.logger as logger
from gregium.logger.basic_logs import *

# Set logger to output to stdout
logger.set_stdout()

# Log different items
info("Hello",__name__)
warn("Test",__name__)
error("Three",__name__)
debug("Debug message",__name__)
critical("Program is stopped",__name__)
```

## Markdown

Partial support of markdown tags in Gregium

> Uses Discord-like syntax for underscores

Supports:

- ~~Strikethrough~~ (~~)
- **Bolding** (**)
- *Italicization* (*)
- ***Bold & Italicization*** (***)
- <u>Underline</u> (__)
- `Blocks` (`)

```python
import gregium.markdown as md

text = md.format("**bold** *italicize* ***bold & italicize*** ~~strikethrough~~ __underscore__ `block`")

```

> **bold** *italicize* ***bold & italicize*** ~~strikethrough~~ <u>underscore</u> `block`

## Misc

Quite a few random functions that may come in handy in certain programs.

Functions:

- colorAscii : Colors a pixel in Ascii terminal
- open_terminal : Opens terminal on Windows
- loading_bar : Ascii loading bar
- loading_bar_adv : Advanced loading bar with time tracking and estimations
- import_absolute : Imports a module from a file path

```python
import gregium.misc as misc

# Make a red half completed loading bar
print(misc.loading_bar(10,0.5,(255,0,0)))

# Color a pixel light blue
print(misc.colorAscii((50,127,255))+"@")

# Reset terminal color
print("\x1b[0m",end="")

```

## Server

Socket server hosting with significantly more user-friendly syntax and efficient sending.

> The server should be started before running the client

```python
# client.py
import gregium.server as server

port = 8000

# Generate client (automatically uses host IP)
client = server.Client(port)

# Connect to server
client.connect()

# Send and recv
client.send("Hello, server!")

# Get starting info (sends gregium version)
print(client.recv())

# Get server sent packet
print(client.recv())
```

```python
# server.py
import gregium.server as server

port = 8000

# Generate server (automatically uses host IP)
host = server.Server(port)

# Look for client
print("Waiting for Client")
host.host()

# Send and recv
host.send("Hello, client!")

# Get starting info (sends gregium version)
print(host.recv())

# Get client sent packet
print(host.recv())
```

## Settings

Stores settings found in Gregium. Use `gregium.settings` to reference setting values.

For custom settings use `gregium.settings_helper.Settings` object

> Use `python -m gregium.settings_helper` or `python -m gregium` to edit settings

```python
import gregium.settings as settings

# Prints out the default Ollama model
print(settings.DEFAULT_MODEL)
```

## Terminal

Automatic inputs that work on both NT (Windows) and POSIX (Linux & Mac) terminals for almost all keys

> Some keys may not be recognized properly on certain terminals

**MAKE SURE TO RUN** `pip install blessed` **ON WINDOWS**

```python
import gregium.terminal.inputs as inputs

# Start inputs
inputs.start()

# Make options
options_dict = {
    1:{"name":"One","desc":"The first number"},
    2:{"name":"Two","desc":"The second number"},
    3:{"desc":"The third number"},
    4:{"name":"Four","desc":"The fourth number"},
    5:{"name":"Five"}
}

# Load the options
options = inputs.options_from_dict(options_dict)

# Make the user choose an option
chosen = inputs.choice(**options)

# Print out the chosen
print(chosen)

# End inputs
inputs.end()
```

## Library Checker

Checks all the modules installed to make sure they are compatible with Gregium

> Use at your own risk, this will overwrite all installed packages

```python
from gregium.library_checker import verify_lib
import gregium.logger as logger

# Change logging
logger.set_stdout()

# Verify
verify_lib()
```
