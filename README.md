# Smart Librarian – AI Book Recommender

<a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/python-3.13-blue" alt="Python Version"></a>
<a href="https://streamlit.io/" target="_blank"><img src="https://img.shields.io/badge/Streamlit-2.0+-green" alt="Streamlit"></a>
<a href="https://openai.com/" target="_blank"><img src="https://img.shields.io/badge/OpenAI-API-blue" alt="OpenAI"></a>

## Overview

Smart Librarian is a Streamlit-powered web app that recommends books based on your interests, themes, or keywords. It uses semantic search, OpenAI models, and AI-generated images to provide personalized book suggestions. You interact with the app by typing your query. The app also features text-to-speech for recommendations and maintains a conversation history.

## Features

- **Semantic Search:** Finds the best book matches for your query using vector embeddings.
- **AI Recommendations:** Generates friendly, conversational book suggestions using OpenAI's GPT models.
- **AI-Generated Images:** Visualizes book covers or scenes using DALL-E.
- **Text-to-Speech:** Listen to the AI recommendation.
- **Conversation History:** View your previous queries and responses.

## Technologies Used

- Python 3.13
- Streamlit
- OpenAI API (GPT, DALL-E)
- chromadb
- better_profanity
- gTTS

## Setup & Installation

1. **Clone the repository:**
    ```sh
    git clone <repo-url>
    cd SmartLibrarian_with_Streamlit
    ```

2. **Create a virtual environment (recommended):**
    ```sh
    python -m venv .venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

4. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Set up your `.env` file:**
    - Create a `.env` file in the project root and provide values for the following variables:
        ```
        OPENAI_EMBEDDINGS_MODEL=
        OPENAI_IMAGE_MODEL=
        OPENAI_TEXT_MODEL=
        ```
6. **Set up your OpenAI API key:** 
Make sure your OpenAI API key is set properly. Use `setx OPENAI_API_KEY "your-key"` on Windows.

## Running the App

1. **Ingest book summaries into the vector store (must be run once before using the app):**
    ```sh
    python rag_ingest_and_search.py
    ```

2. **Start the app:**
    ```sh
    streamlit run app.py
    ```

3. **Interact:**
    - Type your interests, themes, or keywords in the input box.
    - View the recommended book, listen to the recommendation, and see the AI-generated image.
    - Review your conversation history.

## File Structure

- `app.py` – Main Streamlit app.
- `utils.py` – Utility functions for AI, image generation, speech, and profanity filtering.
- `rag_ingest_and_search.py` – Semantic search and database ingestion.
- `book_summaries.txt` – Source book summaries.
- `complete_book_summaries.json` – Detailed book summaries.
- `.env` – Environment variables for model names.
- `requirements.txt` – Python dependencies.

## Troubleshooting

- Make sure your OpenAI API key is valid and set.
- If image generation fails, check your OpenAI quota and model settings.
- Ensure you run `rag_ingest_and_search.py` before using the app to populate the vector store.