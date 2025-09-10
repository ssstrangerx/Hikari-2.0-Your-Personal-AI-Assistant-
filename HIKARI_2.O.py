"""Created by Pranav Tripathi, not anyone else"""

import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import pyautogui
import keyboard
import datetime
import python_weather
import asyncio
import random
import requests
from bs4 import BeautifulSoup

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 1
        
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"You: {query}")
            return query.lower()
        
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            say("Sorry Boss, there's a problem with the recognition service.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def open_application(app_name):
    say(f"Opening {app_name}, Boss.")
    os.system(f"start {app_name}")

def close_application(app_name):
    say(f"Closing {app_name}, Boss.")
    os.system(f"taskkill /f /im {app_name}.exe")

def open_website(url):
    say(f"Opening {url}, Boss.")
    webbrowser.open(url)

def google_search(query):
    say(f"Searching for {query} on Google, Boss.")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def download_file(query):
    say(f"Searching for {query} download, Boss.")
    webbrowser.open(f"https://www.google.com/search?q={query}+download")

def open_new_tab():
    say("Opening a new tab, Boss.")
    keyboard.press_and_release('ctrl+t')

def close_tab():
    say("Closing the current tab, Boss.")
    keyboard.press_and_release('ctrl+w')

def type_text(text):
    say(f"Typing: {text}")
    pyautogui.write(text, interval=0.05)

def shutdown_pc():
    say("Shutting down the system, Boss.")
    os.system("shutdown /s /t 1")

def restart_pc():
    say("Restarting the system, Boss.")
    os.system("shutdown /r /t 1")

def sleep_pc():
    say("Putting the system to sleep, Boss.")
    os.system("powercfg -hibernate off & rundll32.exe powrprof.dll,SetSuspendState Sleep")

def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    say(f"Boss, the time is {current_time}.")

def get_date():
    today_date = datetime.datetime.now().strftime("%A, %d %B %Y")
    say(f"Boss, today's date is {today_date}.")

def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    joke = random.choice(jokes)
    say(joke)

def get_weather():
    try:
        import requests
        from bs4 import BeautifulSoup
        from datetime import datetime

        city = "delhi"
        url = f"https://www.accuweather.com/en/in/{city}/202396/weather-forecast/202396"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Request & parse
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract temp & condition
        temperature_tag = soup.find("div", class_="temp")
        condition_tag = soup.find("span", class_="phrase")

        # Detect season
        month = datetime.now().month
        if month in [3, 4, 5]:
            season = "summer"
        elif month in [6, 7, 8, 9]:
            season = "monsoon"
        elif month in [10, 11]:
            season = "autumn"
        else:
            season = "winter"

        if temperature_tag and condition_tag:
            temperature = temperature_tag.text.strip()
            condition = condition_tag.text.strip()

            say(f"Boss, it's currently {temperature} in {city.capitalize()} with {condition.lower()}. "
                f"It feels like {season} season today.")
        else:
            say("Sorry Boss, I couldn't get the weather data from AccuWeather.")
            print("Missing weather tags.")
    except Exception as e:
        say("Sorry Boss, there was an error while fetching AccuWeather.")
        print("AccuWeather Scrape Error:", e)


def get_news():
    url = "https://news.google.com/news/rss"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    headlines = soup.find_all("title")

    say("Boss, here are the top three news headlines.")
    for i in range(1, 4):
        say(headlines[i].text)
        

def stop_assistant():
    say("Okay, bye Boss!")
    exit()

if __name__ == "__main__":
    say("Hello Boss, I am Hikari.")
    
    while True:
        command = take_command()
        
        if command:
            if "stop" in command or "exit" in command:
                stop_assistant()
            
            elif "shutdown" in command:
                shutdown_pc()

            elif "restart" in command:
                restart_pc()

            elif "sleep" in command:
                sleep_pc()

            elif "open google" in command:
                open_website("https://www.google.com")
            
            elif "search" in command:
                query = command.replace("search", "").strip()
                google_search(query)
            
            elif "download" in command:
                query = command.replace("download", "").strip()
                download_file(query)

            elif "open tab" in command:
                open_new_tab()
            
            elif "close tab" in command:
                close_tab()
            
            elif "type" in command:
                text = command.replace("type", "").strip()
                type_text(text)

            elif "open" in command:
                app_name = command.replace("open", "").strip()
                open_application(app_name)

            elif "close" in command:
                app_name = command.replace("close", "").strip()
                close_application(app_name)

            elif "time" in command:
                get_time()

            elif "date" in command:
                get_date()

            elif "joke" in command:
                tell_joke()

            elif "weather" in command:
                get_weather()

            elif "news" in command:
                get_news()

            else:
                say("Boss, I didn't understand that. Can you repeat?")