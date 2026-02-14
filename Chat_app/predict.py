import joblib
from datetime import datetime
import requests
from preprocessing import preprocess_text

import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY not found in .env file")


# Load model once
vectorizer = joblib.load("my_tfidf.pkl")
logistic = joblib.load("my_intent_clf_model.pkl")


def get_news():
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=india&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    )

    data = requests.get(url).json()

    if data.get("status") != "ok":
        return f"News API Error: {data}"

    articles = data.get("articles", [])

    if not articles:
        return "No news found."

    return "\n".join([a["title"] for a in articles[:5]])
def get_location():
    ip_address = requests.get("https://api.ipify.org").text
    data = requests.get(f"http://ip-api.com/json/{ip_address}").json()
    return f"{data.get('city')}, {data.get('regionName')}, {data.get('country')}"


def get_weather():
    try:
        loc_data = requests.get("https://api.ipify.org").text
        loc = requests.get(f"http://ip-api.com/json/{loc_data}").json()

        API_KEY = "PASTE_YOUR_REAL_KEY_HERE"

        url = (
            "https://api.weatherapi.com/v1/current.json"
            f"?key={WEATHER_API_KEY}&q={loc['lat']},{loc['lon']}&aqi=no"
        )

        data = requests.get(url).json()

        if "current" not in data:
            return f"Weather API Error: {data.get('error', {}).get('message', 'Unknown error')}"

        return (
            f"Location: {loc['city']}\n"
            f"Temperature: {data['current']['temp_c']}°C\n"
            f"Condition: {data['current']['condition']['text']}"
        )

    except Exception:
        return "Weather service is currently unavailable."

def predict_intent(user_input):
    processed = preprocess_text([user_input])
    user_vector = vectorizer.transform(processed)
    prediction = logistic.predict(user_vector)[0]
    return prediction


def get_response(user_input):
    intent = predict_intent(user_input)

    if intent == "greet":
        return "Hello, How can I help you?"

    elif intent == "date":
        return datetime.now().strftime("%d-%m-%Y")

    elif intent == "time":
        return datetime.now().strftime("%I:%M:%S %p")

    elif intent == "location":
        return get_location()

    elif intent == "news":
        return get_news()

    elif intent == "weather":
        return get_weather()
    elif intent == "open":
        site = user_input.lower().replace("open", "").strip()

        if site:
            return f"[Click here to open {site}](https://www.{site}.com)"
        else:
            return "Please specify a website to open."
    else:
        return "I don't understand you."