"""
Text-To-Speech Queues for Edge-TTS

**These will not work properly if you are already playing sound via the pygame.mixer.music (as they use the same audio pipe)**

If none of these work, try `RealtimeTTS`
"""
# Import libraries
import asyncio
import logging
import os
import threading
import time

from ..verification import verify_exists

verify_exists("edge_tts","edge-tts")
verify_exists("pygame","pygame-ce")

import edge_tts
import pygame

pygame.mixer.init()

logger = logging.getLogger(__name__)

TTS_DEFAULT_VOICE:str|None = None
'Default voice to use (https://github.com/bytectlgo/edge-tts/blob/main/voice-list.md)'

NUMBER:int = 0
'Current generate number (loops at 2**24)'

def get_number() -> int:
    """
    Returns a random (currently unused) number
    """

    global NUMBER

    NUMBER = (NUMBER + 1) % 16777216

    return NUMBER

def set_default_voice(voice:str):
    """
    Sets the default voice to use
    
    Arguments:
        voice:
            The voice (shortname) for the AI to use (https://github.com/bytectlgo/edge-tts/blob/main/voice-list.md)
    """
    
    global TTS_DEFAULT_VOICE
    
    TTS_DEFAULT_VOICE = voice

def _get_default_voice() -> str|None:
    """
    Returns the default voice
    """
    return TTS_DEFAULT_VOICE

