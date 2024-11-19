import os
import numpy as np
import cv2
from keras.models import load_model

# Load the pre-trained model for facial expression detection
# Replace 'your_model.h5' with the path to your trained model
model = load_model('your_model.h5')

# Define the class labels for the model
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

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

if __name__ == '__main__':
    # Provide the path to the video file you want to analyze
    test_video_path = 'test_cap.mov'  # Replace with the path to your video file

    if os.path.exists(test_video_path):
        # Analyze the video
        result = analyze_video(test_video_path)
        print(f"Analysis Result: {result}")
    else:
        print(f"Video file not found at {test_video_path}")
