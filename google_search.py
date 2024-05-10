import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from voice.voice import tts

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def search_on_google(query):
    tts(f"Searching Google for {query}")
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(5)  # Adjust the delay time as needed

        # Find the search result description
        search_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".kno-rdesc"))
        )
        description = search_result.text

        # Check if the description ends with "Wikipedia" and remove it
        if description.endswith("Wikipedia"):
            description = description.rsplit(' ', 1)[0]  # Remove the last word

        tts(description)
    except Exception as e:
        print("Error:", e)
        tts("Sorry, I encountered an error while searching on Google.")
    finally:
        time.sleep(5)  # Adjust the delay time as needed
        driver.quit()

if __name__ == "__main__":
    pass
