# 🎙️ Pi Voice — Meet Ace

> A fully offline voice assistant running on a Raspberry Pi 5. Speak a question, hear an answer — no internet required.

---

## 🧠 About This Project

**Pi Voice** is a local voice assistant named **Ace** that runs entirely on a Raspberry Pi 5. It listens through a microphone, sends your question to a local Gemma AI model via Ollama, and speaks the answer back using text-to-speech — all without touching the internet.

It started with a wake word system, evolved into a continuous listener, and the final experiment? Getting **two Raspberry Pis to talk to each other**.

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| **Hardware** | Raspberry Pi 5 + Microphone |
| **Local AI Runtime** | Ollama |
| **Model** | Gemma 3 (1B) |
| **Speech Recognition** | `speech_recognition` + Google Speech API |
| **Text-to-Speech** | `pyttsx3` |
| **AI Assist** | Claude (Anthropic), Gemini (Google) |
| **Language** | Python |

---

## ⚙️ How It Works

1. **Listen** — The Pi microphone picks up your voice using `speech_recognition`
2. **Transcribe** — Google Speech API converts audio to text
3. **Think** — The text is sent to Gemma 3 running locally via Ollama
4. **Speak** — `pyttsx3` reads the response aloud as Ace's voice
5. **Loop** — Ace keeps listening until you say *"goodbye"*

---

## 🤖 Ace in Action

```
🎙️  Calibrating microphone...
✅ Ace is ready! Just speak your question.
   Say 'goodbye' to quit. Press Ctrl+C to force stop.

🤖 Ace says: Hello! I'm ready. What would you like to know?

👂 Listening...
🗣️  You asked: what is the speed of light?

🧠 Thinking (gemma3:1b)...
🤖 Ace says: The speed of light is approximately 299,792 kilometres per second in a vacuum.
```

---

## 🧪 Experiments Along the Way

| Version | What Changed |
|---|---|
| v1 | Basic listen → think → speak loop |
| v2 | Added a wake word to trigger listening |
| v3 | Removed wake word for continuous listening |
| v4 *(attempted)* | Two Raspberry Pis talking to each other |

The two-Pi experiment — where one Pi asks questions and the other answers — was the most ambitious idea. Getting there is still in progress.

---

## 💡 Key Learnings

- Integrating microphone input and speaker output in Python
- Stripping markdown from AI responses before text-to-speech (asterisks and headers sound terrible spoken aloud)
- Managing ambient noise calibration for reliable speech recognition
- How to query a local Ollama model via HTTP from Python
- The challenges of real-time audio pipelines on low-power hardware

---

## 🚀 Part of the AI Bootcamp

This project was built during the **Week 2 Physical AI** phase of a 15-day AI Developer Bootcamp.  
See the full bootcamp repo → [The AI Bootcamp](../README.md)

---

*Ace is always listening. Always thinking. Always ready.* 🎙️🧠
