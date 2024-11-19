const video = document.getElementById('video');
const recordButton = document.getElementById('record');
const analyzeButton = document.getElementById('analyze');
const resultDiv = document.getElementById('result');

let mediaRecorder;
let recordedChunks = [];

// Access the webcam
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // Initialize MediaRecorder for recording
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = function (event) {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        // When recording is stopped
        mediaRecorder.onstop = async function () {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            recordedChunks = [];

            // Create a FormData object to send the video to the server
            const formData = new FormData();
            formData.append('video', blob);

            // Enable the analyze button
            analyzeButton.disabled = false;

            // Send video to server for analysis
            analyzeButton.onclick = async function () {
                resultDiv.textContent = 'Analyzing...';

                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    resultDiv.textContent = `Analysis Result: ${result.expression}`;
                } catch (error) {
                    console.error('Error analyzing video:', error);
                    resultDiv.textContent = 'Error analyzing video.';
                }
            };
        };
    } catch (error) {
        console.error('Error accessing webcam:', error);
        alert('Webcam access denied.');
    }
}

// Start/stop recording on button click
recordButton.onclick = function () {
    if (mediaRecorder.state === 'inactive') {
        recordedChunks = [];
        mediaRecorder.start();
        recordButton.textContent = 'Stop Recording';
        analyzeButton.disabled = true;
    } else {
        mediaRecorder.stop();
        recordButton.textContent = 'Start Recording';
    }
};

// Initialize webcam when the page loads
window.onload = startWebcam;