# Define queue
class Queue:
    """
    Allow for generating and playing edge tts audio at high speeds and robustly
    
    Attributes:
        generate (function): To generate a prompt and play
        queue_play (function): To queue a play path
        check_generate (function): To check for new things to generate (run every frame)
        check_play (function): To check for new things to play (run every frame)
        remove_generate (function): To remove a generate request from queue
        remove_play (function): To remove a play request from queue
        wipe_dir (function): To remove all generated files (at the start of program)
        check_played (function): To check if something has started playing yet
        has_completed (function): Checks if all functions have completed
        terminate (function): Stops all queue functions

        generate_queue (dict): The queue for generating new tts messages
        generating (bool): If the queue is generating
        force_completion (bool): Instantly ends all playing audio when true
        play_queue (dict): The queue for playing tts messages
        playing (bool): If the queue is playing
        terminated (bool): If the queue is stopped entirely
    """
    
    generate_queue:dict[int,list[tuple]]
    generating:bool
    force_completion:bool
    play_queue:dict[int,list[tuple]] 
    playing:bool
    terminated:bool = False
        
    def __init__(self):
        """
        Generate a new queue
        """
        
        # Generate queue to prevent overlapping generates
        self.generate_queue = {}
        self.generating = False
        self.force_completion = False
        
        # Play queue to prevent overlapping sound
        self.play_queue = {}
        self.playing = False
    
    def _generate(self,text:str,voice:str,volume:int=0,rate:int=0,pitch:int=0,priority:int=0):
        """
        Begins the generation of an item in queue
        """
        
        # Get the new output file path
        path = f".\\temp\\output{get_number()}.mp3"
        
        # Log generation message
        logger.debug(f"Generating TTS Message at: {path} with content: {text}")

        # Prevent other plays from running
        self.queue_play(path,priority,text,False)
        
        # Don't generate twice
        self.remove_generate(text,priority)
        
        # Start generating
        asyncio.run(generate(self,text,voice,volume,rate,pitch,priority,path))

    def _play(self,path:str,priority:int,text:str,ready:bool,no_delete:bool):
        """
        Begins the play of an item in queue
        """
        
        self.remove_play(path,priority)
        play(self,path,no_delete)
    
    def generate(self,text:str,voice:str|None=None,volume:int=0,rate:int=0,pitch:int=0,priority:int=0,timeout:float|None=None):
        """
        Request a generate
        
        Arguments:
            queue:
                The queue to append play request to
            text:
                The text for the AI to speak
            voice:
                The voice (shortname) for the AI to use (https://github.com/bytectlgo/edge-tts/blob/main/voice-list.md)
                
                Can be none if voice has been specified by `set_default_voice()`
            rate:
                The additional speed of the voice (%) this can be positive or negative
            volume:
                The additional volume of the voice (%) this can be positive or negative
            pitch:
                The additional pitch of the voice (Hz) this can be positive or negative
            priority:
                The urgency of the audio to be played (lower will be played first)
            timeout:
                How long until the generate request should be canceled (Seconds)
        """
        
        if voice is None:
            
            if TTS_DEFAULT_VOICE is None:
            
                raise ValueError("Global and local TTS Voice not specified, call `set_default_voice()` or specify voice in function")
        
            voice = TTS_DEFAULT_VOICE
        
        # Get the generate queue
        queue = self.generate_queue
        
        # Check if a new list needs to be generated
        if priority not in queue:
            queue[priority] = []
            
        # Add request to queue
        queue[priority].append((text,voice,volume,rate,pitch,priority,(time.time()+timeout if timeout is not None else None)))
        
        # Log generation message
        logger.debug(f"Generating request added for TTS Message with content: {text}")
    
    def queue_play(self,path:str,priority:int=0,text:str="",ready:bool=True,no_delete:bool=False):
        """
        Queues a play (usually by generate function)
        
        Arguments:
            path:
                The path to play on
            priority:
                The priority of the play request
            text:
                The original text message of the generate request
            ready:
                If the sound should be played once the queue has reached it or if the program should wait for ready_play() to called
            no_delete:
                If the file should be preserved once playing is completed
        """
        
        # Get the play queue
        queue = self.play_queue
        
        # Check if a new list needs to be generated
        if priority not in queue:
            queue[priority] = []
            
        # Add request to queue
        queue[priority].append((path,priority,text,ready,no_delete))
        
        # Log play message
        logger.debug(f"Play request added for TTS Message with content: {text}")
    
    def ready_play(self,path:str,priority:int=0):
        """
        Makes a play request ready to be played
        This prevents sounds of lower priority from getting played first and makes the function always prioritize lower priority
        
        Arguments:
            path:
                The path of the play request
            priority:
                The priority of the play request (this helps with tracking down the play request)
        """
        
        # Get the queue
        queue = self.play_queue
        
        # Find the item
        for n,item in enumerate(queue[priority]):
            
            if item[0] == path:
            
                # Set the ready to true
                queue[priority][n] = tuple(list(item)[:-2]+[True,]+list(item)[-1:])
                
        # Log ready message
        logger.debug(f"Play request readied for TTS Message with path: {path}")
    
    def check_played(self,text:str,priority:int=0):
        """
        Returns true if the sound has started playing, returns false if it is still queued
        
        Arguments:
            text:
                The text the original generate was called with
            priority:
                The priority of the play call (same as generate request)
        """
        
        # Checking play queue
        # Get the queue
        queue = self.play_queue
        
        # Only run if priority in queue
        if priority in queue:
            
            # Find the item
            for item in queue[priority]:
                if item[2] == text:
                
                    # If it has been found, return false (it's stilled queued)
                    return False
        
        # Checking generate queue
        # Get the queue
        queue = self.generate_queue
        
        # Only run if priority in queue
        if priority in queue:
            
            # Find the item
            for item in queue[priority]:
                
                if item[0] == text:
                
                    # If it has been found, return false (it's stilled queued)
                    return False
                
        # If it can't be located, it isn't in queue
        return True
        
    def _generate_next(self):
        """
        Generates the lowest priority item in the queue
        """
        
        # Get the generate queue
        queue = self.generate_queue
        
        # Find the lowest priority
        queue_list = list(queue)
        queue_list.sort()
        queue_indexed = queue_list[0]
        
        # Get queue item (actual settings from generate request)
        queue_item = queue[queue_indexed][0]
        
        # If the lowest priority item has no timeout
        # And the lowest priority item is timed out, delete and cancel
        if queue_item[6] is not None and queue_item[6] < time.time():
            
            self.remove_generate(queue_item[0],queue_indexed)
            return
            
        # Start generating
        self.generating = True
        threading.Thread(target=self._generate,args=queue_item[:-1]).start()
    
    def _play_next(self):
        """
        Plays the lowest priority item in the queue
        """
        
        # Get the play queue
        queue = self.play_queue
        
        # Find the lower priority
        queue_list = list(queue)
        queue_list.sort()
        queue_indexed = queue_list[0]
        
        # Find any sounds of that priority that are ready
        queue_found = None
        for item in queue[queue_indexed]:
            if item[3]:
                queue_found = item
                break
        
        # Stop attempting to play if none is found
        if queue_found is None:
            return
        
        # Start playing
        self.playing = True
        threading.Thread(target=self._play,args=queue_found).start()
        
    def remove_generate(self,text:str,priority:int=0):
        """
        Removes an item from the generation queue if it still exists
        
        Arguments:
            text:
                The text the generate was requested with
            priority:
                The priority of the generate request (this helps with tracking down the generate request)
        """
        
        # Get the generate queue
        queue = self.generate_queue
        
        # Cancel if the priority doesn't exist
        if priority not in queue:
            return -1
        
        # Get the section of the queue to search
        queue_section = queue[priority]
        
        # Search the queue
        for item in queue_section:
            
            # Remove the item from queue
            if item[0] == text:
                queue_section.remove(item)
                
                # If the section is now empty, remove it
                if len(queue_section) == 0:
            
                    queue.pop(priority)
        
    def remove_play(self,path:str,priority:int=0):
        """
        Removes an item from the play queue if it still exists
        
        Arguments:
            text:
                The path the play was requested with
            priority:
                The priority of the play request (this helps with tracking down the play request)
        """
        
        # Get the play queue
        queue = self.play_queue
        
        if priority not in queue:
            return -1
        
        # Cancel if the priority doesn't exist
        queue_section = queue[priority]
        
        # Search the queue
        for item in queue_section:
            
            # Remove the item from queue
            if item[0] == path:
                queue_section.remove(item)
                
                # If the section is now empty, remove it
                if len(queue_section) == 0:
                    
                    queue.pop(priority)
    
    def stop_play(self):
        """
        Instantly stops the currently playing audio
        """
        
        self.force_completion = True
        
    def check_generate(self):
        """
        Checks for new audio to generate
        """
        
        # Generate new if there is something to generate and not currently generating
        if not self.generating and len(self.generate_queue) > 0:
            
            self._generate_next()
            
    def check_play(self):
        """
        Checks for new audio to play
        """
        
        # Play new if there is something to play and not currently play
        if not self.playing and len(self.play_queue) > 0:
            
            self._play_next()
            
    def wipe_dir(self):
        """
        Wipes the /temp directory of output{n}.mp3 files and clears queue
        """
        
        # Make sure directory exists
        if "temp" not in os.listdir():
            
            # If it does not exist, create one and end func            
            os.mkdir(".\\temp")
            logger.warning("No temp found, creating temp")
            return
        
        # Wipe queue
        self.play_queue:dict[int,list[tuple]] = {}
        self.generate_queue:dict[int,list[tuple]] = {}
        
        # Stop generation wait (keep waiting for play to finish to prevent sound overlap)
        self.generating = False

        # Go through every file
        for file in os.listdir(".\\temp"):
            
            # Delete all containing "output" and of type "mp3"
            if "output" in file and (os.path.splitext(file)[1] in [".mp3",".wav"]):
                
                os.remove(".\\temp\\"+file)
                
        # Log that all files were clear
        logger.debug("Cleared generated TTS files")
        
    def has_completed(self) -> bool:
        """
        Checks if all generations have finished generating and playing
        """
        
        if len(self.generate_queue) > 0:
            return False
        if len(self.play_queue) > 0:
            return False
        if self.playing:
            return False
        return not self.generating

    def terminate(self) -> None:
        """
        Attempts to stop the queue threaded functions and playing audio
        """

        self.terminated = True
        self.force_completion = True

