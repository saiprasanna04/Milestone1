import sounddevice as sd  
import numpy as np  
import speech_recognition as sr  
import pyttsx3  

duration = 5 
sample_rate = 44100  
engine = pyttsx3.init()  
  
def generate_response(text):  
    responses = {  
        "hello": "Hello! How can I assist you?",  
        "how are you": "I'm fine, thank you! How about you?",  
        "what is your name": "I am your voice assistant.",  
        "what can you do": "I can help you with various tasks, like answering questions or recording notes.",  
        "exit": "Goodbye!"  
    }    
    text = text.lower()  
    for key in responses:  
        if key in text:  
            return responses[key]   
    return "I'm not sure how to respond to that."  

def record_audio(duration, sample_rate):  
    print("Recording...")  
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')  
    sd.wait()  
    print("Recording complete.")  
    return audio_data  

def recognize_speech(audio_data, sample_rate):  
    recognizer = sr.Recognizer()  
    audio_data = np.array(audio_data, dtype=np.float32)  
    audio_data = sr.AudioData(audio_data.tobytes(), sample_rate, 4)  

    try:  
        print("Recognizing speech...")  
        text = recognizer.recognize_google(audio_data)  
        print(f"Recognized Text: {text}")  
        return text  
    except sr.UnknownValueError:  
        print("Could not understand the audio.")  
        return None  
    except sr.RequestError as e:  
        print(f"Could not request results from the speech recognition service: {e}")  
        return None  

def speak_text(text):  
    engine.say(text)  
    engine.runAndWait()  

def main():
    while True:  
        user_prompt = input("Enter your prompt (or press Enter to use voice): ")  

        if user_prompt:
            print(f"User 's prompt: {user_prompt}")
            response = generate_response(user_prompt)
            print(f"Assistant: {response}")
            speak_text(response)

            if "exit" in user_prompt.lower():  
                break  

        else:
            audio_data = record_audio(duration, sample_rate)  

            recognized_text = recognize_speech(audio_data, sample_rate)  

            if recognized_text:  
                response = generate_response(recognized_text)  
                print(f"Assistant: {response}")  
                speak_text(response)  

                if "exit" in recognized_text.lower():  
                    break  
            else:  
                print("No valid speech recognized.")

if __name__ == "__main__":
    main()



