import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import webbrowser
from voice.voice import tts
from Listen.voice import SpeechRecognitionModel
from voice.AI_voice import main
# Initialize the speech recognition and text-to-speech engines
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
        try:
            main("Listening for your choice of news category...")
            print("Listening for your choice of news category...")
            text = SpeechRecognitionModel()
            print("You said: " + text)
            return text
    #Listen for a voice command and convert it to text.
            """with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)"""
        except sr.UnknownValueError:
            main("Sorry, I did not catch that. Please repeat.")
            return None

def fetch_and_read_news(category):
    """Fetch and read news based on the user's choice of category."""
    categories = {
        "climate": "https://www.bbc.com/news/science_and_environment",
        "video": "https://www.bbc.com/news/video_and_audio",
        "world": "https://www.bbc.com/news/world",
        "ai": "https://www.bbc.com/innovation/artificial-intelligence",
        "uk": "https://www.bbc.com/news/uk",
        "business": "https://www.bbc.com/news/business",
        "technology": "https://www.bbc.com/innovation/technology",
        "wheather" : "https://www.bbc.com/weather",
        "sports": "https://www.bbc.com/sport",
    }

    if category.lower() in categories:
        url = categories[category.lower()]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if category.lower() == "technology":
            promo_contents = soup.select('.gxEarx')  # Updated selector for technology news
            #print(promo_contents)
        elif category.lower() == "business":
            promo_contents = soup.select('.gxEarx')
            #print(promo_contents).strip()
        elif category.lower() == "ai":
            promo_contents = soup.select('.gxEarx')    
        
        else:
            promo_contents = soup.select('.ssrcss-tq7xfh-PromoContent')
        
        if promo_contents:
            main(f"Here are the top news items from {category}.")
            for content in promo_contents[:5]:  # Read up to 5 news items
                headline = content.find('h3')
                if headline:
                    print(headline.text.strip())
                    main(headline.text.strip())
                else:
                    print(content.text.strip())
                    main(content.text.strip())
            # After reading news, offer to open the web browser
            main("Would you like to open the news portal to read more?")
            response = listen()
            if response and "do it" in response.lower():
                webbrowser.open(url)
                return
        else:
            main(f"Sorry, there are no news items available right now for {category}.")
    else:
        main("Sorry, I don't have news for that category.")


def run_assistant():
    main("Which type of news would you like to hear? You can choose from climate, video, world, AI, UK, business, or technology.")
    category = listen()
    if category:
        fetch_and_read_news(category)

#if __name__ == "__main__":
    #run_assistant()