async def generate(queue:Queue,text:str,voice:str|None=None,volume:int=0,rate:int=0,pitch:int=0,priority:int=0,path:str=".\\tts\\output.mp3"):
    """
    Request immediate generation from edge servers
        
    Arguments:
        queue:
            The queue to append play request to
        text:
            The text for the AI to speak
        voice:
            The voice (shortname) for the AI to use (https://github.com/bytectlgo/edge-tts/blob/main/voice-list.md)
            
            Can be none if a voice has been specified by `set_default_voice()`
        rate:
            The additional speed of the voice (%) this can be positive or negative
        volume:
            The additional volume of the voice (%) this can be positive or negative
        pitch:
            The additional pitch of the voice (Hz) this can be positive or negative
        priority:
            The urgency of the audio to be played (lower will be played first)
        path:
            The location to store the file
    """
    
    if voice is None:
            
        if TTS_DEFAULT_VOICE is None:
        
            raise ValueError("Global and local TTS Voice not specified, call `set_default_voice()` or specify API key in function")
    
        voice = TTS_DEFAULT_VOICE
    
    # Format parameters
    frate:str = ("+" if rate >= 0 else "") + str(rate) + "%"
    fvolume:str = ("+" if volume >= 0 else "") + str(volume) + "%"
    fpitch:str = ("+" if pitch >= 0 else "") + str(pitch) + "Hz"
    
    # Communicate to edge servers
    communicated = edge_tts.Communicate(text,voice,rate=frate,volume=fvolume,pitch=fpitch)
    
    # Save the mp3 file
    await communicated.save(path)
    
    # Allow another item to be queued
    queue.generating = False
    
    # Notify readying
    logger.debug(f"Readying play request for path: {path}")
    
    # Allow play request to play
    queue.ready_play(path,priority)
    
    # Log that generation was completed
    logger.debug(f"Completed tts message generation at: {path} with content: {text}")

