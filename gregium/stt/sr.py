"""
A method of speech-to-text on the microphone using online tools (google stt)
"""

import logging

from ..verification import verify_exists

logger = logging.getLogger(__name__)

verify_exists("speech_recognition", "SpeechRecognition")
verify_exists("pyaudio","PyAudio")

import speech_recognition as sr

recognizer = sr.Recognizer()


def adjust(duration: float = 1) -> None:
    """
    Adjusts current ambient noise level

    :param duration: The max amount of time to adjust in sections (must be at least 0.5s)
    :type duration: float, optional
    """

    with sr.Microphone() as source:
        logger.debug(f"Adjusting noise level duration: {duration}")
        recognizer.adjust_for_ambient_noise(source, duration=duration)
        logger.debug("Adjusted noise level")


def get() -> str:
    """
    Runs Speech-To-Text using Google STT

    If an error happens, will return a blank string
    """
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
    except Exception:
        logger.exception("Error whilst recognizing speech")
    return ""
