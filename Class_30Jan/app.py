from datetime import datetime
import webbrowser
import requests
#always use to convert input lower case
greet_msgs=["hi","hello","hey","hi there","hello there"]
date_msgs=["what's the date","what is the date","current date","date"]
time_msgs=["what's the time","what time is it","current time","time"]
open_msgs=["youtube","facebook","google","linkedin"]
news_msgs=["tell me news","simple news","today news"]
def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=695e07af402f4b119f0703e9b19f4683"
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    for i in range(len(articles)):
        print(articles[i]['title'])

chat=True
while(chat):
    user_msg = input("Enter your message:").lower()
    if(user_msg in greet_msgs):
        print("Hello, How can I help you?")
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
    else:
        print("I don't understand you")

