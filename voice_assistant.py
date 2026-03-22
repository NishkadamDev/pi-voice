import speech_recognition as sr
import pyttsx3
import requests

# ── Configuration ─────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"
WAKE_WORD = "hello"

# Test to sync to gitbub number 2
# ── Set up text-to-speech ──────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

def speak(text):
    print(f"🤖 Ace says: {text}\n")
    engine.say(text)
    engine.runAndWait()

# ── Set up speech recognition ──────────────────────────────────
recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=1)

def listen(timeout=5):
    with mic as source:
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
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
        return "I can't reach Ollama. Make sure it's running with: ollama serve"
    except Exception as e:
        return f"Something went wrong: {e}"

# ── Main loop ──────────────────────────────────────────────────
print("🎙️  Calibrating microphone...")
with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)

print(f"✅ Ace is ready! Say 'Ace' to wake me up.")
print("   Press Ctrl+C to stop.\n")

while True:
    try:
        print("💤 Waiting for wake word...")
        heard = listen(timeout=10)

        if heard is None:
            continue

        print(f"   Heard: {heard}")

        if WAKE_WORD not in heard:
            continue

        print(f"✅ Wake word detected!")
        speak("Yeah?")

        print("👂 Listening for your question...")
        question = listen(timeout=7)

        if question is None:
            speak("I didn't catch that. Say Ace again when you're ready.")
            continue

        print(f"🗣️  You asked: {question}\n")

        if any(word in question for word in ["stop", "exit", "quit", "goodbye", "bye"]):
            speak("See you later!")
            break

        reply = ask_ollama(question)
        speak(reply)

    except KeyboardInterrupt:
        print("\n👋 Ace signing off. Bye!")
        break
