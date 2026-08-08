import argparse
import sys

from . import VERSION
from .verification import check_all

if __name__ == "__main__":

    # Make parser
    parser = argparse.ArgumentParser(prog=f"Gregium ({VERSION})")

    # Add verify argument
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Checks for missing Gregium dependencies that may not be installed by default",
    )

    # Parse
    args = parser.parse_args()

    # Verify libraries
    if args.verify:

        check_all(
            [
                "edge-tts",
                "blessed",
                "ollama",
                "beautifulsoup4",
                "pillow",
                "pygame-ce",
                "SpeechRecognition",
                "tts_with_rvc==0.1.9",
                "requests",
                "dotenv",
                "vosk",
                "PyAudio"
            ]
        )
        sys.exit()

    print("No action specified (run \"python -m gregium -h\" for help)")