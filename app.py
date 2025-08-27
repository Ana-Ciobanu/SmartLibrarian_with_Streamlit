import os
from dotenv import load_dotenv
import streamlit as st
from rag_ingest_and_search import semantic_search
from utils import contains_offensive_language, generate_book_image, chatgpt_response, text_to_speech
from openai import OpenAI
from better_profanity import profanity
import streamlit.components.v1 as components

load_dotenv()
IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL")
TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL")

client = OpenAI()
profanity.load_censor_words()

st.set_page_config(page_title="Smart Librarian", layout="centered")
st.title("Smart Librarian – AI Book Recommender")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_query" not in st.session_state:
    st.session_state.voice_query = ""

if "mic_clicked" not in st.session_state:
    st.session_state.mic_clicked = False

# JavaScript-based voice input integration (separated behavior)
components.html("""
    <div style="margin-bottom: 10px;">
        <button onclick="startVoiceRecognition()" style="padding:10px 16px;font-size:16px;cursor:pointer;">🎤 Speak your question</button>
    </div>
    <script>
        function startVoiceRecognition() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onresult = function (event) {
                const transcript = event.results[0][0].transcript;
                const input = window.parent.document.querySelector('textarea');
                if (input) {
                    input.value = transcript;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
                const micFlag = window.parent.document.querySelector("#mic-flag");
                if (micFlag) micFlag.value = "spoken";
            };

            recognition.onspeechend = function () {
                recognition.stop();
            };

            recognition.onerror = function (event) {
                alert("Speech recognition error: " + event.error);
            };

            recognition.start();

            const micFlag = window.parent.document.querySelector("#mic-flag");
            if (micFlag) micFlag.value = "clicked";
        }
    </script>
    <input type="hidden" id="mic-flag" name="mic-flag" value="" />
""", height=140)

# Input form
with st.form("query_form"):
    user_query = st.text_area(
        "Enter your interests, themes, or keywords to get book recommendations.",
        value=st.session_state.voice_query
    )
    submit = st.form_submit_button("🔍 Submit")

# Only update session state when the user submits
if submit:
    st.session_state.voice_query = user_query  # Save the latest input (including edits)
    # Now use st.session_state.voice_query for further processing
    query_to_use = st.session_state.voice_query
    if not query_to_use.strip():
        st.warning("Please enter a query or use the microphone.")
    elif contains_offensive_language(query_to_use):
        st.warning("I'm here to help, but please avoid using inappropriate language.")
    else:
        if st.session_state.get("last_query") != user_query:
            with st.spinner("Searching for books..."):
                docs, metas = semantic_search(user_query)
            st.session_state.docs = docs
            st.session_state.metas = metas
            st.session_state.last_query = user_query
            st.session_state.response = None
            st.session_state.img_url = None
            st.session_state.last_title = None

        docs = st.session_state.get("docs")
        metas = st.session_state.get("metas")

        st.subheader("Recommended Book:")
        if metas and docs:
            meta = metas[0]
            doc = docs[0]

            if st.session_state.get("last_title") != meta['title']:
                with st.spinner("Getting AI recommendation..."):
                    st.session_state.response = chatgpt_response(user_query, meta['title'], client, TEXT_MODEL)
                st.session_state.last_title = meta['title']

            response = st.session_state.get("response")

            if not st.session_state.messages or st.session_state.messages[-1].get("content") != user_query:
                st.session_state.messages.append({"role": "user", "content": user_query})
                st.session_state.messages.append({"role": "bot", "content": response})

            if st.button("🔊 Listen to the recommendation"):
                audio_file = text_to_speech(response)
                st.audio(audio_file, format="audio/mp3")

            st.markdown(response)

            if st.session_state.img_url is None:
                book_theme = doc if doc else meta['title']
                with st.spinner("Generating image..."):
                    st.session_state.img_url = generate_book_image(meta['title'], book_theme, client, IMAGE_MODEL)

            st.image(st.session_state.img_url, caption=f"Suggested cover or scene for '{meta['title']}'", use_container_width=True)
        else:
            st.info("No matching books found.")

    st.markdown("---")
    st.subheader("Conversation History")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Smart Librarian:** {msg['content']}")
else:
    st.info("Type your interests above, speak into the mic, and then click Submit.")