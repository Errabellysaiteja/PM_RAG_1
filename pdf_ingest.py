import json
import requests
import PyPDF2
import io
from datetime import datetime

def ingest_pdf_to_json(pdf_url):
    print(f"Downloading Master Catalog from {pdf_url}...")
    response = requests.get(pdf_url)
    response.raise_for_status()
    
    print("Loading PDF into memory...")
    pdf_file = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(pdf_file)
    
    curated_data = []
    total_words = 0
    date_accessed = datetime.now().strftime("%Y-%m-%d")
    
    # We will parse the first 120 pages to guarantee we crush the 30,000 word limit
    pages_to_extract = min(120, len(reader.pages))
    
    print(f"Extracting and structuring text from {pages_to_extract} pages...")
    for i in range(pages_to_extract):
        text = reader.pages[i].extract_text()
        if text:
            word_count = len(text.split())
            total_words += word_count
            
            # We categorize the early pages as policy, and later pages as courses/programs
            category = "academic_policies" if i < 30 else "course_pages"
            
            # We create a virtual URL so the AI has a specific "URL + chunk id" to cite
            curated_data.append({
                "url": f"master_catalog.pdf#page={i+1}",
                "category": category,
                "note": f"Catalog Page {i+1}",
                "date_accessed": date_accessed,
                "content": text
            })

    # Save to the exact JSON format we need for the RAG agents
    with open('scraped_catalog_data.json', 'w') as f:
        json.dump(curated_data, f, indent=4)

    print("-" * 30)
    print("PDF Ingestion Complete!")
    print(f"Total Pages Processed: {pages_to_extract}")
    print(f"Total Words Extracted: {total_words}")
    
    if total_words >= 30000:
        print("✅ Word count requirement met (>30,000 words).")
    else:
        print("⚠️ Word count is below 30,000. Try extracting more pages.")

if __name__ == "__main__":
    # A publicly available, text-heavy catalog PDF (Example: Stanford Bulletin)
    CATALOG_URL = "https://web.stanford.edu/dept/registrar/bulletin_past/bulletin07-08/pdf/0708_Bulletin.pdf"
    ingest_pdf_to_json(CATALOG_URL)