from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from datetime import datetime
import re

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


with open("uk_cities.txt", "r") as f:
    UK_CITIES = set(city.strip().lower() for city in f if city.strip())


def extract_budget(text):
    match = re.search(r"(\£?\d+[kKmM]?)\s*[-to ]*\s*(\£?\d+[kKmM]?)?", text)
    return match.group(0) if match else None

def extract_location(text):
    for w in text.lower().split():
        if w in UK_CITIES:
            return w.capitalize()
    return None

def extract_bedrooms(text):
    match = re.search(r"(\d+)\s*bed", text.lower())
    if match:
        return match.group(1)
    if "any" in text.lower():
        return "Any"
    return None


def extract_property_type(text):
    for ptype in ["house", "flat", "apartment"]:
        if ptype in text.lower():
            return ptype.capitalize()
    if "any" in text.lower():
        return "Any"
    return None


def log_usage(user_message, bot_response):
    log_entry = {
        "timestamp": str(datetime.now()),
        "user": user_message,
        "bot": bot_response
    }
    with open ( "/tmp/chat_log.json", 'a') as f:            
        f.write(json.dumps(log_entry) + "\n")

class RealEstateBot:
    def __init__(self, system_prompt = None):

        if not system_prompt:
            system_prompt = """
            You are an AI assistant for a real estate agency. 
            Your job is to greet visitors, collect their information, and answer questions about properties. 
            Always be friendly, professional, and concise.

            Your main goals are:
            1. Greet the user warmly and introduce yourself as a real estate assistant.
            2. Collect key lead information:
            - Budget range
            - Preferred location
            - Property type (house, flat, apartment, etc.)
            - Number of bedrooms
            3. Answer common real estate FAQs (office hours, viewing process, deposits, etc.).
            4. If the user asks about properties, give simple example listings (you can make up sample data if needed).
            5. At the end, encourage the user to provide their contact details (phone or email) so an agent can follow up.
            6. If you don't know something, politely say you will connect them with a human agent.
            7. Always keep responses short, clear, and helpful.
            After you have collected the user's budget, location, property type, and number of bedrooms:
            - Summarize their requirements back to them.
            - Provide 9 - 10 short example property listings (you can make up realistic sample data).
            - Encourage the user to provide their phone number or email so an agent can follow up.
            - Then continue answering FAQs or property-related questions as needed.
            """
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content" : system_prompt}]
        self.leads = []
    def update_leads(self, user_message):
        lead_entry = {"timestamp": str(datetime.now())}
        updated = False

        for extractor, key in [
            (extract_budget, "budget"),
            (extract_location, "location"),
            (extract_bedrooms, "bedrooms"),
            (extract_property_type, "property_type"),
        ]:
            val = extractor(user_message)
            if val:
                lead_entry[key] = val
                updated = True

        if updated:
            self.leads.append(lead_entry)  
            
    def chat(self, user_message):
        self.messages.append({"role": "user", "content" : user_message})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = self.messages,
            temperature = 0.7
        )

        bot_response = completion.choices[0].message.content

        self.messages.append({"role" : "assistant", "content" : bot_response})

        self.update_leads(user_message)

        log_usage(user_message, bot_response)

        return bot_response, self.leads 