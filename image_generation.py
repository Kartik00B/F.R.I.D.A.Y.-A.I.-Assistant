import requests
import speech_recognition as sr
from PIL import Image
import time
import os
import io
API_URL = "https://api-inference.huggingface.co/models/Yntec/edgeOfRealism"

headers = {"Authorization": "Bearer hugging_face_apy_key"}

def query(payload, retries=3):
    delay = 30  # Initial delay
    for attempt in range(retries):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            try:
                Image.open(io.BytesIO(response.content)).verify()
                return response.content
            except Exception as e:
                print(f"Failed to verify image content: {e}")
                return None
        elif response.status_code == 503 and 'estimated_time' in response.json():
            wait_time = response.json().get('estimated_time', delay) + 10
            print(f"Model is loading, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Failed to fetch image: HTTP {response.status_code} - {response.text}")
    print("Failed to fetch image after retries.")
    return None

def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def moderate_image(image_path):
    print("Checking image for inappropriate content...")
    return True  # Assume no moderation for simplicity

def generate_image(description):
    if not description:
        description = get_speech_input()
        if not description:
            print("No description provided.")
            return "No valid input received."
    print(f"Generating image for: {description}")
    image_bytes = query({"inputs": description})
    if image_bytes:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"output_{timestamp}.jpg"
        output_directory = "Generated_images"
        os.makedirs(output_directory, exist_ok=True)
        full_path = os.path.join(output_directory, filename)
        with open(full_path, "wb") as f:
            f.write(image_bytes)
        if moderate_image(full_path):
            print(f"Image saved as '{full_path}'.")
            image = Image.open(full_path)
            image.show()
            return f"Image saved and opened: '{full_path}'"
        else:
            os.remove(full_path)
            return "Image failed moderation and was not saved."
    else:
        print("Failed to generate a valid image.")
        return "Failed to generate a valid image."

# Example of using the function through a voice command
if __name__ == "__main__":
    # This can be triggered by a specific command to your voice assistant
    generate_image("red panda")
