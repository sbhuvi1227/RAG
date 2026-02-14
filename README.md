Enhanced College FAQ Chatbot (Hybrid RAG + Web Search)
🚀 Overview

This project is an Enhanced College FAQ Chatbot built using:

✅ Local Document RAG (Chroma + HuggingFace Embeddings)

✅ Smart Similarity Threshold Detection

✅ Automatic Web Search Fallback (DuckDuckGo)

✅ Groq LLM (LLaMA 3 via OpenAI-compatible endpoint)

✅ Streamlit UI

The system first searches the local college document database.
If relevant information is not found, it automatically performs a web search and generates an answer from online results.

User Query
    ↓
Local Vector DB (Chroma)
    ↓
Similarity Score Check
    ↓
If Relevant → Local RAG Answer
If Not Relevant → Web Search RAG
    ↓
Groq LLM Generates Final Answer
    ↓
Streamlit UI


⚙️ Technologies Used

Python 3.11

LangChain

ChromaDB

HuggingFace Embeddings (all-MiniLM-L6-v2)

Groq API (LLaMA 3.1 8B Instant)

DuckDuckGo Search

Streamlit


🔍 How It Works
🟢 Local RAG

Converts college_info.txt into embeddings

Stores in ChromaDB

Retrieves top similar documents

Checks similarity score

If score is good → answer generated locally

🔵 Web Search RAG

Triggered when similarity score is low

Uses DuckDuckGo search

Feeds search results into Groq LLM

Generates answer from web data

🎯 Key Features

Hybrid Retrieval Architecture

Smart Fallback Mechanism

Groq LLM Integration

Production-Ready Structure

Clean Streamlit UI

Extensible Design
