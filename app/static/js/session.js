// Initialize Socket.io
const socket = io();

socket.on('connect', () => {
    console.log("Connected to Sensei server via Multimodal Vosk pipeline.");
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
    
    // Reset UI for the new word
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
 * Sends the audio blob to the server.
 * Called by recorder.js upon stopRecording().
 */
function sendAudioToServer(audioBlob, currentWordId) {
    socket.emit('submit_audio', {
        audio: audioBlob,
        word_id: currentWordId
    });
}

/**
 * Handles the AI evaluation result (Vosk + Levenshtein + TTS)
 */
socket.on('evaluation_result', (data) => {
    const feedbackEl = document.getElementById('sensei-feedback');
    const scoreEl = document.getElementById('score-display');
    const transEl = document.getElementById('user-transcription');
    const nextBtn = document.getElementById('next-btn');
    
    // 1. Update Text UI
    feedbackEl.innerText = data.message;
    scoreEl.innerText = `Score: ${(data.score * 100).toFixed(0)}%`;
    transEl.innerText = `Sensei heard: "${data.user_transcription}"`;
    
    // 2. Play Sensei's Voice (Multimodal Output)
    if (data.audio_url) {
        const audio = new Audio(data.audio_url);
        audio.play().catch(e => console.error("Audio playback failed:", e));
    }

    // 3. Research Debugging (Visible in F12 Console)
    if (data.debug) {
        console.group("Sensei Evaluation Trace");
        console.log("Raw STT:", data.debug.raw_stt);
        console.log("Normalized Input:", data.debug.normalized_input);
        console.log("Target Phonetic:", data.debug.target_phonetic);
        console.log("Distance Logic:", data.debug.file_size_bytes, "bytes processed in", data.debug.proc_time);
        console.groupEnd();
    }
    
    // 4. Flow Control: Enable "Next" button only after result is in
    if (nextBtn) {
        nextBtn.disabled = false;
    }

    // 5. Re-enable the record button
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