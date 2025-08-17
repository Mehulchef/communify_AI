import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os
import threading

# Global variables
r = sr.Recognizer()
translator = Translator()

# --- Only include Official Indian Languages + English ---
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

language_options = sorted([(name, code) for name, code in indian_languages.items()])

selected_source_lang = ''
selected_dest_lang = ''

# --- Main Tkinter Setup ---
root = tk.Tk()
root.title("Communify AI - Voice Translator")
root.attributes('-fullscreen', True)
root.configure(bg="#ffffff")

# --- Screen 0: Main Intro Page ---
screen0 = tk.Frame(root, bg="#f0f8ff")
screen0.pack(fill="both", expand=True)

# Title
tk.Label(
    screen0,
    text="🌐 Communify AI",
    font=("Arial", 36, "bold"),
    bg="#f0f8ff",
    fg="#0078D7"
).pack(pady=60)

# Description
description = (
    "In India, there are more than 20+ official languages spoken by millions of people.\n"
    "This vast linguistic diversity, while beautiful, often creates barriers in communication\n"
    "between communities of different regions and religions.\n\n"
    "👉 Communify AI is a Python-powered Voice Translator designed to bridge this gap.\n"
    "It enables real-time speech-to-speech translation across major Indian languages,\n"
    "helping Indians connect, collaborate, and communicate seamlessly."
)

tk.Label(
    screen0,
    text=description,
    font=("Arial", 16),
    bg="#f0f8ff",
    fg="#333333",
    justify="center"
).pack(pady=40)

# Demo Button
def go_to_language_screen():
    screen0.pack_forget()
    screen1.pack(fill="both", expand=True)

tk.Button(
    screen0,
    text="▶ Start Demo",
    font=("Arial", 18, "bold"),
    bg="#0078D7",
    fg="white",
    padx=20,
    pady=10,
    command=go_to_language_screen
).pack(pady=30)

# Footer
tk.Label(
    screen0,
    text="Created by Mehul.k | mehulkrishieee@gmail.com",
    font=("Arial", 12, "italic"),
    bg="#f0f8ff",
    fg="#666666"
).pack(side="bottom", pady=20)

# --- Screen 1: Language Selection ---
screen1 = tk.Frame(root, bg="#ffffff")

tk.Label(screen1, text="🌐 Select Languages", font=("Arial", 28, "bold"), bg="#ffffff").pack(pady=50)

lang_frame = tk.Frame(screen1, bg="#ffffff")
lang_frame.pack()

tk.Label(lang_frame, text="Source Language:", font=("Arial", 16), bg="#ffffff").grid(row=0, column=0, padx=30, pady=20, sticky="e")
src_lang_combobox = ttk.Combobox(lang_frame, values=[name for name, _ in language_options], font=("Arial", 14), width=30, state="readonly")
src_lang_combobox.set("English")
src_lang_combobox.grid(row=0, column=1, padx=30, pady=20)

tk.Label(lang_frame, text="Target Language:", font=("Arial", 16), bg="#ffffff").grid(row=1, column=0, padx=30, pady=20, sticky="e")
dest_lang_combobox = ttk.Combobox(lang_frame, values=[name for name, _ in language_options], font=("Arial", 14), width=30, state="readonly")
dest_lang_combobox.set("Tamil")
dest_lang_combobox.grid(row=1, column=1, padx=30, pady=20)

def proceed_to_translator():
    global selected_source_lang, selected_dest_lang
    src_name = src_lang_combobox.get()
    dest_name = dest_lang_combobox.get()

    if not src_name or not dest_name:
        messagebox.showerror("Error", "Please select both languages.")
        return

    selected_source_lang = dict(language_options)[src_name]
    selected_dest_lang = dict(language_options)[dest_name]
    start_translator_screen()

tk.Button(screen1, text="Continue", font=("Arial", 16), bg="#0078D7", fg="white", command=proceed_to_translator)\
    .pack(pady=40)

# --- Screen 2: Translator Functionality ---
def start_translator_screen():
    screen1.pack_forget()

    def translate_and_speak():
        with sr.Microphone() as source:
            status_label.config(text="Listening...", fg="blue")
            try:
                audio = r.listen(source)
                speech_text = r.recognize_google(audio, language=selected_source_lang)
                input_text_box.delete(1.0, tk.END)
                input_text_box.insert(tk.END, speech_text)

                translated = translator.translate(speech_text, src=selected_source_lang, dest=selected_dest_lang)
                translated_text = translated.text
                output_text_box.delete(1.0, tk.END)
                output_text_box.insert(tk.END, translated_text)

                voice = gTTS(translated_text, lang=selected_dest_lang)
                voice.save("voice.mp3")
                playsound("voice.mp3")
                os.remove("voice.mp3")

                status_label.config(text="Done", fg="green")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand the speech.")
                status_label.config(text="Ready", fg="green")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not connect to the service.")
                status_label.config(text="Ready", fg="green")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                status_label.config(text="Ready", fg="green")

    def on_translate_click():
        threading.Thread(target=translate_and_speak).start()

    def go_back_home():
        screen2.pack_forget()
        input_text_box.delete(1.0, tk.END)
        output_text_box.delete(1.0, tk.END)
        status_label.config(text="Ready", fg="green")
        screen1.pack(fill="both", expand=True)

    global screen2
    screen2 = tk.Frame(root, bg="#f9f9f9")
    screen2.pack(fill="both", expand=True)

    tk.Label(screen2, text="🎤 Voice-to-Voice Translator", font=("Arial", 22, "bold"), bg="#f9f9f9").pack(pady=20)
    global status_label
    status_label = tk.Label(screen2, text="Ready", font=("Arial", 14), fg="green", bg="#f9f9f9")
    status_label.pack(pady=5)

    tk.Label(screen2, text="Recognized Text:", bg="#f9f9f9", anchor='w', font=("Arial", 12)).pack(fill="x", padx=40)
    global input_text_box
    input_text_box = scrolledtext.ScrolledText(screen2, height=4, font=("Arial", 12))
    input_text_box.pack(padx=40, fill="x")

    tk.Label(screen2, text="Translated Text:", bg="#f9f9f9", anchor='w', font=("Arial", 12)).pack(fill="x", padx=40, pady=(10, 0))
    global output_text_box
    output_text_box = scrolledtext.ScrolledText(screen2, height=4, font=("Arial", 12))
    output_text_box.pack(padx=40, fill="x")

    tk.Button(screen2, text="🎤 Speak & Translate", font=("Arial", 14), bg="#4CAF50", fg="white", command=on_translate_click)\
        .pack(pady=20)

    tk.Button(screen2, text="⏪ Exit to Home", font=("Arial", 12), bg="#d9534f", fg="white", command=go_back_home)\
        .pack(pady=10)

# --- Escape Key to Exit Fullscreen ---
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

root.mainloop()
