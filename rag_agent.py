import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURATION ---
# Get your free key at: https://console.mistral.ai/
os.environ["MISTRAL_API_KEY"] = "Your API key here"

def format_docs_with_citations(docs):
    """Formats retrieved chunks to include their metadata URLs for strict citation."""
    formatted_text = ""
    for i, doc in enumerate(docs):
        # We append the chunk's URL so Mistral knows exactly where the info came from
        formatted_text += f"\n--- Source {i+1} (URL: {doc.metadata.get('url', 'Unknown')}) ---\n"
        formatted_text += doc.page_content
    return formatted_text

def build_rag_chain():
    print("Loading Chroma database...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # Retrieve the top 5 most relevant chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # Hooking up the official Mistral API!
    print("Connecting to Mistral API (open-mixtral-8x7b)...")
    llm = ChatMistralAI(model="open-mixtral-8x7b", temperature=0)

    # --- THE STRICT SYSTEM PROMPT ---
    # --- THE STRICT SYSTEM PROMPT ---
    template = """
    You are a strict, rules-bound Prerequisite & Course Planning Assistant for a university.
    You evaluate student queries STRICTLY and EXCLUSIVELY against the provided Context Documents. 
    
    CRITICAL DIRECTIVE: You have amnesia regarding all outside academic knowledge. UNDER NO CIRCUMSTANCES are you allowed to use your pre-trained knowledge to name courses, suggest sequences, or state policies that are not explicitly written in the Context Documents below.

    Rules:
    1. If the Context Documents do not contain the specific courses or rules needed to answer the question, you MUST abort and output EXACTLY: "I don't have that information in the provided catalog/policies. Please consult an academic advisor."
    2. Do not invent course numbers, guess prerequisites, or assume major progressions.
    3. Every single claim or suggested course MUST be backed by a direct citation using the provided Source URLs.

    Context Documents:
    {context}

    Student Query: {question}

    You MUST structure your response exactly like this:
    Answer/Plan: [Your direct answer or course plan based ONLY on context]
    Why (requirements/prereqs satisfied): [Your reasoning backed by context]
    Citations: [Bullet list of URLs used for your answer]
    Clarifying questions (if needed): [Any missing info from the student, or "None"]
    Assumptions / Not in catalog: [List anything you had to refuse to answer, or "None"]
    """



    
    
    prompt = PromptTemplate.from_template(template)

    # Build the LangChain pipeline
    rag_chain = (
        {"context": retriever | format_docs_with_citations, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    print("Initializing Course Planning Assistant...")
    chain = build_rag_chain()
    
    print("\n" + "="*50)
    print("System Ready! Type your query (or 'quit' to exit).")
    print("="*50)
    
    while True:
        user_query = input("\nStudent: ")
        if user_query.lower() in ['quit', 'exit', 'q']:
            break
            
        print("\nMistral is thinking and searching the catalog...")
        response = chain.invoke(user_query)
        print("\n--- ASSISTANT RESPONSE ---")
        print(response)
        print("-" * 26)
