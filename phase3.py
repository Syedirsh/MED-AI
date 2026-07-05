# Step1a: Setup Text to Speech – TTS – model with gTTS
import os
import platform
import subprocess
from dotenv import load_dotenv
from gtts import gTTS

# Load environment variables
load_dotenv()

# Step1b: Setup Text to Speech – TTS – model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def text_to_speech_with_gtts(input_text, output_filepath, autoplay=False):
    try:
        language = "en"
        audioobj = gTTS(text=input_text, lang=language, slow=False)
        audioobj.save(output_filepath)

        if autoplay:
            _play_audio(output_filepath)

    except Exception as e:
        print("gTTS error:", e)


def text_to_speech_with_elevenlabs(input_text, output_filepath, autoplay=False):
    try:
        if not ELEVENLABS_API_KEY:
            print("ElevenLabs API key missing, falling back to gTTS...")
            return text_to_speech_with_gtts(input_text, output_filepath, autoplay)

        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        audio = client.generate(
            text=input_text,
            voice="Alice",
            model="eleven_turbo_v2"
        )

        elevenlabs.save(audio, output_filepath)

        if autoplay:
            _play_audio(output_filepath)

    except Exception as e:
        print("ElevenLabs error:", e)
        print("Falling back to gTTS...")
        text_to_speech_with_gtts(input_text, output_filepath, autoplay)


def _play_audio(filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":
            subprocess.run(['ffplay', '-nodisp', '-autoexit', filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', filepath])
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"Audio play error: {e}")


# === TEST BLOCK ===
if __name__ == "__main__":
    input_text = "Hi, this is a test voice."
    text_to_speech_with_elevenlabs(
        input_text,
        output_filepath="test.mp3",
        autoplay=True
    )