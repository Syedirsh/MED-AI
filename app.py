# VoiceBot UI with Gradio
import os
import gradio as gr

from phase1 import encode_image, analyze_image_with_query
from phase2 import transcribe_with_groq
from phase3 import text_to_speech_with_elevenlabs

system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose. 
What's in this image? Do you find anything wrong with it medically? If you make a differential, suggest some remedies for them. 
Never add any numbers or special characters like " * " in your response. Your answer should sound like a real doctor talking to a patient. 
Avoid saying 'As an AI' or using markdown. Always start your response directly by saying 'With what I see, I think you might have...'. 
Keep your explanation natural and informative — 3 to 5 sentences maximum. Mention any concern seen and give basic advice or a remedy clearly. 
Be consistent in your medical reasoning — if the same image is given again, try to give a similar response unless the visual input clearly changes."""

def process_inputs(audio_filepath, image_filepath):
    transcription = transcribe_with_groq(
        stt_model="whisper-large-v3",
        audio_filepath=audio_filepath,
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
    )

    if image_filepath:
        encoded_image = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(
            query=system_prompt + transcription,
            encoded_image=encoded_image,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    text_to_speech_with_elevenlabs(
        input_text=doctor_response,
        output_filepath="final.mp3",
        autoplay=False
    )

    return transcription, doctor_response, "final.mp3"

# Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(
            sources=["microphone", "upload"], 
            type="filepath", 
            label="Describe Your Symptoms",
            interactive=True,
            show_label=True
        ),
        gr.Image(type="filepath", label="Upload Affected Area (if any)")
    ],
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor Speaks", autoplay=True)
    ],
    title="MED-AI -VIRTUAL DOCTOR  "
)

iface.launch()