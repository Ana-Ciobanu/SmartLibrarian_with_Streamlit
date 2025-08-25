import os
from dotenv import load_dotenv
import streamlit as st
from rag_ingest_and_search import semantic_search
from utils import contains_offensive_language, generate_book_image, chatgpt_response, text_to_speech, play_audio_autoplay
from openai import OpenAI
from better_profanity import profanity

load_dotenv()
IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL")
TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL")

client = OpenAI()

profanity.load_censor_words()

st.set_page_config(page_title="Smart Librarian", layout="centered")
st.title("Smart Librarian – AI Book Recommender")

user_query = st.text_input("Enter your interests, themes, or keywords to get book recommendations.", "")

if user_query:
    if contains_offensive_language(user_query):
        st.warning("I'm here to help, but please avoid using inappropriate language.")
    else:
        # Only run search and generate new recommendation if the query changed
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

            # Only generate response if not already cached for this title
            if st.session_state.get("last_title") != meta['title']:
                with st.spinner("Getting AI recommendation..."):
                    st.session_state.response = chatgpt_response(user_query, meta['title'], client, TEXT_MODEL)
                st.session_state.last_title = meta['title']

            response = st.session_state.get("response")

            if st.button("🔊 Listen to the recommendation"):
                audio_file = text_to_speech(response)
                st.audio(audio_file, format="audio/mp3")

            st.markdown(response)

            # Only generate image if not already cached for this title
            if st.session_state.img_url is None:
                book_theme = doc if doc else meta['title']
                with st.spinner("Generating image..."):
                    st.session_state.img_url = generate_book_image(meta['title'], book_theme, client, IMAGE_MODEL)

            st.image(st.session_state.img_url, caption=f"Suggested cover or scene for '{meta['title']}'", use_container_width=True)
        else:
            st.info("No matching books found.")
else:
    st.info("Type your interests above and press Enter.")
