import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()
EMBEDDINGS_MODEL = os.getenv("OPENAI_EMBEDDINGS_MODEL")
client = OpenAI()
embedding_function = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)
chroma = Chroma(
    collection_name="book_summaries",
    embedding_function=embedding_function,
    persist_directory="./chroma_db",
)


def load_summaries(file_path):
    # Load book summaries from the txt file.
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    docs = []
    title = None
    summary_lines = []
    for line in lines:
        if line.startswith("## Title:"):
            if title and summary_lines:
                docs.append(
                    {"title": title.strip(), "summary": " ".join(summary_lines).strip()}
                )
                summary_lines = []
            title = line.replace("## Title:", "").strip()
        elif line.strip():
            summary_lines.append(line.strip())
    if title and summary_lines:
        docs.append(
            {"title": title.strip(), "summary": " ".join(summary_lines).strip()}
        )
    return docs


def ingest_to_chromadb(docs):
    # Ingest documents into ChromaDB vector store.
    global chroma
    documents = []
    for doc in docs:
        documents.append(
            Document(page_content=doc["summary"], metadata={"title": doc["title"]})
        )
    chroma = Chroma.from_documents(
        documents,
        embedding_function,
        persist_directory="./chroma_db",
        collection_name="book_summaries",
    )


def semantic_search(query, n_results=3):
    # Semantic search for book summaries.
    results = chroma.similarity_search(query, k=n_results)
    docs = [r.page_content for r in results]
    metas = [r.metadata for r in results]
    return docs, metas


if __name__ == "__main__":
    docs = load_summaries("book_summaries.txt")
    ingest_to_chromadb(docs)
