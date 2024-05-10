import subprocess
import speech_recognition as sr
from Listen.voice import SpeechRecognitionModel
import sys
from voice.AI_voice import main
installed_apps = {
    'system idle process': None, 
    'system': '', 
    '': '', 
    'powerpoint': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
    'word': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
    'excel': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
    'python ide': 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2023.3.3\\bin\\pycharm64.exe', 
    'brave': 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',  
    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 
    'vs code': 'C:\\Users\\karti\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe', 
    'spotify': 'C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.233.1042.0_x64__zpdnekdrzrea0\Spotify.exe',  
    'python': 'C:\\Users\\karti\\AppData\\Local\\Programs\\Python\\Python311\\python.exe', 
    'powershell': 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',  
    'whatsapp': 'whatsapp.exe',  
    'explorer': 'C:\\Windows\\explorer.exe', 
    'securityhealthservice': 'C:\\Windows\\System32\\SecurityHealthService.exe', 
    'settings': 'C:\\Windows\\ImmersiveControlPanel\\SystemSettings.exe', 
    'camera': 'Camera.exe',  # Camera application (pre-installed)
    'notepad': 'notepad.exe',  # Notepad application (pre-installed)
}

def launch_application(application_name):
    if application_name is None:
        print("No application name provided.")
        return

    application_name = application_name.lower()  # Convert input to lowercase
    application_name = application_name.replace("open ", "")  # Remove "open " prefix
    
    if application_name in installed_apps:
        application_path = installed_apps[application_name]
        if application_path:
            try:
                subprocess.Popen([application_path])  # Launch the application
                print(f"Launching {application_name} from {application_path}")
        
            except Exception as e:
                print(f"Failed to launch {application_name}: {e}")
        else:
            print(f"Application '{application_name}' is not installed or path is not available.")
    else:
        print(f"Application '{application_name}' not found in the list.")

def get_voice_command():
    while True:
        try:
            command = SpeechRecognitionModel().lower()
            print("You said:", command)
            if command.startswith("open"):
                launch_application(command)
            
            if "exit" in command:
                main("Closing app launcher")
                return
            else:
                print("Invalid command. Please say 'open' followed by the application name.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

#if __name__ == "__main__":
    #get_voice_command()
