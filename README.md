# AI/ML Engineer Intern Assessment: Course Planning Assistant

This repository contains a Retrieval-Augmented Generation (RAG) system built for the Purple Merit Technologies AI/ML Engineer Intern Assessment (Option 1). 

The system acts as a strict, rule-bound Prerequisite & Course Planning Assistant. It ingests an academic catalog (PDF), builds a local vector database, and uses the Mistral LLM to answer student queries. It features aggressive prompt-level guardrails to prevent hallucination, ensuring every claim is backed by a specific citation and safely abstaining when information is missing.

## 🛠️ Architecture & Tech Stack
* **Orchestration:** LangChain (LCEL)
* **LLM:** Mistral (`open-mixtral-8x7b`) via official API
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`) via `sentence-transformers`
* **Vector Store:** ChromaDB (Local)
* **Ingestion:** `PyPDF2` with custom chunking (`RecursiveCharacterTextSplitter`)

## 🚀 Setup & Execution

## 1. Install Dependencies

```bash
pip install -r requirements.txt

2. Environment Variables

Linux / macOS
export MISTRAL_API_KEY="your_api_key_here"
Windows (PowerShell)
$env:MISTRAL_API_KEY="your_api_key_here"


