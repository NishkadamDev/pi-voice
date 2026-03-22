import speech_recognition as sr
import pyttsx3
import requests
import re
import time

# ── Configuration ─────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

# ── Set up text-to-speech ──────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

def speak(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+\s?', '', text)
    text = re.sub(r'`+', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\n+', ' ', text)
    text = text.strip()
    print(f"🤖 Ace says: {text}\n")
    engine.say(text)
    engine.runAndWait()

# ── Set up speech recognition ──────────────────────────────────
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen(timeout=10):
    with mic as source:
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=20)
        except sr.WaitTimeoutError:
            return None

    try:
        text = recognizer.recognize_google(audio).lower()
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"   Speech API error: {e}")
        return None

# ── Send text to Ollama ────────────────────────────────────────
def ask_ollama(prompt):
    print(f"🧠 Thinking ({MODEL})...")
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        return response.json().get("response", "I have no response.")
    except requests.exceptions.ConnectionError:
        return "I can't reach Ollama. Make sure it's running with ollama serve"
    except Exception as e:
        return f"Something went wrong: {e}"

# ── Main loop ──────────────────────────────────────────────────
print("🎙️  Calibrating microphone...")
with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1

print("✅ Ace is ready! Just speak your question.")
print("   Say 'goodbye' to quit. Press Ctrl+C to force stop.\n")
speak("Hello! I'm ready. What would you like to know?")

while True:
    try:
        print("👂 Listening...")
        question = listen(timeout=10)

        if question is None:
            print("   Nothing heard, still listening...\n")
            continue

        print(f"🗣️  You asked: {question}\n")

        if any(word in question for word in ["stop", "exit", "quit", "goodbye", "bye"]):
            speak("See you later!")
            break

        reply = ask_ollama(question)
        speak(reply)
        time.sleep(1)

    except KeyboardInterrupt:
        print("\n👋 Ace signing off. Bye!")
        break