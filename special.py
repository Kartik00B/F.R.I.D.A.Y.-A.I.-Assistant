import speech_recognition as sr
from openai import OpenAI
from elevenlabslib import *
import sys
from voice.AI_voice import main
from Listen.voice import SpeechRecognitionModel
def start_assistant():
    # Initialize OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Initialize ElevenLabs API key
    #elevenLabsAPIKey = 'elevenLabsAPIKey'

    # Initialize SpeechRecognition recognizer and microphone
    #r = sr.Recognizer()
    #mic = sr.Microphone()

    # Initialize ElevenLabs user
    #user = ElevenLabsUser(elevenLabsAPIKey)

    # Select voice for speech output
    #voice = user.get_voices_by_name("Glinda")[0]

    # Initialize conversation history
    conversation = [{"role": "system", "content": "my name is friday and my purpose is to be your AI assistant"}]

    while True:
        """with mic as source:
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("tell me how can i help you kartik")
            tts("tell me how can i help you kartik")
            audio = r.listen(source)

        # Recognize speech input
        try:
            word = r.recognize_google(audio)"""
              
        try:
            print("Listening...")
            word = SpeechRecognitionModel()
            print("You said:", word)
        except sr.UnknownValueError:
            main("Could not understand audio")
            continue  # Restart the loop if audio is not understood

        if "draw" in word:
            i = word.find("draw")
            i += 2
            response = client.images.generate(
                prompt=word[i:],
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            print(word[i:])
            print(image_url)
            continue  # Skip the rest of the loop to prevent processing as chat input

        elif "chat" in word:
            i = word.find("chat")
            i += 2
            # Append user input to conversation history
            conversation.append({"role": "user", "content": word[i:]})

            # Generate completion based on conversation history
            prompt = '\n'.join([utterance["content"] for utterance in conversation])  # Using the entire conversation history as the prompt
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=1,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Retrieve the response from the model
            message = response.choices[0].text
            conversation.append({"role": "assistant", "content": message})

            # Print the response
            print(message)
            main(message)

            # Generate speech audio and play it using ElevenLabs voice
            #voice.generate_play_audio_v2(message)
            
        elif ("goodbye" in word) or ("get lost" in word):
            main("Thanks for using me boss, have a good day")
            sys.exit(0)
        
        else:
            # Append user input to conversation history
            conversation.append({"role": "user", "content": word})

            # Generate completion based on conversation history
            prompt = '\n'.join([utterance["content"] for utterance in conversation])  # Using the entire conversation history as the prompt
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=1,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Retrieve the response from the model
            message = response.choices[0].text
            conversation.append({"role": "assistant", "content": message})

            # Print the response
            print(message)
            main(message)

            # Generate speech audio and play it using ElevenLabs voice
            #voice.generate_play_audio_v2(message)


# Call the function to start the assistant
if __name__ == "__main__":
    start_assistant()
