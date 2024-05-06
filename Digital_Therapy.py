import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import openai

# Set up OpenAI API
openai.api_key = "sk-proj-zyPvrlTy01HgghLEhiS5T3BlbkFJ606eGcjwOA4pA4noDwg3"

# Function to transcribe speech to text
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Function to generate response from OpenAI API
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Function to convert text to audio
def text_to_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

# Streamlit app
def main():
    st.title("Digital Therapist")

    # Record audio
    st.write("Click the button below and speak to start recording:")
    record_state = st.button("Record")

    if record_state:
        with st.spinner("Recording..."):
            filename = "user_audio.wav"
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.listen(source)
                with open(filename, "wb") as file:
                    file.write(audio_data.get_wav_data())

        st.success("Recording saved!")

        # Transcribe audio to text
        text = transcribe_audio(filename)
        st.write("You said:", text)

        # Get response from OpenAI API
        prompt = "User: " + text + "\nTherapist:"
        response = generate_response(prompt)
        st.write("Therapist:", response)

        # Convert response to audio
        therapist_audio_filename = "therapist_audio.mp3"
        text_to_audio(response, therapist_audio_filename)

        # Display audio player for therapist response
        st.audio(therapist_audio_filename, format="audio/mp3")

if __name__ == "__main__":
    main()
