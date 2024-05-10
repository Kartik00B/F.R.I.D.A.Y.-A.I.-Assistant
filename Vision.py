import cv2
import argparse
from ultralytics import YOLO
import PIL.Image
import google.generativeai as genai
import threading
import queue
import speech_recognition as sr
from Listen.voice import SpeechRecognitionModel
from voice.AI_voice import main
# Import your API Key configuration and other required modules
from Gemini_API_Key import Gemini_Key

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-time object detection and AI interaction")
    parser.add_argument("--webcam-resolution", default=[1280, 720], nargs=2, type=int)
    return parser.parse_args()

def capture_frames(cap, frame_queue):
    while True:
        ret, frame = cap.read()
        if ret:
            if frame_queue.qsize() < 2:  # Keep only the latest frames
                frame_queue.put(frame)
            else:
                try:
                    frame_queue.get_nowait()  # Discard the oldest frame
                except queue.Empty:
                    pass
                frame_queue.put(frame)

def display_camera_feed(frame_queue):
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            cv2.imshow("Camera Feed", frame)
            if cv2.waitKey(1) == ord('q'):  # Exit on pressing 'q'
                break
    cv2.destroyAllWindows()

def vision():
    args = parse_arguments()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.webcam_resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.webcam_resolution[1])

    frame_queue = queue.Queue(maxsize=2)
    threading.Thread(target=capture_frames, args=(cap, frame_queue), daemon=True).start()
    threading.Thread(target=display_camera_feed, args=(frame_queue,), daemon=True).start()

    #model_yolo = YOLO('yolov8n.pt')
    genai.configure(api_key=Gemini_Key)
    model_gemini = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config={"temperature": 1.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048})

    recognizer = sr.Recognizer()
    #mic = sr.Microphone()

    
    current_frame = None
    while True:
        if current_frame is None:
            current_frame = frame_queue.get()  # Always get the latest frame if none is being processed

        print("Speak a question about the captured frame (say 'quit' to exit):")
        #with sr.Microphone() as source:
            #audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            prompt = SpeechRecognitionModel()
            print("You asked:", prompt)

            if 'what do you see' in prompt.lower():
                current_frame = frame_queue.get()  # Capture new frame on specific prompt

            if prompt.lower() == 'quit':
                cap.release()
                cv2.destroyAllWindows()
                return

            img = PIL.Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
            response_gemini = model_gemini.generate_content([prompt + '\n', img])
            print(response_gemini.text)
            main(response_gemini.text)
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {e}")
        continue
        #finally:
           #cap.release()

#if __name__ == "__main__":
   #vision()


