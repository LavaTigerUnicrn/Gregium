"""
A number of different TTS methods

If none of these work, try `RealtimeTTS` (it should be automatically installed)
"""
# Import libraries
import threading
import asyncio
import os
import pygame
import edge_tts
import time
from ...logger.basic_logs import *
from ...settings import TTS_VOICE
import tts_with_rvc
from pathlib import Path

# Get settings
TTS_DEFAULT_VOICE = TTS_VOICE

# Initialize pygame
pygame.init()

# Define queue
class Queue():
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
        
        generate_queue (dict): The queue for generating new tts messages
        generate_file_num (int): The current file number for generating tts messages
        generating (bool): If the queue is generating
        force_completion (bool): Instantly ends all playing audio when true
        play_queue (dict): The queue for playing tts messages
        playing (bool): If the queue is playing
    """
    
    generate_queue:dict[str,list[tuple]]
    generate_file_num:int
    generating:bool
    force_completion:bool
    play_queue:dict[str,list[tuple]] 
    playing:bool
        
    def __init__(self):
        """
        Generate a new queue
        """
        
        # Generate queue to prevent overlapping generates
        self.generate_queue = {}
        self.generate_file_num = 0
        self.generating = False
        self.force_completion = False
        
        # Play queue to prevent overlapping sound
        self.play_queue = {}
        self.playing = False
    
    def _generate(self,text:str,voice:str=TTS_DEFAULT_VOICE,volume:int=0,rate:int=0,pitch:int=0,priority:int=0):
        """
        Begins the generation of an item in queue
        """
        
        # Get the new output file path
        path = f".\\temp\\output{self.generate_file_num}.mp3"
        self.generate_file_num = (self.generate_file_num + 1) % 128
        
        # Log generation message
        info(f"Generating TTS Message at: {path} with content: {text}",__name__)

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
    
    def generate(self,text:str,voice:str=TTS_DEFAULT_VOICE,volume:int=0,rate:int=0,pitch:int=0,priority:int=0,timeout:int=None):
        """
        Request a generate
        
        Arguments:
            queue:
                The queue to append play request to
            text:
                The text for the AI to speak
            voice:
                The voice for the AI to use (https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462)
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
        
        # Get the generate queue
        queue = self.generate_queue
        
        # Check if a new list needs to be generated
        if priority not in queue:
            queue[priority] = []
            
        # Add request to queue
        queue[priority].append((text,voice,volume,rate,pitch,priority,(time.time()+timeout if timeout is not None else None)))
        
        # Log generation message
        info(f"Generating request added for TTS Message with content: {text}",__name__)
    
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
        info(f"Play request added for TTS Message with content: {text}",__name__)
    
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
        info(f"Play request readied for TTS Message with path: {path}",__name__)
    
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
        
        # If the lowest priority item has no timeout, continue
        if queue_item[6] is not None:
            
            # If the lowest priority item is timed out, delete and cancel
            if queue_item[6] < time.time():
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
            warn("No temp found, creating temp",__name__)
            return
        
        # Wipe queue
        self.play_queue:dict[str,list[tuple]] = {}
        self.generate_queue:dict[str,list[tuple]] = {}
        
        # Reset number
        self.generate_file_num = 0
        
        # Stop generation wait (keep waiting for play to finish to prevent sound overlap)
        self.generating = False

        # Go through every file
        for file in os.listdir(".\\temp"):
            
            # Delete all containing "output" and of type "mp3" or "wav"
            if "output" in file and (os.path.splitext(file)[1] == ".mp3" or os.path.splitext(file)[1] == ".wav"):
                
                os.remove(".\\temp\\"+file)
                
        # Log that all files were clear
        info("Cleared generated TTS files",__name__)
        
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
        if self.generating:
            return False
        return True

