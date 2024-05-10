import requests
from voice.AI_voice import main
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

#ipinfo_token = '4dd1a712dd1121'
#visual_crossing_key = 'J6LHWKPNT2MUEKDHKESEKBYAE'

def get_location(ip, ipinfo_token):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}?token={ipinfo_token}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching location data: {e}")
        return {}

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

def get_weather(latitude, longitude, visual_crossing_key):
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude},{longitude}?key={visual_crossing_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        current_weather = data['currentConditions']
        return {
            'temp': fahrenheit_to_celsius(current_weather['temp']),
            'feels_like': fahrenheit_to_celsius(current_weather['feelslike']),
            'humidity': current_weather['humidity']
        }
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}

def process_command(command, ipinfo_token=None, visual_crossing_key=None):
    if ipinfo_token is None:
        ipinfo_token = '4dd1a712dd1121'
    if visual_crossing_key is None:
        visual_crossing_key = 'J6LHWKPNT2MUEKDHKESEKBYAE'

    if 'weather' in command:
        ip = get_public_ip()
        if ip:
            location_data = get_location(ip, ipinfo_token)
            if 'loc' in location_data:
                latitude, longitude = location_data['loc'].split(',')
                weather_info = get_weather(latitude, longitude, visual_crossing_key)
                print(f"Current Temperature: {weather_info['temp']:.2f}°C")
                main(f"Current Temperature: {weather_info['temp']:.2f}°C")
                print(f"Feels Like: {weather_info['feels_like']:.2f}°C")
                main(f"Feels Like: {weather_info['feels_like']:.2f}°C")
                print(f"Humidity: {weather_info['humidity']}%")
                main(f"Humidity: {weather_info['humidity']}%")
            else:
                print("Location data is incomplete.")
        else:
            print("Failed to detect public IP.")
    elif 'location' in command:
        ip = get_public_ip()
        if ip:
            location_data = get_location(ip, ipinfo_token)
            if 'city' in location_data:
                print(f"City: {location_data['city']}")
                main(f"City: {location_data['city']}")
            else:
                print("City information is not available.")
    else:
        print("Command not recognized. Please type 'weather' or 'location'.")
