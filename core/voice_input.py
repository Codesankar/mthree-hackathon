import os
from dotenv import load_dotenv
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

model = whisper.load_model("base")  

def record_audio(duration=5, samplerate=16000):
    print("🎙 Listening...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return np.squeeze(audio)

def transcribe_audio(audio, samplerate=16000):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        scipy.io.wavfile.write(f.name, samplerate, audio)
        print("🧠 Transcribing...")
        result = model.transcribe(f.name)
        return result["text"]

def listen_and_transcribe():
    audio = record_audio()
    return transcribe_audio(audio)

if __name__ == "__main__":
    text = listen_and_transcribe()
    print("You said:", text)
