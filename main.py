import speech_recognition as sr
import webbrowser
import pyttsx3
import pocketsphinx
import time
import pyjokes
import requests
import wikipedia
from googlesearch import search
from bs4 import BeautifulSoup

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def play_song(song_name):
    url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
    webbrowser.open(url)

def openSite(site):
    s = site.lower()
    webbrowser.open(f"https://{s}.com")

newsApi = "ba54cd18c1194d5fb3a6b8eb0fdaba58"

def get_news():
    """Fetches top news headlines from NewsAPI"""
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApi}"
    
    try:
        response = requests.get(url)  # Send API request
        response.raise_for_status()  # Raise error for bad requests (4xx, 5xx)
        data = response.json()  # Convert response to JSON
        print(data)  # Print full response for debugging
        
        if data.get("status") == "ok":
            articles = data.get("articles", [])[:5]  # Get top 5 news
            if not articles:
                speak("No news availble")
                return "No news available."
            news_list = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]
            return "\n".join(news_list)
        else:
            return f"Error fetching news: {data.get('message', 'Unknown error')}"
    
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"


def get_wikipedia_summary(query):
    """Fetches a short summary from Wikipedia"""
    try:
        summary = wikipedia.summary(query, sentences=2)  # Get first 2 sentences
        return f"According to Wikipedia, {summary}"
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple results. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on Wikipedia."


def google_search(query):
    """Fetches the first result from Google and extracts some text"""
    try:
        results = list(search(query, num_results=1))  # Get the top search result
        if not results:
            return "Sorry, no results found."

        url = results[0]  # First search result URL
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract first paragraph text from the webpage
        paragraphs = soup.find_all("p")
        if paragraphs:
            info = paragraphs[0].get_text()
            return f"According to Google, {info}"
        else:
            return f"Here is what I found: {url}"

    except Exception:
        return "Sorry, I couldn't search Google."


def processCommand(c):
    if c.lower().startswith("open"):
        site = c.lower().split(" ")[1]
        openSite(site)
    
    elif c.lower().startswith("play"):
        song_name = " ".join(c.lower().split(" ")[1:]) 
        play_song(song_name)

    elif "joke" in c.lower():
        joke = pyjokes.get_joke()
        speak(joke)

    elif "news" in c.lower():
        news = get_news()
        speak(news)

    elif "search wikipedia for" in c.lower():
        topic = c.lower().replace("search wikipedia for", "").strip()
        if topic:
            summary = get_wikipedia_summary(topic)
            speak(summary)
        else:
            speak("What should I search for?")
    
    else:
        #Search on google
        result = google_search(c)
        speak(result)
        



if __name__ == "__main__":
    speak("I am onn")
    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            # print("did you mean:",command)
            #Listen for the wake word "Chhotu"
            if(word.lower() == "deactivate"):
                speak("Ok sir, i am going to sleep now, bye!")
                break
            elif(word.lower() in ["chhotu", "chotu", "chhotu babu"]):
                speak("Yes sir, ")
                last_command_time = time.time() 
                while(True):
                    #listen for the main command now
                    try:
                        with sr.Microphone() as source:
                            print("Listening for command...")
                            audio = r.listen(source, timeout=2, phrase_time_limit=3)
                        command = r.recognize_google(audio)
                        if(command.lower() == "bye"):
                            speak("Bye - bye!")
                            break
                        processCommand(command)
                        last_command_time = time.time() 
                    except Exception as e:
                        print("Sorry, i didn't understand...")
                        continue

                    # Check if 2 minutes have passed since the last command
                    if time.time() - last_command_time > 60:
                        speak("ahhhhh")
                        break  # Exit command loop and wait for "Chhotu" again




        except Exception as e:
            print("Sorry, i didn't understand...")
            
