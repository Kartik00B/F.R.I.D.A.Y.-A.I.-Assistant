import subprocess
import webbrowser
import sys
import time
import speech_recognition as sr
from win32com.client import Dispatch
import pywhatkit
import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
from insta import receive_command
from google_search import search_on_google
from location import locate_location
from news import run_assistant
import os
from app_index import get_voice_command
from voice.AI_voice import main
from Listen.voice import SpeechRecognitionModel
from command_R_plus import ai
from Vision import vision
from image_generation import generate_image
from weather import process_command


def speak(audio):
    speaking = Dispatch('SAPI.SpVoice')
    speaking.speak(audio)
    print(audio)

def classify_emotion(sentence):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(sentence)
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def takeCommand():
    #main("friday has been started")
    main("Hello, I am friday, Your Personal A.I. Assistant")
    """r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        
        r.energy_threshold=1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,0,56)"""

    while True:
        try:
            #print("Listening...")
            query = SpeechRecognitionModel()
                
            #query = r.recognize_google(audio, language="eng-in")
            print("Recognizing...")
            print("You Said", query)
            

            emotion = classify_emotion(query)
            print("Emotion:", emotion)

            if "friday" in query.lower() or "okay friday" in query.lower():
                print(f"User Said: {query}\n")
                

                sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.org"],
                        ["geeksforgeeks", "https://www.geeksforgeeks.org"]]

                for site in sites:
                    if f"open {site[0]}".lower() in query.lower():
                        main(f"Opening {site[0]} Kartik....")
                        webbrowser.open(site[1])

                if "open instagram" in query.lower():
                    # Pass the command to the Instagram handling code
                    receive_command(query)                
                
                elif "search" in query.lower():
                    search_query = query.lower().split("search", 1)[-1].strip()  # Extract the search query
                    print("Search query:", search_query)
                    # Debug print
                    search_on_google(search_query)# Call the search_on_google function

                elif "locate" in query.lower():
                    location = query.lower().split("locate", 1)[-1].strip()
                    main(f"Locating {location} on Google Maps.")
                    locate_location(location)

                elif "exit" in query.lower():  # Check for exit command
                    main("Exiting. Goodbye!")
                    sys.exit()

                elif "youtube" in query.lower():
                    pywhatkit.playonyt(query)

                elif "search" in query.lower():
                    pywhatkit.search(query)

                elif "use ai" in query.lower():
                   user_input = query.lower().split("use ai", 1)[-1].strip()
                   ai(user_input) 
                    
                elif "news" in query.lower():
                    run_assistant()
                
                elif "open launcher" in query.lower():
                    main("Opening App Launcher")
                    get_voice_command()
                
                elif "open your eyes" in query.lower():
                    main("opening my eyes wait a second...")
                    vision()
                    
                elif "generate image of" in query.lower():
                    user_input = query.lower().split("generate image of", 1)[-1].strip()
                    generate_image(user_input)
                    
                elif 'weather' in query.lower():
                    process_command('weather')
                elif 'location' in query.lower():
                    process_command('location')
                    
                """elif "check instagram" in query.lower():
                    # Extract the names of people who sent the messages
                    choose_action()
                    print("done")"""
                """elif "check whatsapp" in query.lower():
                    # Extract the names of people who sent the messages
                    main("sure kartik give me a second...")
                    wpmain()"""
                
            else:
                print("You Missing Something 😁")
                
                main("Aren't you missing something")

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            print("Request Error:", e)
            main("Sorry, I couldn't request results. Check your internet connection.")
        except Exception as e:
            print("Error:", e)
            main("Sorry, I encountered an error. Please try again.")
takeCommand()
"""if __name__ == '__main__':
    main("Hello, I am Your Personal A.I. Assistant")
    while True:
        print("Recognizing.....")
        takeCommand()"""
