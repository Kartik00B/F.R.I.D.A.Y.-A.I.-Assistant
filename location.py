import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from voice.AI_voice import main
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def locate_location(location):
    main("User asked to locate " + location)

    # Start Chrome WebDriver
    driver = webdriver.Chrome()

    # Open Google Maps
    driver.get("https://www.google.com/maps")

    try:
        # Wait for the search box to be visible
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "searchboxinput"))
        )

        # Send the location to the search box
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)

        # Check if quick facts are available
        try:
            # Wait for the "See more" button to be clickable
            see_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jBCsPc') and contains(text(), 'More')]"))
            )

            # Click on the "See more" button
            see_more_button.click()

            # Wait for the text to load after clicking "See more"
            facts_text_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'wEvh0b'))
            )
            
            # Extract quick facts text
            facts_text = facts_text_element.text

            print(f"Quick Facts about {location}:", facts_text)
            main(f" Quick Facts about {facts_text}")

        except:
            # If quick facts are not available, try to fetch from the "About" section .ZqFyf
            about_section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".PYvSYb")))
            about_text = about_section.text.strip()

            print(f"About {location}:", about_text)
            main(f"About {about_text}")

    except Exception as e:
        print("Error:", e)
        main("Sorry, I encountered an error while locating the location.")
    finally:
        # Close the browser after a delay
        time.sleep(10)  # Adjust the delay time as needed
        driver.quit()

#if __name__ == "__main__":
    #locate_location("Great Wall Of China")




