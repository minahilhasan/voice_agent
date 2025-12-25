import streamlit as st
from stt import aireply, give_response
from streamlit_mic_recorder import mic_recorder
import openai

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Transcription function
def transcribe_audio(audio_bytes):
    with open("temp_audio.webm", "wb") as f:
        f.write(audio_bytes)

    with open("temp_audio.webm", "rb") as f:
        transcription = openai.Audio.transcribe(
            model="whisper-1",
            file=f,
            language="en"
        )
    return transcription["text"]

def main():
    st.title("Real Time Voice Agent")

    st.write("🎤 Press Start, speak, then Stop to get the AI response.")

    # Record audio from mic
    audio_info = mic_recorder(start_prompt="🎙️ Start", stop_prompt="⏹️ Stop")

    if audio_info:
        audio_bytes = audio_info["bytes"]
        st.audio(audio_bytes, format="audio/webm")

        st.write("Transcribing audio...")
        try:
            transcribed = transcribe_audio(audio_bytes)
            st.subheader("Transcribed Text")
            st.write(transcribed)
        except Exception as e:
            st.error(f"Transcription Error: {e}")
            return

        # Get AI reply
        reply = aireply(transcribed)
        if reply:
            st.write(f"The AI responded: {reply}")

            # Generate TTS
            audio = give_response(reply)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.error("Audio could not be generated")
        else:
            st.error("AI could not respond")

if __name__ == "__main__":
    main()

