from google import genai
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def score_and_enrich_leads(leads):
    leads_text = json.dumps(leads, indent=2)
    prompt = "You are a sales analyst. Analyze these business leads and return ONLY a JSON array with no extra text. For each lead add these fields: score (number 1-10), status (Hot or Warm or Cold), reason (one line), outreach_message (Hinglish). Give higher score if rating is 4 plus, no website, phone available. Here are the leads: " + leads_text
    
    for attempt in range(3):
        try:
            print("Gemini AI analyzing... attempt " + str(attempt+1))
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt
            )
            response_text = response.text
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            enriched_leads = json.loads(response_text[start:end])
            print(str(len(enriched_leads)) + " leads scored!")
            return enriched_leads
        except Exception as e:
            print("Error: " + str(e)[:100])
            print("Waiting 60 seconds before retry...")
            time.sleep(60)
    
    print("Adding basic scores manually...")
    for lead in leads:
        lead['score'] = 5
        lead['status'] = 'Warm'
        lead['reason'] = 'Manual score - API limit reached'
        lead['outreach_message'] = 'Namaste! Aapki business ke liye kuch interesting options hain.'
    return leads

def batch_process(leads, batch_size=10):
    all_processed = []
    for i in range(0, len(leads), batch_size):
        batch = leads[i:i + batch_size]
        processed = score_and_enrich_leads(batch)
        all_processed.extend(processed)
        if i + batch_size < len(leads):
            print("Waiting 30 seconds between batches...")
            time.sleep(30)
    return all_processed

if __name__ == "__main__":
    from scraper import scrape_google_maps
    leads = scrape_google_maps("coaching institute in Lucknow", 5)
    enriched = batch_process(leads)
    for lead in enriched:
        print(str(lead.get('name')) + " - Score: " + str(lead.get('score')))