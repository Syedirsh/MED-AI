# ====================================
# Phase 3 - Text To Speech
# ====================================

import os
import platform
import subprocess

from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

# gTTS

def text_to_speech_with_gtts(
    input_text,
    output_filepath,
    autoplay=False
):

    try:

        tts = gTTS(
            text=input_text,
            lang="en",
            slow=False
        )

        tts.save(output_filepath)

        if autoplay:
            play_audio(output_filepath)

    except Exception as e:
        print("gTTS Error:", e)



# Main TTS Function


def text_to_speech_with_elevenlabs(
    input_text,
    output_filepath,
    autoplay=False
):

    text_to_speech_with_gtts(
        input_text=input_text,
        output_filepath=output_filepath,
        autoplay=autoplay
    )



# Audio Player


def play_audio(filepath):

    try:

        os_name = platform.system()

        if os_name == "Windows":

            subprocess.run([
                "ffplay",
                "-nodisp",
                "-autoexit",
                filepath
            ])

        elif os_name == "Darwin":

            subprocess.run([
                "afplay",
                filepath
            ])

        elif os_name == "Linux":

            subprocess.run([
                "aplay",
                filepath
            ])

    except Exception as e:

        print("Playback Error:", e)



# Test


if __name__ == "__main__":

    text_to_speech_with_elevenlabs(
        input_text="Hello, this is a test.",
        output_filepath="test.mp3",
        autoplay=True
    )