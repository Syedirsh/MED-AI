# ==============================
# Phase 2 - Speech to Text
# ==============================

import os
import logging
from io import BytesIO

import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

STT_MODEL = "whisper-large-v3"



# Record Audio

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            logging.info("Listening...")

            audio_data = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

            wav_data = audio_data.get_wav_data()

            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(
                file_path,
                format="mp3",
                bitrate="128k"
            )

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"Recording failed: {e}")



# Speech to Text using Groq


def transcribe_with_groq(
    stt_model=STT_MODEL,
    audio_filepath=None,
    GROQ_API_KEY=None
):

    try:

        if not audio_filepath:
            return "No audio file provided."

        if not os.path.exists(audio_filepath):
            return "Audio file not found."

        api_key = GROQ_API_KEY or os.environ.get("GROQ_API_KEY")

        if not api_key:
            return "GROQ API key not found."

        client = Groq(api_key=api_key)

        with open(audio_filepath, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )

        return transcription.text

    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return "Error during transcription."


# Test

if __name__ == "__main__":

    audio_filepath = "patient_voice_test.mp3"

    record_audio(audio_filepath)

    result = transcribe_with_groq(
        audio_filepath=audio_filepath
    )

    print("\nTranscription:\n")
    print(result)