import streamlit.components.v1 as components


def voice_input():
    voice_html = """
    <style>
    .voice-form-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
    }
    .voice-btn {
        background: #0A400C;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 32px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: background 0.2s;
    }
    .voice-btn:hover {
        background: #819067;
    }
    .voice-input {
        width: 320px;
        padding: 10px;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .voice-label {
        font-size: 1rem;
        color: #333;
        margin-bottom: 4px;
    }
    .voice-instruction {
        font-size: 0.98rem;
        color: #555;
        margin-top: 2px;
        text-align: center;
    }
    </style>
    <script>
    let recognition;
    function startRecognition() {
        if (!('webkitSpeechRecognition' in window)) {
            document.getElementById('voice_text').value = "Speech recognition not supported";
            return;
        }
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('voice_text').value = transcript;
        };
        recognition.onerror = function(event) {
            document.getElementById('voice_text').value = "Error: " + event.error;
        };
        recognition.start();
    }
    </script>
    <div class="voice-form-container">
      <button class="voice-btn" onclick="startRecognition()">🎤 Speak</button>
      <input type="text" id="voice_text" name="voice_text" class="voice-input" value="" placeholder="Your spoken text will appear here..." />
      <div class="voice-instruction">After speaking, copy the recognized text from the box above and paste it below.</div>
    </div>
    """
    components.html(voice_html, height=230)
