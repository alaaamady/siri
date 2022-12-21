import speech_recognition
import pyttsx3 as tts
import sys
import wikipedia
import webbrowser
import os
recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 180)

todo_list = ["Go Shopping", "Clean Room", "Record Video"]
speaker.say("Hello, I'm your voice assistant, how can I help you")


def speak(audio):
    speaker.say(audio)
    speaker.runAndWait()


def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        query = ''
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except speech_recognition.UnknownValueError:
        speak("Unable to Recognize your voice.")
    except speech_recognition.RequestError:
        speak("sorry my speech service is down")
    return query


def create_note():
    global recognizer
    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=2.0)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the todo {filename}")
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! please")
            speaker.runAndWait()


def add_todo():
    global recognizer
    speaker.say("What todo do you want to add?")
    speaker.runAndWait()
    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"I added {item} to the to do list!")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand. Please try again!")
            speaker.runAndWait()


def show_todos():
    speaker.say("The item on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def change_voice():
    speaker.say("Would you like to change to Male or Female Voice?")
    speaker.runAndWait()
    done = False

    while not done:
        gender = takeCommand()
        print(gender)
        genderIndex = 1
        if gender == 'female':
            genderIndex = 1
        voices = speaker.getProperty('voices')
        print(voices)
        speaker.setProperty('voice', voices[genderIndex].id)
        speak("Voice changed successfully")
        done = True


def hello():
    speaker.say("Hello what can I do for you?")
    speaker.runAndWait()


def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit
}

while True:
    try:
        recognizer = speech_recognition.Recognizer()
        speaker.runAndWait()
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("Listening...")
            audio = recognizer.listen(mic)
            print("Recognizing")
            if audio:
                message = recognizer.recognize_google(audio)
                message = message.lower()
                print(message)
                if message == "hello":
                    hello()
                elif message == "change voice":
                    change_voice()
                elif message == "show to-do list":
                    show_todos()
                elif message == "create to-do item":
                    add_todo()
                elif message == "create note":
                    create_note()
                elif message == "search in wikipedia":
                    speak('What do you want to search wikipedia for?')
                    query = takeCommand()
                    results = wikipedia.summary(query, sentences=3)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                elif message == "goodbye":
                    quit()
                elif 'search for' in message:
                    message = message.replace("search for", "")
                    speak("Here's your search results in Google\n")
                    webbrowser.open(f"https://www.google.com/search?q={message}")
                elif "open youtube" in message:
                    message = message.replace("open youtube", "")
                    message = message.replace(" ", "+")
                    speak("Here's your request on youtube")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={message}")
                elif "open word" in message:
                    speak("opening word")
                    os.startfile("C:/Users/DELL 5520/Desktop/speech-processing-task.docx")
                else:
                    speak("I can't do that")
            speak("What else can I help you with?")
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
