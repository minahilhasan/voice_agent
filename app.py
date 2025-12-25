import streamlit as st
from stt import transcribe_audio,aireply,give_response
from streamlit_audio_recorder import audio_recorder

def main():
    st.title("Real Time Voice Agent")
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.write("Transcribing audio...")
        try:
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_bytes)
            with open("temp_audio.wav", "rb") as audio_file:
                transcription = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
                st.write("transcribing audio....")
                st.subheader("Transcribe Text")
                transcribed=transcription[text]
                st.write(transcribed)
        except Exception as e:
            st.error(f"Transcription Error: {e}")
            return
        reply=aireply(transcribed)
        if reply:
            st.write(f"The AI responded: {reply}")
            audio=give_response(reply)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.error("Audio could not be generated")
        else:
            st.error("AI could not respond")
        

if __name__ == "__main__":
    main()
