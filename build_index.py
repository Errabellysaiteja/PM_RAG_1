import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_vector_store(json_filepath="scraped_catalog_data.json", persist_directory="./chroma_db"):
    # 1. Load the structured JSON data
    print("Loading catalog data...")
    try:
        with open(json_filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_filepath} not found. Did you run the ingestion script?")
        return

    # 2. Convert JSON into LangChain Document objects with Metadata
    # This is crucial for the citation requirement!
    documents = []
    for item in data:
        doc = Document(
            page_content=item["content"],
            metadata={
                "url": item["url"],
                "category": item["category"],
                "note": item["note"]
            }
        )
        documents.append(doc)

    # 3. Apply the Chunking Strategy
    print("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""] # Try to split on paragraphs/sentences first
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} pages.")

    # 4. Initialize the free HuggingFace Embeddings
    print("Initializing HuggingFace Embeddings (all-MiniLM-L6-v2)...")
    # This will download the model to your machine the first time you run it
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 5. Build and Save the Chroma Vector Store
    print("Building Chroma vector store. This might take a minute or two...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    print(f"✅ Vector store successfully built and saved to {persist_directory}/")

if __name__ == "__main__":
    build_vector_store()