async def generate(queue:Queue,text:str,voice:str=TTS_DEFAULT_VOICE,volume:int=0,rate:int=0,pitch:int=0,priority:int=0,path:str=".\\tts\\output.mp3"):
    """
    Request immediate generation from edge servers
        
    Arguments:
        queue:
            The queue to append play request to
        text:
            The text for the AI to speak
        voice:
            The voice for the AI to use
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
    
    # Format parameters
    rate = ("+" if rate >= 0 else "") + str(rate) + "%"
    volume = ("+" if volume >= 0 else "") + str(volume) + "%"
    pitch = ("+" if pitch >= 0 else "") + str(pitch) + "Hz"
    
    # Communicate to edge servers
    communicated = edge_tts.Communicate(text,voice,rate=rate,volume=volume,pitch=pitch)
    
    # Save the mp3 file
    await communicated.save(path)
    
    # Allow another item to be queued
    queue.generating = False
    
    # Notify readying
    info(f"Readying play request for path: {path}",__name__)
    
    # Allow play request to play
    queue.ready_play(path,priority)
    
    # Log that generation was completed
    info(f"Completed tts message generation at: {path} with content: {text}",__name__)
    
async def generate_no_play(text:str,voice:str=TTS_DEFAULT_VOICE,volume:int=0,rate:int=0,pitch:int=0,path:str=".\\tts\\output.mp3"):
    """
    Request immediate generation from edge servers and not play
        
    Arguments:
        text:
            The text for the AI to speak
        voice:
            The voice for the AI to use
        rate:
            The additional speed of the voice (%) this can be positive or negative
        volume:
            The additional volume of the voice (%) this can be positive or negative
        pitch:
            The additional pitch of the voice (Hz) this can be positive or negative
        path:
            The location to store the file
    """
    
    # Format parameters
    rate = ("+" if rate >= 0 else "") + str(rate) + "%"
    volume = ("+" if volume >= 0 else "") + str(volume) + "%"
    pitch = ("+" if pitch >= 0 else "") + str(pitch) + "Hz"
    
    # Communicate to edge servers
    communicated = edge_tts.Communicate(text,voice,rate=rate,volume=volume,pitch=pitch)
    
    # Save the mp3 file
    await communicated.save(path)
    
    # Log that generation was completed
    info(f"Completed tts message generation at: {path} with content: {text}",__name__)
 
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
    info(f"Playing TTS Message at: {path}",__name__)
    
    # Play sound
    try:
        pygame.mixer.music.load(path,os.path.basename(path).split(".")[1])
        pygame.mixer.music.play()
    except:
        
        # Not able to load sound
        error(f"File not found: {path}",__name__)
        
        # Once finished, allow queue to play another sound
        queue.playing = False
        queue.force_completion = False
        pygame.mixer.music.unload()
        return
    
    # Wait for completion
    while pygame.mixer.music.get_busy() and not queue.force_completion:
        
        time.sleep(0.1)
        
    # Unload sound
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    
    # Once finished, allow queue to play another sound
    queue.playing = False
    queue.force_completion = False
    
    # Log play completion
    info(f"Completed playing TTS Message at: {path}",__name__)
    
    # Remove sound
    if not no_delete:
        os.remove(path)

class QueuedRVCObject:
    
    timeout:int|None
    def __init__(self,text,tts_rate:int=0,tts_volume:int=0,tts_pitch:float=0,index_rate:float=0.75,resample_sr:int=0,rms_mix_rate:float=0.5,protect:float=0.33,priority:int=0,timeout:int=None):
        self.text = text
        self.tts_rate = tts_rate
        self.tts_volume = tts_volume
        self.tts_pitch = tts_pitch
        self.index_rate = index_rate
        self.resample_sr = resample_sr
        self.rms_mix_rate = rms_mix_rate
        self.protect = protect
        self.timeout = timeout
        self.priority = priority
        
    def __getitem__(self,index:int):
        
        if index == 0:
            return self.text
        
        raise Exception()

class Queue_RVC(Queue):
    """
    A modified version for RVC TTS
    
    Allow for generating and playing edge tts audio at high speeds and robustly
    
    Attributes:
        generate (function): to generate a prompt and play
        queue_play (function): to queue a play path
        check_generate (function): to check for new things to generate (run every frame)
        check_play (function): to check for new things to play (run every frame)
        remove_generate (function): to remove a generate request from queue
        remove_play (function): to remove a play request from queue
        wipe_dir (function): to remove all generated files (at the start of program)
        check_played (function): to check if something has started playing yet
        
        generate_queue (dict): The queue for generating new tts messages
        generate_file_num (int): The current file number for generating tts messages
        generating (bool): If the queue is generating
        force_completion (bool): Instantly ends all playing audio when true
        play_queue (dict): The queue for playing tts messages
        playing (bool): If the queue is playing
    """
    generate_queue:dict[str,list[QueuedRVCObject]]
    
    def __init__(self,path:str,index:str="",device:str="cuda:0",voice:str=TTS_DEFAULT_VOICE):
        """
        Generate a new queue
        
        Arguments:
            path: The path of the PTH file
            index: The path of the index file
            device: The device to perform AI calculations (generally cuda for gpu and cpu for cpu)
            voice: The edge tts voice (https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462)
        """
        
        # Make base
        super().__init__()
        
        # Load RVC
        info(f"Loading RVC with PTH={path} Voice={voice}",__name__)
        self.generator = tts_with_rvc.TTS_RVC(path,index_path=index,device=device,voice=voice)
    
    def generate(self,text,tts_rate:int=0,tts_volume:int=0,tts_pitch:float=0,index_rate:float=0.75,resample_sr:int=0,rms_mix_rate:float=0.5,protect:float=0.33,priority:int=0,timeout:int=None):
        """
        Generates speech from text using Edge TTS and converts it using RVC.

        Args:
            text (str): The text to synthesize.
            pitch (int, optional): Pitch change (transpose) for RVC in semitones. Defaults to 0.
            tts_rate (int, optional): Speed adjustment for Edge TTS in percentage (+-). Defaults to 0.
            tts_volume (int, optional): Volume adjustment for Edge TTS in percentage (+-). Defaults to 0.
            tts_pitch (int, optional): Pitch adjustment for Edge TTS in Hz (+-). Defaults to 0.
            output_filename (str, optional): Name for the output file. If None, a unique name is generated. Defaults to None.
            index_rate (float, optional): Contribution of the RVC index file (0 to 1). Defaults to 0.75.
            resample_sr (int, optional): Sample rate to resample audio to. 0 means no resampling. Defaults to 0.
            rms_mix_rate (float, optional): Volume envelope scaling (0-1). Lower values mimic original volume. Defaults to 0.5.
            protect (float, optional): Protection for voiceless consonants and breaths (0-1). Lower values increase protection. 0.5 disables. Defaults to 0.33.
            priority (int, optional): The urgency of the audio to be played (lower will be played first)
            timeout (int, optional): How long until the generate request should be canceled (Seconds)

        Raises:
            RuntimeError: If TTS or RVC process fails.
            ValueError: If parameters are invalid.
        """
        
        # Get the generate queue
        queue = self.generate_queue
        
        # Check if a new list needs to be generated
        if priority not in queue:
            queue[priority] = []
            
        # Add request to queue
        # TODO: Fix adding request to queue
        queue[priority].append(QueuedRVCObject(text,tts_rate,tts_volume,tts_pitch,index_rate,resample_sr,rms_mix_rate,protect,priority,(time.time()+timeout if timeout is not None else None)))
        
        # Log generation message
        info(f"Generating request added for TTS Message with content: {text}",__name__)
        
    def _generate(self,arguments:QueuedRVCObject):
        """
        Begins the generation of an item in queue
        """
        
        # Extract important information
        text = arguments.text
        priority = arguments.priority
        tts_pitch = arguments.tts_pitch
        tts_volume = arguments.tts_volume
        tts_rate = arguments.tts_rate
        index_rate = arguments.index_rate
        resample_sr = arguments.resample_sr
        rms_mix_rate = arguments.rms_mix_rate
        protect = arguments.protect
        
        # Get the new output file path
        path = f".\\temp\\output{self.generate_file_num}.wav"
        true_path = f".\\output{self.generate_file_num}.wav"
        self.generate_file_num = (self.generate_file_num + 1) % 128
        
        # Log generation message
        info(f"Generating TTS Message at: {path} with content: {text}",__name__)

        # Prevent other plays from running
        self.queue_play(path,priority,text,False)
        
        # Don't generate twice
        self.remove_generate(text,priority)
        
        # Generate
        self.generator(text,tts_pitch,tts_rate,tts_volume,tts_pitch,true_path,index_rate,resample_sr=resample_sr,rms_mix_rate=rms_mix_rate,protect=protect,f0method="rmvpe")
        
        # Allow another item to be queued
        self.generating = False
        
        # Notify readying
        info(f"Readying play request for path: {path}",__name__)
        
        # Allow play request to play
        self.ready_play(path,priority)
        
        # Log that generation was completed
        info(f"Completed tts message generation at: {path} with content: {text}",__name__)
        
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
        
        # If the lowest priority item has no timeout, continue
        if queue_item.timeout is not None:
            
            # If the lowest priority item is timed out, delete and cancel
            if queue_item.timeout < time.time():
                self.remove_generate(queue_item[0],queue_indexed)
                return
            
        # Start generating
        self.generating = True
        threading.Thread(target=self._generate,args=[queue_item,]).start()

# Get path
models_path = str(Path(__file__).parent.absolute()) + "/models/"

def update_model_path(new_path:str):
    """
    Changes the path the rvc models are located in
    
    Arguments:
        new_path:
            The new path to check in
    """
    global models_path
    
    # Change path
    models_path = new_path

def load_model(model_name:str) -> Queue_RVC:
    """
    Quickly loads a model from models
    
    Arguments:
        model_name:
            The name of the model (should in in models)
    """
    
    # Scan for index and pth
    files = scan_for_files(model_name)
    
    # Load model
    return Queue_RVC(files["pth"],files["index"])
    
def scan_for_files(model_name:str) -> dict:
    """
    Checks for the pth and index files in models
    
    Returns (dict): The pth file at key "pth" and index file at "index" (key "index" will be an empty string if missing)
    
    Arguments:
        model_name:
            The name of the model (should in in models)
    """
    
    # Get path from root
    path = models_path+"/"+model_name
    
    # Check for files with extension
    potential = os.listdir(path)
    potential_pth = list(filter(lambda x: ".pth" in x,potential))
    potential_index = list(filter(lambda x: ".index" in x,potential))
    
    # Combine into dict
    output = {"pth":path+"/"+potential_pth[0],"index":""}
    
    if len(potential_index) > 0:
        
        output["index"] = path+"/"+potential_index[0]
        
    return output

def list_models() -> list:
    """
    Lists all possible models
    """
    # Get path from root
    path = models_path
    
    # List all folders
    return os.listdir(path)

def _checker_thread(queue:Queue):
    
    while True:
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