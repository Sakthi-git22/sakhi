document.addEventListener("DOMContentLoaded", () => {
    const startRecordingButton = document.getElementById('start-recording');
    const answerTextarea = document.getElementById('answer');
    const statusMessage = document.getElementById('status');
    const video = document.getElementById('video');
    const analyzeButton = document.getElementById('analyze-btn');

    // Check if browser supports SpeechRecognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        startRecordingButton.addEventListener('click', () => {
            recognition.start();
            statusMessage.textContent = '🎙️ Listening... Please speak your answer.';
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            answerTextarea.value = transcript;
            statusMessage.textContent = '✅ Recording complete! You can edit your answer.';
        };

        recognition.onerror = (event) => {
            statusMessage.textContent = '❌ Error: ' + event.error;
        };

        recognition.onend = () => {
            statusMessage.textContent = '🎤 Recording stopped.';
        };
    } else {
        statusMessage.textContent = '⚠️ Your browser does not support voice input.';
        startRecordingButton.disabled = true;
    }

    // Start Video Stream
    async function startVideo() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            video.play();
            statusMessage.textContent = '✅ Camera is active.';
            analyzeButton.disabled = false;
            startRecordingButton.disabled = false;
        } catch (error) {
            console.error('❌ Camera Error: ', error);
            statusMessage.textContent = '❌ Camera access failed. Allow permissions & retry.';
        }
    }

    startVideo();
});
