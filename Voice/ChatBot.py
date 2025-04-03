import openai
import pyttsx3
import speech_recognition as sr
import serial
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=api_key)  # Replace with actual API key

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech rate

# Configure Serial Port (Update COM port for Windows or /dev/ttyUSB0 for Linux)
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # Allow connection

def speak(text):
    """Convert text to speech and control mouth movement."""
    ser.write(b'START\n')  # Signal Arduino to start mouth movement
    engine.say(text)
    engine.runAndWait()
    ser.write(b'STOP\n')  # Signal Arduino to stop movement

def listen():
    """Capture audio from microphone and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text[:500]  # Allow longer input (up to 500 characters)
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return None
    except sr.RequestError:
        print("Speech recognition service is unavailable")
        return None

def chat_with_gpt(prompt):
    """Send user input to OpenAI and return a longer, more detailed response."""
    retries = 3  # Retry logic for handling API rate limits
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Keep GPT-3.5
                messages=[{"role": "user", "content": prompt}],  # User input
                max_tokens=250  # Increased response length (now up to ~200 words)
            )
            return response.choices[0].message.content.strip()  # Strip unnecessary spaces
        except openai.RateLimitError:
            print(f"Rate limit exceeded, retrying in 5 seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(5)  # Wait before retrying

    return "Sorry, I'm currently overloaded. Try again later."

# Main loop for conversation flow
while True:
    user_input = listen()
    if user_input:
        response = chat_with_gpt(user_input)
        print(f"GPT Response: {response}")
        speak(response)