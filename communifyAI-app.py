import streamlit as st
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
from tempfile import NamedTemporaryFile

# Initialize translator and recognizer
translator = Translator()
r = sr.Recognizer()

# Official Indian Languages + English
indian_languages = {
    "Assamese": "as",
    "Bengali": "bn",
    "Bodo": "brx",
    "Dogri": "doi",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Kashmiri": "ks",
    "Konkani": "kok",
    "Maithili": "mai",
    "Malayalam": "ml",
    "Manipuri": "mni",
    "Marathi": "mr",
    "Nepali": "ne",
    "Odia": "or",
    "Punjabi": "pa",
    "Sanskrit": "sa",
    "Santali": "sat",
    "Sindhi": "sd",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "English": "en"
}

language_options = list(indian_languages.keys())

# --- Page config ---
st.set_page_config(page_title="Communify AI", layout="centered")

# --- Main Intro Page ---
st.title("🌐 Communify AI")
st.markdown("""
In India, there are more than 20+ official languages spoken by millions of people.  
This vast linguistic diversity, while beautiful, often creates barriers in communication  
between communities of different regions and religions.

👉 **Communify AI** is a Python-powered Voice Translator designed to bridge this gap.  
It enables real-time speech-to-speech translation across major Indian languages,  
helping Indians connect, collaborate, and communicate seamlessly.
""")

st.info("Created by Mehul.k | mehulkrishieee@gmail.com")

# Demo button
if st.button("▶ Start Demo"):
    st.session_state.demo_started = True
else:
    if 'demo_started' not in st.session_state:
        st.session_state.demo_started = False

if st.session_state.demo_started:
    st.subheader("🌐 Select Languages")
    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("Source Language", options=language_options, index=language_options.index("English"))
    with col2:
        dest_lang = st.selectbox("Target Language", options=language_options, index=language_options.index("Tamil"))

    st.write("### 🎤 Voice-to-Voice Translator")
    st.write("Upload a WAV file of your voice to get translation.")

    uploaded_audio = st.file_uploader("Upload WAV file", type=["wav"])

    if st.button("🎤 Translate Voice"):
        if uploaded_audio is None:
            st.warning("Please upload a WAV file.")
        else:
            try:
                # Save uploaded file temporarily
                with NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(uploaded_audio.read())
                    tmp_path = tmp.name

                # Recognize speech
                with sr.AudioFile(tmp_path) as source:
                    audio_data = r.record(source)
                    speech_text = r.recognize_google(audio_data, language=indian_languages[src_lang])

                st.text_area("Recognized Text:", value=speech_text, height=100)

                # Translate text
                translated = translator.translate(speech_text, src=indian_languages[src_lang], dest=indian_languages[dest_lang])
                st.text_area("Translated Text:", value=translated.text, height=100)

                # Convert translation to speech
                tts = gTTS(translated.text, lang=indian_languages[dest_lang])
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)

                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.error(f"Error: {e}")
