from datetime import datetime
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        rec.pause_threshold = 1
        audio = rec.listen(source)
    try:
        print("Recognizing...")
        query = rec.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

        return query.lower()
    except Exception as e:
        print("Cant understand")
        return "none"

#always use to convert input lower case
greet_msgs=["hi","hello","hey","hi there","hello there"]
date_msgs=["what's the date","what is the date","current date","date"]
time_msgs=["what's the time","what time is it","current time","time"]
open_msgs=["youtube","facebook","google","linkedin"]
news_msgs=["tell me news","simple news","today news"]
loc_msgs=["where is","where's","location","tell my currrent location"]
weather_msgs=["weather","tell me weather","what's the weather"]
def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=695e07af402f4b119f0703e9b19f4683%22"
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    for i in range(len(articles)):
        print(articles[i]['title'])
def get_location():
    ip_address = requests.get("https://api.ipify.org").text
    data = requests.get(f"http://ip-api.com/json/{ip_address}").json()
    return {
        "city": data.get("city"),
        "region": data.get("regionName"),
        "country": data.get("country"),
        "lat": data.get("lat"),
        "lon": data.get("lon")
    }


# def get_weather():
#     city = get_location()
#     # url = "https://api.openweathermap.org/data/2.5/weather/timemachine?lat=39.099724&lon=-94.578331&dt=1643803200&appid=a3759b142167ce77c3ce32825dae8efe"
#     url=f"https://api.weatherapi.com/v1/current.json?key=4aa3d8aed6774cc3945160505263001&q={city}&aqi=yes"
#     response = requests.get(url)
#     data = response.json()
#     print(
#         "City ->", data["location"]["name"],
#         "\nCountry ->", data["location"]["country"],
#         "\nTemperature (°C) ->", data["current"]["temp_c"],
#         "\nHumidity ->", data["current"]["humidity"],
#         "\nCondition ->", data["current"]["condition"]["text"]
#     )

def get_weather():
    loc = get_location()
    url = (
        "https://api.weatherapi.com/v1/current.json"
        f"?key=4aa3d8aed6774cc3945160505263001&q={loc['lat']},{loc['lon']}&aqi=yes"
    )
    data = requests.get(url).json()

    print(
        "Location ->", loc["city"], ",", loc["region"],
        "\nTemperature (°C) ->", data["current"]["temp_c"],
        "\nHumidity ->", data["current"]["humidity"],
        "\nCondition ->", data["current"]["condition"]["text"]
    )



chat=True
while(chat):
    # user_msg = input("Enter your message:").lower()
    user_msg = listen()
    if(user_msg in greet_msgs):
        speak("Hello, How can I help you?")
    elif user_msg=="bye":
        print("Bye, Have a nice day!")
        chat=False
    elif user_msg in date_msgs:
        print(datetime.now().strftime("%d-%m-%Y"))
    elif user_msg in time_msgs:
        print(datetime.now().strftime("%I:%M:%S %P"))
    elif user_msg.startswith("open"):
        site = user_msg[5:]
        if site in open_msgs:
            webbrowser.open(f"https://www.{site}.com")
    elif user_msg.startswith("calculate"):
        expression = user_msg.split()[-1]
        result = eval(expression)
        print(result)
    elif user_msg in news_msgs:
        get_news()
    elif user_msg in loc_msgs:
        loc = get_location()
        print(
            "City ->", loc["city"],
            "\nRegion ->", loc["region"],
            "\nCountry ->", loc["country"]
        )

    elif user_msg in weather_msgs:
        get_weather()
    else:
        print("I don't understand you")



# TO RUN IN THIS SYSTEM (LINUX)
# YOU HAVE TO USE THIS COMMAND IN TERMINAL
# python appversion2.py 2>/dev/null