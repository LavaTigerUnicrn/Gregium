from RealtimeSTT import AudioToTextRecorder
from ...settings import LANGUAGE

def generate_recorder(lang:str=LANGUAGE,spinner:bool=False,realtime_func=None):
    """
    Generates a recorder for a given language
    
    Make sure the program runs on if __name__ == "__main__"
    
    Use AudioToTextRecorder.text() to get the said text
    
    Arguments:
        lang:
            The language (set this to "" to auto detect language)
        spinner:
            Toggles the spinner whilst talking
        realtime_func:
            If set to a function will run said function for every word said
    """
    
    use_realtime = False
    if realtime_func is not None:
        use_realtime = True
    
    return AudioToTextRecorder(language=lang,spinner=spinner,on_realtime_transcription_update=realtime_func,enable_realtime_transcription=use_realtime,no_log_file=True)
    

def wait_word(recorder:AudioToTextRecorder,word:str):
    """
    Waits for a word and then returns the text with the word present
    
    Arguments:
        recorder: A recorder instance
        word: The word to wait for
    """
    
    # Get text until found
    while True:
        text = recorder.text()
        
        print(text)
        
        if word.lower() in text.lower():
            
            return text