from flask import Flask, render_template, Response
import cv2
import numpy as np
import pyttsx3
from threading import Thread
from util import get_limits

app = Flask(__name__)
engine = pyttsx3.init()

# Define colors and their names
color_names = {
    'red': (0, 0, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'yellow': (0, 255, 255),
    'cyan': (255, 255, 0),
    'magenta': (255, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

def detect_color(hsv_image, color_name):
    lowerlimit, upperlimit = get_limits(color=color_name)
    mask = cv2.inRange(hsv_image, lowerlimit, upperlimit)
    return mask

def announce_colors(colors):
    if colors:
        color_names_str = ', '.join(set(colors))  # Use set to avoid repeating names
        engine.say(f"Detected colors: {color_names_str}")
        engine.runAndWait()

def gen_frames():  # generate frame by frame from camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Error: Could not open video capture.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        detected_colors = []

        for name, color in color_names.items():
            mask = detect_color(hsvImage, name)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Adjust area threshold as needed
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    detected_colors.append(name)

        if detected_colors:
            Thread(target=announce_colors, args=(detected_colors,)).start()
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
