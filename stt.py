import openai
import streamlit as st
from groq import Groq
import logging
from deepgram import DeepgramClient
import streamlit as st

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
    try:
        deepgram = DeepgramClient(api_key=st.secrets["DEEPGRAM_API_KEY"])

        response = deepgram.speak.v1.audio.generate(
            text=text,
            model="aura-2-thalia-en"
        )

        audio_bytes = response.stream.getvalue()

        with open("test.mp3", "wb") as audio_file:
            audio_file.write(audio_bytes)

        st.success("Audio saved successfully!")
        return audio_bytes

    except Exception as e:
        st.error(f"Exception: {e}")
        return None


    
    
       
