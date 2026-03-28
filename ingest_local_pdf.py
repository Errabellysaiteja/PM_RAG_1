import json
import PyPDF2
from datetime import datetime

def ingest_local_pdf_to_json(pdf_path, output_json="scraped_catalog_data.json"):
    print(f"Loading local PDF: {pdf_path}...")
    
    curated_data = []
    total_words = 0
    date_accessed = datetime.now().strftime("%Y-%m-%d")
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            print(f"Found {total_pages} pages. Extracting text...")
            
            for i in range(total_pages):
                text = reader.pages[i].extract_text()
                if text:
                    word_count = len(text.split())
                    total_words += word_count
                    
                    # We create a virtual URL so the AI has a specific citation to use
                    curated_data.append({
                        "url": f"{pdf_path}#page={i+1}",
                        "category": "academic_catalog", 
                        "note": f"Catalog Page {i+1}",
                        "date_accessed": date_accessed,
                        "content": text
                    })

        # Save to the exact JSON format our vector store builder expects
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(curated_data, f, indent=4)

        print("-" * 30)
        print("PDF Ingestion Complete!")
        print(f"Total Pages Processed: {total_pages}")
        print(f"Total Words Extracted: {total_words}")
        
        if total_words >= 30000:
            print("✅ Word count requirement met (>30,000 words).")
        else:
            print("⚠️ Word count is below 30,000. You may need a larger catalog.")

    except FileNotFoundError:
        print(f"Error: Could not find '{pdf_path}'. Make sure the file is in the same folder as this script.")

if __name__ == "__main__":
    # --- CHANGE THIS TO YOUR PDF'S EXACT FILE NAME ---
    LOCAL_PDF_FILENAME = "nw_course.pdf" 
    ingest_local_pdf_to_json(LOCAL_PDF_FILENAME)