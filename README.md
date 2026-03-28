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

**1. Install Dependencies**

```bash
pip install -r requirements.txt
```
**2. Environment Variables**


Linux / macOS
```bash
export MISTRAL_API_KEY="your_api_key_here"
```

Windows (PowerShell)
```bash
$env:MISTRAL_API_KEY="your_api_key_here"
```

**3. Run the pipeline**
```bash
# Step 1: Parse the local PDF and generate structured JSON with virtual URLs
python ingest_local_pdf.py

# Step 2: Chunk the text, generate embeddings, and build the local Chroma database
python build_index.py

# Step 3: Launch the interactive Course Planning Assistant
python rag_agent.py
```


