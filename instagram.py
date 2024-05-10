from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from undetected_chromedriver import Chrome, ChromeOptions
import time
import speech_recognition as sr
from Listen.voice import SpeechRecognitionModel
from voice.AI_voice import main as voice_main
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Path to ChromeDriver executable and setup Chrome options
custom_data_dir = 'C:/Users/karti/AppData/Local/Google/Chrome/User Data'
profile_name = "0"  # This is typically "Default" unless you've created new profiles

options = ChromeOptions()
options.add_argument("--headless")
options.add_argument(f"--user-data-dir={custom_data_dir}")  # Path to your user data directory
options.add_argument(f"--profile-directory={profile_name}")
# Initialize WebDriver
driver = Chrome(options=options)

# Define WebDriverWait
wait = WebDriverWait(driver, 10)

def get_voice_input():
    """Get voice input from the user."""
    recognizer = sr.Recognizer()
    try:
        text = SpeechRecognitionModel()
        print("You said:", text)
        return text
    except Exception as e:
        print("An error occurred:", e)
        return None

def handle_new_messages():
    """Handle Instagram new messages."""
    try:
        # Open Instagram and log in
        driver.get('https://www.instagram.com/')
        time.sleep(5)  # Wait for the page to load

        # Wait for redirection to the homepage
        message_count_element = driver.find_element(By.CSS_SELECTOR, '.xyqdw3p')
        message_count = message_count_element.text

        voice_main(f"Sir, you have {message_count} new messages in your Instagram.")

        # Ask if the user wants to know the names of people who sent the messages
        voice_main("Would you like to know the names of people who sent the messages?")

        # Use speech recognition to listen for user response
        response = get_voice_input()

        if "tell me the names" in response.lower():
            # Find the link element for direct messages
            link_element = driver.find_element(By.CSS_SELECTOR, 'a[href="/direct/inbox/"]')
            # Click on the link
            link_element.click()
            time.sleep(5)
        
            new_notifications_names = driver.find_elements(By.CSS_SELECTOR, ".x1s688f")
            new_messages_spans = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.x1xlr1w8")))
            
            if len(new_notifications_names) == len(new_messages_spans):
                for i in range(len(new_notifications_names)):
                    name = new_notifications_names[i].text
                    message = new_messages_spans[i].text
                    print(f"{name}: {message}")
                    voice_main(f"{name}: {message}")
                    time.sleep(2)
            else:
                print("The number of names does not match the number of messages. Please check the selectors.")
        else:
            print("Invalid choice. Please say 'tell me the names'.")

    except TimeoutException:
        print("Timeout occurred while waiting for the element.")
    #finally:
        # Close the WebDriver
        #driver.quit()

def handle_follow_requests():
    """Handle Instagram follow requests."""
    try:
        # Open Instagram and log in
        #driver.get('https://www.instagram.com/')
        #time.sleep(5)  # Wait for the page to load

        # Check for follow requests
        driver.get("https://www.instagram.com/notifications/?followRequests=true")
        time.sleep(5)
        req = driver.find_elements(By.CSS_SELECTOR, "._ab5c")

        if not req:
            print("Follow request is present.")
            #voice_main("Follow request is present.")

            # If follow requests are present, extract names
            name_elements = driver.find_elements(By.CSS_SELECTOR, ".x1xmf6yo")
            names = [name.text for name in name_elements]

            # Print names and ask for action
            print("Names of people who sent follow requests:")
            for name in names:
                print(name)
                voice_main(f"{name} has sent a follow request.")

            # Ask the user to accept or delete follow requests
            voice_main("Do you want to accept the follow request?")

            # Get user response
            choice = get_voice_input()

            # Click the accept or delete button based on user's choice
            if choice.lower() == "do it":
                accept_buttons = driver.find_elements(By.CSS_SELECTOR, ".x1emribx")
                for button in accept_buttons:
                    button.click()
                    print(f"Follow Request from {name} is accepted")
                    voice_main(f"Follow Request from {name} is accepted")
            elif choice.lower() == "delete":
                delete_buttons = driver.find_elements(By.CSS_SELECTOR, ".x1gjpkn9")
                for button in delete_buttons:
                    button.click()
                    print(f"Follow Request deleted from {name}")
                    voice_main(f"Follow Request deleted from {name}")
            else:
                print("Invalid choice. Please say 'do it' or 'delete'.")
        else:
            print("No follow requests.")
            voice_main("No follow requests.")

    except TimeoutException:
        print("Timeout occurred while waiting for the element.")
    finally:
        # Close the WebDriver
        driver.quit()

def choose_action():
    """Prompt the user to choose which action to perform."""
    while True:
        voice_main("What would you like to check? New messages or follow requests?")
        response = get_voice_input()
        if "new messages" in response.lower():
            handle_new_messages()
        elif "follow request" in response.lower():
            handle_follow_requests()
        else:
            print("Invalid choice. Please say 'new messages' or 'follow requests'.")
            continue

        voice_main("Do you want to check anything else?")
        response = get_voice_input()
        if "no" in response.lower():
            break

if __name__ == "__main__":
    choose_action()
