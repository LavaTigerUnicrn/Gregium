
# Changelog

A list of *almost* all changes made from versions 2.2.0 onward

Changes are formatted into sections of Changes, Fixes

Additionally, found at the bottom, are upcoming Planned (changes), and (known) Bugs

Within each they are categorized by which module they pertain to

## Versions

- 2.2
  - [2.2.0](#220)
  - [2.2.1](#221)
  - [2.2.2](#222)
- 2.3
  - [2.3.0](#230)
- [Upcoming](#upcoming)

## 2.2.0

### Changes

- Removed random main.py file
- Moved all single-file modules out of their own folders (names are preserved)
- Removed example code (examples coming to wiki)

#### AI

- Removed generic 'ai' folder and moved AI functions into their own sections
  - AI/LLM is now LLM
  - AI/TTS is now TTS
  - AI/STT is now STT

#### ASCII Render

- Huge performance improvement for loading images and rendering

#### G-HTTP

- G-HTTP no longer automatically assumes an encoding to decode responses
- G-HTTP puts cookie in a specific property of class and not only in generic headers
- Added more return types for G-HTTP Returns being 'file' 'ok' and 'byte'
- Added automatic loading for cookies when receiving from client and methods to get data from webforms

#### Library Checker (D)

- Removed in place of Verification

#### LLM

- Remade LLM structure to lint better and make more sense

#### Logging

- Mostly removed Gregium logging in place of standard logging
  - Existing logging module now has controls for formatting existing logger for stdout or file and adding custom colors

#### Misc

- Allowed for changing the character to use for loading bars
- Gave more helpful error messages for missing specs when loading a module
- Added function to recursively list all items in a directory
- Changed names from "interp" to "interpolate" in color interpolation functions
- Made more extensive progress bars

#### RealTimeSTT (R)

- Removed due to slow speed and inaccuracy

#### Server

- Rewrote server to better support multiple clients and be more similar to G-HTTP protocol

#### Settings (D)

- Dissolved settings
  - Settings now found in the given module and can be changed with functions within them
  - Still make sure to put secure values in a .env file (just not auto-loaded)

#### Terminal

- Uses blessed for most terminal inputs
- Added a terminal-specific way of rendering progress bars similar to misc

#### TTS

- Prevent program from crashing when missing tts_with_rvc
- Changed voice list to a more correct version
- Changed method of playing audio to allow for pygame.mixer.music to still be used
- Added function to stop queue threads
- Removed models folder

#### Verification

- Created to give users more control over packages to install and be usable elsewhere

### Fixes

- Fixed incorrect typing (mostly)

#### TTS

- When making multiple Queue objects or when having >512 consecutive audio instances awaiting playing, audio files will no longer collide

#### Command Tree

- Fixed command tree help command, added tracing, and fixed error handling

#### G-HTTP

- Fixed issue where HTTP would always request one more byte than needed and miss partial large packets
- Fixed G-HTTP server to no longer abort connection when editing \_post or \_get methods and having an error
- Redirects in G-HTTP are no longer cached meaning that redirects will not continue to take affect even when structure changes
- Added PATCH, PUT, OPTIONS, TRACE, and HEAD (CONNECT will not be added)
- Added HTTPS protocol

#### Json-Matcher

- Fixed issue with dictionary paths being formatted using os.path.pardir

## 2.2.1

### Fixes

- LLM Functions erroneously included nonexistent arguments in docstring

## 2.2.2

### Changes

#### Engine (D)

- Removed engine (moved vectors to dedicated file)

#### LLM

- Moved severity of tooling running to INFO

#### JSON Matcher

- Added setitem dunder method

#### Vector

- Changed function names to make more sense and added some additional functions
- Added dunder methods for all standard operations
- Added higher dimension Vectors

### Fixes

#### LLM

- Added 'Role' type to the standard init file, allowing for use in sub-ChatBots
- Fixed type of 'add_tool' function
- Fixed issue where running 'run_tools' would not clear the tool queue
- Fixed issue where bot messages on Ollama bot would not be saved causing the bot to go into an infinite loop

#### JSON Matcher

- 'Value' parameter of 'set' function now reflects the allowed 'Any' and not just 'str'
- Clears JSON file instead of raising global exception when loading

## 2.3.0

### Changes

- Created docs
- Rewrote most docstrings

#### Command Tree

- Improved parsing, error checking, and type checking

#### LLM

- tool_loader now uses ollama library tool loading

#### Markdown (D)

- Merged into misc under name "format_md"

#### Vector

- Added method `from_polar`
- Vector2, Vector3, and Vector4 now are generators for a standard Vector and not a type

#### Verification

- Fixed pip install command when installing multiple modules with `check_all`

## Upcoming

### Planned

#### TTS

- Rewrite for more coherence, speed, and stability

#### JSON Matcher

- Adding support for lists (arrays) in JSON schemas in matcher
- Rewrite for better stability and functions

### Bugs

**[Report any issues found here](https://github.com/LavaTigerUnicrn/Gregium/issues)**

- None currently known of
