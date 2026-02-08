import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import smtplib
import requests

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
        print("Command:", command)
    except:
        talk("Sorry, I didn't catch that.")
        return ""
    return command

def send_email(receiver, subject, body):
    sender_email = "youremail@gmail.com"
    sender_password = "yourpassword"
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(sender_email, receiver, message)
        server.quit()
        talk("Email has been sent successfully.")
    except:
        talk("Failed to send the email.")

def get_weather(city):
    api_key = "your_openweathermap_api_key"
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        temp = main["temp"]
        desc = data["weather"][0]["description"]
        talk(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
    else:
        talk("City not found.")

def run_advanced_assistant():
    talk("Hello, I am your assistant. What can I do for you?")
    command = listen_command()

    if "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"It's {time}")
    elif "date" in command:
        date = datetime.datetime.now().strftime('%B %d, %Y')
        talk(f"Today's date is {date}")
    elif "search" in command:
        query = command.replace("search", "")
        talk(f"Searching for {query}")
        pywhatkit.search(query)
    elif "email" in command:
        talk("Who do you want to send the email to?")
        receiver = input("Receiver email: ")  # For security
        talk("What's the subject?")
        subject = input("Subject: ")
        talk("What's the message?")
        body = input("Message: ")
        send_email(receiver, subject, body)
    elif "weather" in command:
        talk("Which city?")
        city = listen_command()
        get_weather(city)
    else:
        talk("Sorry, I didn't understand.")

if __name__ == "__main__":
    run_advanced_assistant()
