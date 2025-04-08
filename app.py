from flask import Flask, render_template, Response
import cv2
from deepface import DeepFace
import time
from datetime import datetime

app = Flask(__name__)
camera = cv2.VideoCapture(0)

last_check = time.time()
CHECK_INTERVAL = 5  # seconds

def gen_frames():
    global last_check
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            now = time.time()

            if now - last_check >= CHECK_INTERVAL:
                last_check = now
                try:
                    # Analyze emotions using DeepFace
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                    if isinstance(result, list):
                        result = result[0]
                    emotion = result["dominant_emotion"]
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Dominant Emotion: {emotion}")
                except Exception as e:
                    print(f"Emotion detection failed: {e}")

            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
