import streamlit as st

# Official Indian Languages + English
language_options = [
    "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada",
    "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi",
    "Nepali", "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil",
    "Telugu", "Urdu", "English"
]

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

# --- Demo button ---
if st.button("▶ Start Demo"):
    st.session_state.demo_started = True
else:
    if 'demo_started' not in st.session_state:
        st.session_state.demo_started = False

# --- Language selection UI ---
if st.session_state.demo_started:
    st.subheader("🌐 Select Languages")

    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("Source Language", options=language_options, index=language_options.index("English"))
    with col2:
        dest_lang = st.selectbox("Target Language", options=language_options, index=language_options.index("Tamil"))

    st.write("### 🎤 Voice-to-Voice Translator")
    st.write("Upload a voice file (WAV format) or click a button to record your voice.")

    # --- Frontend placeholders ---
    st.file_uploader("Upload a voice file (WAV format)", type=["wav"])
    st.button("🎤 Translate Voice")

    st.text_area("Recognized Text:", value="", height=100)
    st.text_area("Translated Text:", value="", height=100)
