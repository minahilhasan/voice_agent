import openai
import streamlit as st
from groq import Groq
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

def transcribe_audio(audio_file):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    audio=openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        language="en"
    )
    return audio['text']

def aireply(transcription):
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

    messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": transcription}
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    reply = response.choices[0].message.content


    messages.append({"role": "assistant", "content": reply})

    return reply


def give_response(text):
    elevenlabs = ElevenLabs(
        api_key=st.secrets["ELEVENLABS_API_KEY"],
    )

     try:
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        return audio 
    except Exception as e:
        st.error(f"TTS failed: {e}")
        return None
