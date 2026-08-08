import logging
import os
import threading
import time
from pathlib import Path

from ..verification import verify_exists
from . import Queue, _get_default_voice, get_number, set_default_voice, dispatch_checker_thread

verify_exists("tts_with_rvc", "tts_with_rvc")

import tts_with_rvc

logger = logging.getLogger(__name__)

class QueuedRVCObject:

    timeout: float | None

    def __init__(
        self,
        text: str,
        pitch: int,
        tts_rate: int = 0,
        tts_volume: int = 0,
        tts_pitch: int = 0,
        index_rate: float = 0.75,
        resample_sr: int = 0,
        rms_mix_rate: float = 0.5,
        protect: float = 0.33,
        priority: int = 0,
        timeout: float | None = None,
    ):
        self.text = text
        self.pitch = pitch
        self.tts_rate = tts_rate
        self.tts_volume = tts_volume
        self.tts_pitch = tts_pitch
        self.index_rate = index_rate
        self.resample_sr = resample_sr
        self.rms_mix_rate = rms_mix_rate
        self.protect = protect
        self.timeout = timeout
        self.priority = priority

    def __getitem__(self,item:int):

        if item == 0:
            return self.text

        return None


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
        terminate (function): Stops all queue functions
        
        generate_queue (dict): The queue for generating new tts messages
        generating (bool): If the queue is generating
        force_completion (bool): Instantly ends all playing audio when true
        play_queue (dict): The queue for playing tts messages
        playing (bool): If the queue is playing
        terminated (bool): If the queue is stopped entirely
    """

    generate_queue: dict[int, list[QueuedRVCObject]]

    def __init__(
        self,
        path: str,
        index: str = "",
        device: str = "cuda:0",
        voice: str | None = None,
    ):
        """
        Generate a new queue

        Arguments:
            path: The path of the PTH file
            index: The path of the index file
            device: The device to perform AI calculations (generally cuda for gpu and cpu for cpu)
            voice:
                The edge tts voice (https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462)

                Can be none if a voice has been specified by `set_default_voice()`
        """

        if voice is None:

            TTS_DEFAULT_VOICE = _get_default_voice()
            if TTS_DEFAULT_VOICE is None:

                raise ValueError(
                    "Global and local TTS Voice not specified, call `set_default_voice()` or specify voice in function"
                )

            voice = TTS_DEFAULT_VOICE

        # Make base
        super().__init__()

        # Load RVC
        logger.debug(f"Loading RVC with PTH={path} Voice={voice}")
        self.generator = tts_with_rvc.TTS_RVC(
            path, index_path=index, device=device, voice=voice
        )

    def generate(
        self,
        text: str,
        pitch: int = 0,
        tts_rate: int = 0,
        tts_volume: int = 0,
        tts_pitch: int = 0,
        index_rate: float = 0.75,
        resample_sr: int = 0,
        rms_mix_rate: float = 0.5,
        protect: float = 0.33,
        priority: int = 0,
        timeout: float | None = None,
    ):
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
        queue[priority].append(
            QueuedRVCObject(
                text,
                pitch,
                tts_rate,
                tts_volume,
                tts_pitch,
                index_rate,
                resample_sr,
                rms_mix_rate,
                protect,
                priority,
                (time.time() + timeout if timeout is not None else None),
            )
        )

        # Log generation message
        logger.debug(f"Generating request added for TTS Message with content: {text}")

    def _generate(self, arguments: QueuedRVCObject):
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
        pitch = arguments.pitch

        # Get the new output file path
        num = get_number()
        path = f".\\temp\\output{num}.wav" # TODO: CHANGE FILE NUMBER METHOD TO BE BETTER
        true_path = f".\\output{num}.wav"

        # Log generation message
        logger.debug(f"Generating TTS Message at: {path} with content: {text}")

        # Prevent other plays from running
        self.queue_play(path, priority, text, False)

        # Don't generate twice
        self.remove_generate(text, priority)

        # Generate
        self.generator(
            text,
            pitch,
            tts_rate,
            tts_volume,
            tts_pitch,
            true_path,
            index_rate,
            resample_sr=resample_sr,
            rms_mix_rate=rms_mix_rate,
            protect=protect,
            f0method="rmvpe",
        )

        # Allow another item to be queued
        self.generating = False

        # Notify readying
        logger.debug(f"Readying play request for path: {path}")

        # Allow play request to play
        self.ready_play(path, priority)

        # Log that generation was completed
        logger.debug(
            f"Completed tts message generation at: {path} with content: {text}"
        )

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
        # And the lowest priority item is timed out, delete and cancel
        if queue_item.timeout is not None and queue_item.timeout < time.time():

            self.remove_generate(queue_item.text, queue_indexed)
            return

        # Start generating
        self.generating = True
        threading.Thread(
            target=self._generate,
            args=[
                queue_item,
            ],
        ).start()