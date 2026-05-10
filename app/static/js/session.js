// Initialize Socket.io
const socket = io();

socket.on('connect', () => {
    console.log("Connected to Sensei server via Whisper pipeline.");
});

/**
 * UI & NAVIGATION LOGIC
 */
function updateWordDisplay() {
    const word = sessionWords[currentIndex];
    
    // Update DOM elements
    document.getElementById('current-word-id').value = word.id;
    document.getElementById('word-kanji').innerText = word.original;
    document.getElementById('word-furigana').innerText = word.furigana;
    document.getElementById('word-english').innerText = word.english;
    
    // Reset Sensei feedback for the new word
    document.getElementById('score-display').innerText = "Score: --%";
    document.getElementById('sensei-feedback').innerText = "Ready for your pronunciation.";
    document.getElementById('user-transcription').innerText = "";

    // Update Progress counter
    document.getElementById('progress-text').innerText = `${currentIndex + 1} / ${sessionWords.length}`;

    // Toggle Navigation Buttons
    document.getElementById('prev-btn').disabled = (currentIndex === 0);
    document.getElementById('next-btn').innerText = (currentIndex === sessionWords.length - 1) ? "Finish" : "Next";
    
    // Reset recorder UI state
    if (typeof updateUI === "function") {
        updateUI('idle');
    }
}

function nextWord() {
    if (currentIndex < sessionWords.length - 1) {
        currentIndex++;
        updateWordDisplay();
    } else {
        // Redirect to main menu or results page
        window.location.href = "/"; 
    }
}

function prevWord() {
    if (currentIndex > 0) {
        currentIndex--;
        updateWordDisplay();
    }
}

/**
 * COMMUNICATION LOGIC (The "Multimodal" Bridge)
 */

/**
 * Sends the audio blob to the Flask-SocketIO server.
 * Called by recorder.js upon mouseup/touchend.
 */
function sendAudioToServer(audioBlob, currentWordId) {
    // Ensure the payload matches the backend expectations
    socket.emit('submit_audio', {
        audio: audioBlob, // The actual binary data
        word_id: currentWordId
    });
}

/**
 * Handles the AI evaluation result from Whisper + Levenshtein
 */
socket.on('evaluation_result', (data) => {
    const feedbackEl = document.getElementById('sensei-feedback');
    const scoreEl = document.getElementById('score-display');
    const transEl = document.getElementById('user-transcription');
    
    feedbackEl.innerText = data.feedback_msg;
    scoreEl.innerText = `Score: ${(data.score * 100).toFixed(0)}%`;
    transEl.innerText = `Sensei heard: "${data.user_transcription}"`;
    
    // Re-enable the record button
    if (typeof updateUI === "function") {
        updateUI('idle');
    }
});

/**
 * Global Error Handler
 */
socket.on('error', (err) => {
    console.error("Socket Error:", err);
    alert("Sensei encountered an error: " + err.message);
    if (typeof updateUI === "function") {
        updateUI('idle');
    }
});

// Initialize display on load
document.addEventListener('DOMContentLoaded', updateWordDisplay);