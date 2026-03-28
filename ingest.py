import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_text_from_url(url):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""

def main():
    with open('sources.json', 'r') as f:
        sources = json.load(f)

    curated_data = []
    total_words = 0
    date_accessed = datetime.now().strftime("%Y-%m-%d")

    # Iterate through policies, programs, and courses
    for category, items in sources.items():
        for item in items:
            text = scrape_text_from_url(item['url'])
            word_count = len(text.split())
            total_words += word_count
            
            curated_data.append({
                "url": item['url'],
                "category": category,
                "note": item['note'],
                "date_accessed": date_accessed,
                "content": text
            })

    # Save the scraped data
    with open('scraped_catalog_data.json', 'w') as f:
        json.dump(curated_data, f, indent=4)

    print("-" * 30)
    print("Ingestion Complete!")
    print(f"Total Words Extracted: {total_words}")
    if total_words >= 30000:
        print("✅ Word count requirement met (>30,000 words).")
    else:
        print("⚠️ Word count is below 30,000. You may need to add more URLs to sources.json.")

if __name__ == "__main__":
    main()