# Step 1: Setup Audio recorder (ffmpeg & portaudio)
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"Recording error: {e}")


# Step 2: Speech-to-Text using GROQ
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY=None):
    try:
        if not audio_filepath:
            return "No audio file provided."

        api_key = GROQ_API_KEY or os.environ.get("GROQ_API_KEY")

        if not api_key:
            return "GROQ API key missing."

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


# === MAIN TEST BLOCK ===
if __name__ == "__main__":
    audio_filepath = "patient_voice_test.mp3"

    record_audio(file_path=audio_filepath)

    transcription_text = transcribe_with_groq(stt_model, audio_filepath)

    print("Transcription Result:\n", transcription_text)