async def generate_no_play(text:str,voice:str|None=None,volume:int=0,rate:int=0,pitch:int=0,path:str=".\\tts\\output.mp3"):
    """
    Request immediate generation from edge servers and not play
        
    Arguments:
        text:
            The text for the AI to speak
        voice:
            The voice (shortname) for the AI to use (https://github.com/bytectlgo/edge-tts/blob/main/voice-list.md)
            
            Can be none if a voice has been set by `set_default_voice()`
        rate:
            The additional speed of the voice (%) this can be positive or negative
        volume:
            The additional volume of the voice (%) this can be positive or negative
        pitch:
            The additional pitch of the voice (Hz) this can be positive or negative
        path:
            The location to store the file
    """

    if voice is None:

        if TTS_DEFAULT_VOICE is None:

            raise ValueError("Global and local TTS Voice not specified, call `set_default_voice()` or specify API key in function")

        voice = TTS_DEFAULT_VOICE

    # Format parameters
    frate:str = ("+" if rate >= 0 else "") + str(rate) + "%"
    fvolume:str = ("+" if volume >= 0 else "") + str(volume) + "%"
    fpitch:str = ("+" if pitch >= 0 else "") + str(pitch) + "Hz"

    # Communicate to edge servers
    communicated = edge_tts.Communicate(text,voice,rate=frate,volume=fvolume,pitch=fpitch)

    # Save the mp3 file
    await communicated.save(path)

    # Log that generation was completed
    logger.debug(f"Completed tts message generation at: {path} with content: {text}")


def play_audio(queue:Queue, path: str):
    """
    Plays an audio file
    """

    if not os.path.exists(path):
        raise FileNotFoundError()

    # Load sound
    sound = pygame.mixer.Sound(path)

    # Play sound
    sound.play()

    # Get time to completion and await
    sound_len = sound.get_length()
    begin = time.time()

    # If time still remains wait slightly longer
    while time.time() - begin < sound_len and not queue.force_completion:
        time.sleep(0.1)

    # Free sound
    sound.stop()

def play(queue:Queue,path:str,no_delete:bool=False):
    """
    Starts playing an audio clip
    
    Arguments:
        queue:
            The queue to allow play request to work properly
        path:
            Path to play the sound on
        no_delete:
            If the file should be preserved once playing is completed
    """

    # Log play
    logger.debug(f"Playing TTS Message at: {path}")
    
    # Play sound
    try:
        play_audio(queue,path)
    except FileNotFoundError:
        
        # Not able to load sound
        logger.error(f"File not found: {path}")
        
        # Once finished, allow queue to play another sound
        queue.playing = False
        queue.force_completion = False
        return
    
    # Once finished, allow queue to play another sound
    queue.playing = False
    queue.force_completion = False
    
    # Log play completion
    logger.debug(f"Completed playing TTS Message at: {path}")
    
    # Remove sound
    if not no_delete:
        os.remove(path)

def _checker_thread(queue:Queue):
    
    while not queue.terminated:
        queue.check_generate()
        queue.check_play()

def dispatch_checker_thread(queue:Queue):
    """
    Makes a daemon thread that checks for updates to the queue automatically
    
    Arguments:
        queue:  
            The queue instance
    """
    
    threading.Thread(target=_checker_thread,args=(queue,),daemon=True).start()
