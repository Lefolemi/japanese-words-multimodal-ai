let mediaRecorder;
let audioChunks = [];

/**
 * Initializes the microphone and starts recording.
 * Uses MediaRecorder with a timeslice for more reliable data capture.
 */
async function startRecording() {
    audioChunks = []; // Clear previous recording data
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Standard webm format
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            // 1. Check if we actually captured chunks
            if (audioChunks.length === 0) {
                console.error("No audio chunks captured.");
                updateUI('idle');
                return;
            }

            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

            // 2. Validate blob size (WebM headers are usually > 100 bytes)
            if (audioBlob.size < 100) {
                console.error("Audio blob too small, likely empty.");
                updateUI('idle');
            } else {
                console.log("Recording stopped. Sending blob. Size:", audioBlob.size);
                const currentWordId = document.getElementById('current-word-id').value;

                if (typeof sendAudioToServer === "function") {
                    sendAudioToServer(audioBlob, currentWordId);
                } else {
                    console.error("sendAudioToServer is not defined in session.js");
                    updateUI('idle');
                }
            }
            
            // 3. Cleanup: Stop all tracks to release the microphone
            stream.getTracks().forEach(track => track.stop());
        };

        // REQUEST DATA EVERY 100MS: This ensures data is pushed to chunks 
        // continuously rather than only at the very end.
        mediaRecorder.start(100); 
        
        console.log("MediaRecorder started with 100ms timeslices...");
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