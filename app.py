import streamlit as st
from stt import transcribe_audio, aireply, give_response

def main():
    st.title("Real Time Voice Agent")

    # Option 1: record audio from mic
    recorded_audio = st.audio_input("Record your voice")

    # Option 2: upload audio file
    uploaded_audio = st.file_uploader(
        "Or upload an audio file:",
        type=["mp3", "wav"]
    )

    audio_file = recorded_audio or uploaded_audio

    if audio_file:
        st.write("Transcribing audio...")

        try:
            transcription = transcribe_audio(audio_file)
            st.subheader("Transcribed Text")
            st.write(transcription)
        except Exception as e:
            st.error(f"Transcription Error: {e}")
            return

        reply = aireply(transcription)
        if reply:
            st.subheader("AI Response")
            st.write(reply)

            audio = give_response(reply)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.error("Audio could not be generated")
        else:
            st.error("AI could not respond")

if __name__ == "__main__":
    main()


