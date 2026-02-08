import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit

# Initialize the speech engine
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = listener.listen(source)

    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("User said:", command)
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        talk("Network error.")
        return ""
    return command

def run_voice_assistant():
    command = listen_command()

    if "hello" in command:
        talk("Hello! How can I help you?")
    elif "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time}")
    elif "date" in command:
        date = datetime.datetime.now().strftime('%B %d, %Y')
        talk(f"Today's date is {date}")
    elif "search for" in command:
        query = command.replace("search for", "")
        talk(f"Searching for {query}")
        pywhatkit.search(query)
    else:
        talk("I can only greet, tell time or date, or search for now.")

if __name__ == "__main__":
    run_voice_assistant()
