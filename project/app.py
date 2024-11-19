from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# Load the pre-trained model for facial expression detection
# Replace 'your_model.h5' with the path to your trained model
model = load_model('your_model.h5')

# Define the class labels for the model
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Create a folder to store uploaded videos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def analyze_video(video_path):
    # Load video using OpenCV
    cap = cv2.VideoCapture(video_path)
    emotions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess frame (resize, convert to grayscale, etc.)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (48, 48))
        normalized_frame = resized_frame / 255.0
        reshaped_frame = np.reshape(normalized_frame, (1, 48, 48, 1))

        # Predict emotion
        prediction = model.predict(reshaped_frame)
        emotion_index = np.argmax(prediction)
        emotion = emotion_labels[emotion_index]
        emotions.append(emotion)

    cap.release()

    # Return the most frequent emotion detected
    if emotions:
        most_common_emotion = max(set(emotions), key=emotions.count)
        return most_common_emotion
    else:
        return "No face detected"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)

    # Analyze the video
    expression = analyze_video(video_path)

    # Return the result
    return jsonify({'expression': expression})

if __name__ == '__main__':
    app.run(debug=True)
