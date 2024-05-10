import cohere
from voice.AI_voice import main
# Initialize the Cohere client with your API key
co = cohere.Client(api_key="your API key")

def ai(user_input):
    try:
        # Use Cohere to generate a response
        response = co.generate(
            # Choose the model size; "large" is typically more precise
            prompt=user_input,
            max_tokens=256,  # Lower the max tokens to limit the length of the response
            temperature=1.9,  # Lower the temperature for more deterministic responses
            stop_sequences=["\n", ".", "!", "?"],  # Stops at various sentence ending markers
            frequency_penalty=0.5,
            presence_penalty=0
        )
        
        # Extract the first sentence or segment to ensure single-line output
        text = response.generations[0].text.strip()
        first_sentence = text.split("\n")[0].split(".")[0].strip()
        print(first_sentence)
        main(first_sentence)
        # Return the formatted single-line AI response
        return text
    except Exception as e:
        print("Error:", str(e))
        return None
