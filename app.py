from flask import Flask, render_template, Response
import cv2
import time
import random
import threading

from core.voice_input import record_audio, transcribe_audio  # import from core

app = Flask(__name__)
camera = cv2.VideoCapture(0)

last_check = time.time()
CHECK_INTERVAL = 5  # seconds
latest_transcript = ""

# Load OpenCV's pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
emotions = ['happy', 'sad', 'neutral', 'angry', 'surprised']

def voice_loop():
    global latest_transcript
    while True:
        try:
            print("🎙 Listening...")
            audio = record_audio()
            print("🧠 Transcribing...")
            text = transcribe_audio(audio)
            print("You said:", text)
            latest_transcript = text
        except Exception as e:
            print("Voice error:", e)
            time.sleep(2)

def gen_frames():
    global last_check
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            now = time.time()
            if now - last_check >= CHECK_INTERVAL:
                last_check = now
                for (x, y, w, h) in faces:
                    emotion = random.choice(emotions)  # Simulated
                    print(f"Detected face at ({x},{y},{w},{h}) - Emotion: {emotion}")

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Display transcript text on frame
            y0, dy = 30, 30
            for i, line in enumerate(latest_transcript.splitlines()):
                y = y0 + i * dy
                cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_voice_thread():
    thread = threading.Thread(target=voice_loop, daemon=True)
    thread.start()

if __name__ == '__main__':
    start_voice_thread()
    app.run(debug=True)
