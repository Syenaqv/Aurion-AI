#~~ {{ LIBRARIES }} ~~

import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import pyttsx3, random, webbrowser, datetime, requests, pyautogui, json, spotipy
import speech_recognition, os
from pynput.keyboard import Key,Controller
from time import sleep
import subprocess, sys, threading

#~~ {{ GLOBAL VARIABLES }} ~~
topWidget = None

#~~ {{ APP CREATION }} ~~

mode = "dark"
ctk.set_appearance_mode(mode)
ctk.set_default_color_theme("blue")
App = ctk.CTk()
App.geometry("650x500")
App.title("Aurion AI")
App.resizable(0, 0)

dialogue = ""
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate",170)
Keyboard = Controller()

#~~ {{ FUNCTIONS }} ~~

def toggleWidget():
    global topWidget
    if topWidget:
      topWidget.destroy()  # Destroy the existing top-level window if it exists

    topWidget = ctk.CTkToplevel()
    topWidget.title("AI Chat")
    topWidget.overrideredirect(True)
    topWidget.geometry("300x400+{}+{}".format(App.winfo_screenwidth() - 300, App.winfo_screenheight() - 700))
    topWidget.wm_attributes("-topmost", True)
    Output2 = ctk.CTkTextbox(master=topWidget,
      font=("Roboto", 20),
      wrap=tk.WORD,
      state=tk.DISABLED,
      width=100,
      height=100,
      corner_radius=10,
      fg_color="#303030",
      bg_color="#303030")
    Output2.pack(fill=tk.BOTH, expand=True)
    SpeakButton = ctk.CTkButton(topWidget,
        width = 200,
        height = 30,
        text = "Speak",
        fg_color="#606060",
        cursor = "hand2",
        command = VoiceAssistant)

    SpeakButton.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def volumeup():
    for i in range(5):
        Keyboard.press(Key.media_volume_up)
        Keyboard.release(Key.media_volume_up)
        sleep(0.1)
def volumedown():
    for i in range(5):
        Keyboard.press(Key.media_volume_down)
        Keyboard.release(Key.media_volume_down)
        sleep(0.1)

def getTimeDialogue():
    global time
    global dialogue
    time = int(datetime.datetime.now().hour)
    if time >= 5 and time <= 12:
        dialogue = "Good Morning"
    elif time >= 13 and time <= 15:
        dialogue = "Good Afternoon"
    elif time >= 17 and time <= 19:
        dialogue = "Good Evening"
    elif time >= 21 and time <= 4:
        dialogue = "Good Night"
    else:
        dialogue = "Good Day"

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Aurion: Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)
    try:
        print("Aurion: Interpreting...")
        query  = r.recognize_google(audio,language='en-in')
        print(f"User: {query}")
    except Exception as e:
        print("Aurion: Can you repeat the command please.")
        return "None"
    return query

def VoiceAssistant():
    query = takeCommand().lower()
    inputted = query.capitalize()
    ctk.CTkLabel(Output, text = f"User: {inputted}", font = ("Calibri", 20, "bold")).pack(pady = 10)
    if TopLevelToggleVar.get() == True:
      ctk.CTkLabel(topWidget, text = f"User: {inputted}", font = ("Calibri", 20, "bold")).pack(pady = 10)
    else:
       print()
    if "google" in query:
        from SearchNow import searchGoogle
        searchGoogle(query)
        output = f"Searched for {query}"
    elif "youtube" in query:
        from SearchNow import searchYoutube
        searchYoutube(query)
        output = f"Searched for {query}"
    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M")
        output = f"Sir, the time is {strTime}"   
        speak(f"Sir, the time is {strTime}")
    elif "volume up" in query:
        speak("Turning volume up, Sir")
        output = "Turning volume up, Sir"
        volumeup()
    elif "volume down" in query:
        speak("Turning volume down, Sir")
        output = "Turning volume down, Sir"
        volumedown()
    elif "remember" in query:
        speak("What would you like me to remember?")
        ctk.CTkLabel(Mainframe, text = "What would you like me to remember?", font = ("Calibri", 20, "bold")).pack(pady = 10)
        rememberMessage = takeCommand()
        speak("You told me to remember "+ rememberMessage)
        output = f"You told me to remember {rememberMessage}"
        remember = open("Assets/Remember.txt","a")
        remember.write(rememberMessage)
        remember.write("\n")
        remember.close()
    elif "remind me" in query:
        remember = open("Assets/Remember.txt","r")
        speak("You told me to remember" + remember.read())
        output = "You told me to remember" + remember.read()
    elif "shutdown the system" in query:
        speak("Are You sure you want to shutdown")
        output = "Are You sure you want to shutdown?"
        shutdown = takeCommand()
        if "yes" in shutdown:
            os.system("shutdown /s /t 1")
        else:
            speak("Going back to sleep")
    elif "clear remind list" in query:
        remember = open("Assets/Remember.txt","w")
        remember.close()
        speak("Cleared remind list.")
        output = "Cleared remind list."
    else:
        speak("Command not recognised, Going back to sleep.")
        output = "Command not recognised, Going back to sleep."
    ctk.CTkLabel(Output, text = f"Aurion: {output}", font = ("Calibri", 20, "bold")).pack(pady = 10)
    if TopLevelToggleVar.get() == True:
      ctk.CTkLabel(topWidget, text = f"Aurion: {output}", font = ("Calibri", 20, "bold")).pack(pady = 10)
    else:
      print()

