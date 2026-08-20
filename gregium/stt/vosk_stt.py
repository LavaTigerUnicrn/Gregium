"""
A method of speech-to-text on the microphone using the offline vosk library
"""

from ..verification import verify_exists

verify_exists("vosk","vosk")

import json

import pyaudio
from vosk import KaldiRecognizer, Model


class Recognizer:
    """
    Generates a vosk interpreter
    
    Use get_audio to get audio
    
    :param model_path: Find models at: https://alphacephei.com/vosk/models
    
        *The model should be the path to the model folder within the zip*
    :type model_path: str
    """
    def __init__(self,model_path:str): 
        
        # Make model
        model = Model(model_path)
        self.recognizer = KaldiRecognizer(model,160000)
        
        # Make stream
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=160000, input=True,frames_per_buffer=8192)
        self.stream.start_stream()
        
    def get_audio(self) -> str:
        """
        Reads audio and returns the text
        """
        
        # Read audio
        data = self.stream.read(4096, exception_on_overflow=False)
        
        if self.recognizer.AcceptWaveform(data):
            # Read
            result = json.loads(self.recognizer.Result())
            
            # Return the result
            return result["text"]

        return ""