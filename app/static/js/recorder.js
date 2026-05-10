let mediaRecorder;
let audioChunks = [];

/**
 * Initializes the microphone and starts recording.
 * Uses MediaRecorder to capture raw audio for Whisper.
 */
async function startRecording() {
    audioChunks = []; // Clear previous recording data
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Standard webm format is best for Whisper
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const currentWordId = document.getElementById('current-word-id').value;

            console.log("Recording stopped. Blob size:", audioBlob.size);

            // Call the function in session.js to emit the blob
            if (typeof sendAudioToServer === "function") {
                sendAudioToServer(audioBlob, currentWordId);
            } else {
                console.error("sendAudioToServer is not defined in session.js");
                updateUI('idle');
            }
            
            // Stop all tracks to release the microphone
            stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.start();
        console.log("MediaRecorder started...");
        updateUI('recording');

    } catch (err) {
        console.error("Microphone access denied or error:", err);
        alert("Sensei needs microphone access to hear you.");
        updateUI('idle');
    }
}

/**
 * Stops the MediaRecorder, which triggers the onstop event.
 */
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        updateUI('processing');
    }
}

/**
 * UI State Toggler
 */
function updateUI(state) {
    const btn = document.getElementById('record-btn');
    if (!btn) return;

    if (state === 'recording') {
        btn.innerText = "Listening...";
        btn.classList.add('recording-active');
    } else if (state === 'processing') {
        btn.innerText = "Sensei is evaluating...";
        btn.disabled = true;
    } else {
        btn.innerText = "Hold to Speak";
        btn.disabled = false;
        btn.classList.remove('recording-active');
    }
}