def AppearanceEvent(Value):
  ctk.set_appearance_mode(Value)

def tSwitch():
  if TopLevelToggleVar.get() == True:
    toggleWidget()
  else:
    global topWidget
    topWidget.destroy()

def HideOthers():
  SettingsLabel.place_forget()
  AppearenceLabel.place_forget()
  TopLevelLabel.place_forget()
  LanguageLabel.place_forget()
  KeybindsLabel.place_forget()
  Output.place_forget()
  Output.place_forget()
  VCButton.place_forget()

  Modes.place_forget()
  TopLevelToggle.place_forget()
  Language.place_forget()

def HomeGUI():
  HideOthers()
  Output.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
  VCButton.place(relx = 0.5, rely = 0.9, anchor = tk.CENTER)

def SettingsGUI():
  HideOthers()
  SettingsLabel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
  AppearenceLabel.place(relx=0.25, rely=0.25, anchor=tk.CENTER)
  TopLevelLabel.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
  LanguageLabel.place(relx=0.25, rely=0.45, anchor=tk.CENTER)
  KeybindsLabel.place(relx=0.25, rely=0.55, anchor=tk.CENTER)

  Modes.place(relx=0.8, rely=0.25, anchor=tk.CENTER)
  TopLevelToggle.place(relx=0.8, rely=0.35, anchor=tk.CENTER)
  Language.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

def logout():
  App.destroy()
  try:
    subprocess.run(["python", "main.py"])
  except Exception as e:
    print(f"Error running main.py: {e}")

#~~ {{ MAIN CODE }} ~~

MenuPanel = ctk.CTkFrame(App, 
  width = 150,
  height = 450,
  corner_radius = 10)

Mainframe = ctk.CTkFrame(App, 
  width=455, 
  height=450, 
  corner_radius=10)

AurionLabel = ctk.CTkLabel(MenuPanel,
  width=100,
  height=50,
  text="Aurion",
  font=("Calibri", 25, "bold"))

HomeButton = ctk.CTkButton(MenuPanel,
  width=100,
  height=30,
  fg_color="#606060",
  text="Home",
  corner_radius=10,
  command=HomeGUI)

SettingsButton = ctk.CTkButton(MenuPanel,
  width=100,
  height=30,
  fg_color="#606060",
  text="Settings",
  corner_radius=10,
  command=SettingsGUI)

ExitButton = ctk.CTkButton(MenuPanel,
  width=100,
  height=30,
  fg_color="#606060",
  text="Exit",
  corner_radius=10,
  command=logout)

SettingsLabel = ctk.CTkLabel(Mainframe,
  width=100,
  height=100,
  text="Settings",
  font=("Calibri", 25, "bold"))

AppearenceLabel = ctk.CTkLabel(Mainframe,
  width=100,
  height=50,
  text="Appearance Mode",
  font=("Calibri", 15, "bold"))

TopLevelLabel = ctk.CTkLabel(Mainframe,
  width=100,
  height=50,
  text="Top Level",
  font=("Calibri", 15, "bold"))

TopLevelToggleVar = ctk.IntVar()
TopLevelToggle = ctk.CTkSwitch(Mainframe, width=100, height=50, text="",variable=TopLevelToggleVar, command=tSwitch)

LanguageLabel = ctk.CTkLabel(Mainframe,
  width=100,
  height=50,
  text="Preferred Language",
  font=("Calibri", 15, "bold"))

KeybindsLabel = ctk.CTkLabel(Mainframe,
  width=100,
  height=50,
  text="Keybinds",
  font=("Calibri", 15, "bold"))

Output = ctk.CTkScrollableFrame(Mainframe,
    label_text= "Output",
    label_font = ("Calibri", 20, "bold"),
    width = 420,
    height = 380)

VCButton = ctk.CTkButton(Mainframe,
    width = 200,
    height = 30,
    text = "Speak",
    fg_color="#606060",
    cursor = "hand2",
    command = VoiceAssistant)

Modes = ctk.CTkComboBox(Mainframe,
  values=["Dark", "Light", "System"],
  command=AppearanceEvent)

Language = ctk.CTkComboBox(Mainframe, values=["English", "French", "Spanish"])

Language.set("English")
Modes.set("Dark")

AurionLabel.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
HomeButton.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
SettingsButton.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
ExitButton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

MenuPanel.place(relx=0.15, rely=0.5, anchor=tk.CENTER)
Mainframe.place(relx=0.63, rely=0.5, anchor=tk.CENTER)
Output.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)
VCButton.place(relx = 0.5, rely = 0.9, anchor = tk.CENTER)

# Display the main application window
App.mainloop()