import asyncio
from edge_tts import Communicate

async def speak_async(text):
    communicate = Communicate(text, voice="en-US-AriaNeural")
    await communicate.run()

def speak(text):
    print(f"🔊 Speaking: {text}")
    asyncio.run(speak_async(text))

if __name__ == "__main__":
    speak("Hello! I'm your CARE agent. How are you feeling today?")
