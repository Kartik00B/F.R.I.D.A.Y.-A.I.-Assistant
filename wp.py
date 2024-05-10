import pyttsx3
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import Chrome, ChromeOptions
import time
import importlib.util
from voice.AI_voice import main
from Listen.voice import SpeechRecognitionModel

# Load intent data from intent_data.py
spec = importlib.util.spec_from_file_location("intent_data", "intent_data.py")
intent_data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intent_data_module)
intent_data = intent_data_module.intent_data

#def init_driver():
    # Path to ChromeDriver executable
custom_data_dir = r"C:\Users\karti\AppData\Local\Google\Chrome\User Data"
profile_name = "0"  # This is typically "Default" unless you've created new profiles

    # Setup Chrome options
options = ChromeOptions()
#options.add_argument("--headless")
options.add_argument(f"--user-data-dir={custom_data_dir}")  # Path to your user data directory
options.add_argument(f"--profile-directory={profile_name}")  # Profile name
options.add_argument(f"--chrome-version=124.0.6367.119") 
  # Specify the Chrome version here

driver = Chrome(options=options)
    
wait = WebDriverWait(driver, 10)  # Adjust time accordingly
#driver, wait

def find_unread_messages(driver, wait):
    try:
        # Find all elements with classes _1Gy50 and _2EXPL (these represent unread messages)
        unread_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '._ak7n ._ak8k')))
        return unread_messages
    except Exception as e:
        print("Failed to find unread messages:", str(e))
        return []

def find_sender_names(driver, wait):
    try:
        # Find all elements with class _1Gy50
        sender_name_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '._ak7n ._ak8q')))
        sender_names = [element.text for element in sender_name_elements]
        return sender_names
    except Exception as e:
        print("Failed to find sender names:", str(e))
        return []

def get_permission():
    engine = pyttsx3.init()
    recognizer = sr.Recognizer()
    main("should i read the sender names?")
    # Ask for permission using voice
    #engine.say("Do you want to read the sender names?")
    #engine.runAndWait()

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
    
def ai_response(message):
    # Loop through each intent in the intent data
    for intent, data in intent_data.items():
        # Loop through each example query-response pair for the current intent
        for pair in data:
            query = pair["query"]
            response = pair["response"]
            # If the received message matches any example query, return the corresponding response
            if query in message.lower():
                return response
    # If no match is found, return a default response or None
    return None

def reply_to_message(driver, recipient_name, message):
    try:
        # Use the recipient name to find and reply to the recipient
        chat_selector = f"span[title='{recipient_name}']"
        selected_recipient_element = driver.find_element(By.CSS_SELECTOR, chat_selector)
        selected_recipient_element.click()

        # Get AI response for the received message
        ai_response_text = ai_response(message)
        if ai_response_text:
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
            textarea_element.send_keys(ai_response_text)

            # Press enter to send the message
            textarea_element.send_keys(Keys.RETURN)

            print("AI response pasted successfully:", ai_response_text)
        else:
            print("No suitable AI response found for the message. Skipping.")

        # Allow some time for the chat to open and message to send
        time.sleep(2)
    except Exception as e:
        print(f"Failed to reply to message: {str(e)}")

def wpmain():
    driver.get("https://web.whatsapp.com/")
    #driver, wait = init_driver()
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
            main("Please say the name of the recipient.")
            #engine.say("Please say the name of the recipient.")
            #engine.runAndWait()

            # Listen for user's response
            #with sr.Microphone() as source:
            print("Listening for recipient's name...")
                #recognizer.adjust_for_ambient_noise(source)
                #audio = recognizer.listen(source)

            # Recognize recipient's name
            try:
                recipient_name = SpeechRecognitionModel().capitalize()
                print("Recognized recipient's name:", recipient_name)

                # Find the index of the selected recipient in the sender names list
                recipient_index = sender_names.index(recipient_name)

                # Display the message of the selected recipient index
                selected_message = unread_messages[recipient_index].text
                print("Message from", recipient_name, ":", selected_message)
      
        # Reply to the message using AI-generated response for the sender
                reply_to_message(driver, recipient_name, selected_message)
            
            except sr.UnknownValueError:
                print("Sorry, I didn't catch the recipient's name.")
            except sr.RequestError:
                print("Sorry, I couldn't request results. Please check your internet connection.")
    # Properly close the driver after operations
    driver.quit()

if __name__ == "__main__":
    wpmain()
