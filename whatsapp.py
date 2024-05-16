import pyttsx3
import speech_recognition as sr
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import Chrome, ChromeOptions
import time
import pyautogui
from voice.AI_voice import main
import cohere
from voice.voice import tts
from command_R_plus import *
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from Listen.voice import SpeechRecognitionModel
from voice.AI_voice import main
# Initialize the Cohere client with your API key
co = cohere.Client(api_key="your API key")

def init_driver():
    # Path to ChromeDriver executable
    custom_data_dir = 'C:/Users/YourUsername/AppData/Local/Google/Chrome/User Data'
    profile_name = "0"  # This is typically "Default" unless you've created new profiles

    # Setup Chrome options
    options = ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument(f"--user-data-dir={custom_data_dir}")  # Path to your user data directory
    options.add_argument(f"--profile-directory={profile_name}")  # Profile name

    # Initialize the Chrome driver with the specified options
    driver = Chrome(options=options)
    
    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    
    wait = WebDriverWait(driver, 20)  # Adjust time accordingly
    return driver, wait

def find_unread_messages(driver, wait):
    try:
        # Find all elements with classes _ak7n and _ak8k (these represent unread messages)
        unread_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '._ak7n ._ak8k')))
        return unread_messages
    except Exception as e:
        print("Failed to find unread messages:", str(e))
        return []

def find_sender_names(driver, wait):
    try:
        # Find all elements with class ._ak7n ._ak8q
        sender_name_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '._ak7n ._ak8q')))
        sender_names = [element.text for element in sender_name_elements]
        return sender_names
    except Exception as e:
        print("Failed to find sender names:", str(e))
        return []

def get_permission():
    engine = pyttsx3.init()
    recognizer = sr.Recognizer()

    # Ask for permission using voice
    engine.say("Do you want to read the sender names?")
    engine.runAndWait()

    # Listen for user's response
    """with sr.Microphone() as source:
        print("Listening for permission...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)"""

    # Recognize user's response
    try:
        response = SpeechRecognitionModel()
        print("You said:", response)
        return response.lower() == "do it"  # Change this condition based on the voice input for "yes"
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return False
    except sr.RequestError:
        print("Sorry, I couldn't request results. Please check your internet connection.")
        return False

def reply_to_message(driver, recipient_name, message):
    try:
        # Use the recipient name to find and reply to the recipient
        chat_selector = f"span[title='{recipient_name}']"
        selected_recipient_element = driver.find_element(By.CSS_SELECTOR, chat_selector)
        selected_recipient_element.click()

        # Get AI response for the received message
        ai_response = message
        if ai_response:
            # Locate the textarea element
            textarea_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "._ak1l [role='textbox']"))
            )

            # Scroll the textarea element into view using JavaScript
            driver.execute_script("arguments[0].scrollIntoView(true);", textarea_element)

            # Click on the textarea to focus on it
            textarea_element.click()

            # Clear any existing text in the textarea
            textarea_element.clear()

            # Pass the AI response to the textarea
            textarea_element.send_keys(ai_response)

            # Press enter to send the message
            textarea_element.send_keys(Keys.RETURN)

            print("AI response pasted successfully:", ai_response)
            main("AI response pasted successfully:", ai_response)
        else:
            print("AI response is None. Skipping message.")

        # Allow some time for the chat to open and message to send
        time.sleep(2)
    except Exception as e:
        print(f"Failed to reply to message: {str(e)}")

def wpmain():
    driver, wait = init_driver()
    # Assume user is already logged in and does not need to scan QR code
    time.sleep(10)  # Give some time for WhatsApp Web to load completely

    # Find unread messages and sender names
    unread_messages = find_unread_messages(driver, wait)
    sender_names = find_sender_names(driver, wait)

    # Print unread message count and sender names
    print(f"Found {len(unread_messages)} unread messages.")
    print("Sender Names:")
    for i, sender in enumerate(sender_names, 1):
        print(f"{i}. {sender}")

    # Ask for permission using voice
    permission = get_permission()

    if permission:
        # Listen for the recipient's name via voice command
        engine = pyttsx3.init()
        recognizer = sr.Recognizer()

        engine.say("Please say the name of the recipient.")
        engine.runAndWait()

        # Listen for user's response
        with sr.Microphone() as source:
            print("Listening for recipient's name...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # Recognize recipient's name
        try:
            recipient_name = recognizer.recognize_google(audio).capitalize()
            print("Recognized recipient's name:", recipient_name)

            # Find the index of the selected recipient in the sender names list
            recipient_index = sender_names.index(recipient_name)

            # Display the message of the selected recipient index
            selected_message = unread_messages[recipient_index].text
            print("Message from", recipient_name, ":", selected_message)
            
            # Reply to the message using AI-generated response for the selected recipient
            message = ai(selected_message)  # Assuming ai function is defined elsewhere
            print("AI Response:", message)
            reply_to_message(driver, recipient_name, message)

        except sr.UnknownValueError:
            print("Sorry, I didn't catch the recipient's name.")
        except sr.RequestError:
            print("Sorry, I couldn't request results. Please check your internet connection.")

        # Properly close the driver after operations
        driver.quit()
    else:
        print("Permission not granted. Exiting.")

#if __name__ == "__main__":
    #wpmain()
