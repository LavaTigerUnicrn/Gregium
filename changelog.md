
# Changelog

A list of *almost* all changes made from versions 2.2.0 onward

Changes are formatted into sections of Changes, Fixes

Additionally at the bottom contain upcoming Planned (changes), and (known) Bugs

Within each they are categorized by which module they pertain to

## Versions

- [2.2.0](#220)

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

## Upcoming

### Planned

- Making wiki

#### Engine

- Making the engine

#### JSON Matcher

- Adding support for lists (arrays) in JSON schemas in matcher

### Bugs

**[Report any issues found here](https://github.com/LavaTigerUnicrn/Gregium/issues)**

- None currently known of
