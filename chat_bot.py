# --- Python 3.13 Audio Patch ---
# import audioop_lts
# import sys; sys.modules['audioop'] = audioop_lts
# -------------------------------
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
from google import genai

def speak(text):
    print(f"Echo: {text}") # Still print it so you can read it
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("\nListening... (Speak now)")
        # Helps filter out background fan/ac noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # Listens for up to 5 seconds
            audio = recognizer.listen(source, timeout=5)
            # Converts audio to text
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except:
            # If it hears nothing or crashes, return empty
            return ""

load_dotenv()
API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)

# Setup Text-to-Speech
engine = pyttsx3.init()
# Optional: Speed up the voice slightly
engine.setProperty('rate', 170) 

# Setup Speech-to-Text
recognizer = sr.Recognizer()

chat = client.chats.create(
    model="gemini-flash-latest",
    config={"system_instruction": "You are an assistant named Atlas"}
)

print("Atlas: Hey! How are you? How is it going? Want some help?")
print("Type 'quit' or 'exit' to exit")

speak("System online. I am listening.")

while True:
    # 1. Listen instead of typing
    user_input = listen()

    # 2. If mic heard nothing, skip this loop iteration
    if not user_input:
        continue

    # 3. Check for exit
    if "quit" in user_input.lower() or "exit" in user_input.lower():
        speak("Goodbye!")
        break
    
    # 4. Chat and Speak
    try:
        response = chat.send_message(user_input)
        speak(response.text)
    except Exception as e:
        speak("I had trouble connecting.")
        print(f"Error: {e}")