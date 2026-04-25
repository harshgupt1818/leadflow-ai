# scraper.py
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")

def scrape_google_maps(query: str, max_results: int = 50):
    leads = []
    
    print(f"🔍 Searching for: {query}")
    
    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": SERP_API_KEY
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    
    results = data.get("local_results", [])
    print(f"✅ Found {len(results)} businesses!")
    
    for i, place in enumerate(results[:max_results]):
        lead = {
            "name": place.get("title", "N/A"),
            "phone": place.get("phone", "N/A"),
            "website": place.get("website", "N/A"),
            "address": place.get("address", "N/A"),
            "rating": place.get("rating", "N/A"),
            "reviews": place.get("reviews", "N/A"),
            "query": query
        }
        leads.append(lead)
        print(f"  ✔️ {i+1}. {lead['name']}")
    
    return leads


if __name__ == "__main__":
    results = scrape_google_maps("coaching institute in Lucknow", 20)
    df = pd.DataFrame(results)
    print(df)
    df.to_excel("test_leads.xlsx", index=False)
    print("✅ Saved to test_leads.xlsx!")