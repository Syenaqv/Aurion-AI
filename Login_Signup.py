#~~ {{ LIBRARIES }} ~~ 
import customtkinter as ctk
import tkinter as tk
import subprocess, sys, os
import tkinter.messagebox as tkmb
from PIL import ImageTk, Image
from tkinter import Label as TkLabel
from CTkMessagebox import CTkMessagebox
import string
import sqlite3

#~~ {{ SETTING UP THE DATABASE }} ~~

connection = sqlite3.connect("Assets/database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT)") # --> This line makes sure that is a database is not found, it will create a database

#~~ {{ APP CREATION }} ~~
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
App = ctk.CTk()
App.geometry("900x700")
App.title("Aurion AI")
# App.resizable(False, False)

#~~ {{ BACKGROUND IMAGE }} ~~
bg_image = Image.open("Assets/bg.png").resize((1130,1000))
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = TkLabel(App, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.config(image=bg_image)

#~~ {{ FUNCTIONS }} ~~

def Login():
    user = Username.get()
    password = Password.get()
    cursor.execute("SELECT * FROM Users WHERE Password = ? AND Username = ?",(password, user))
    result = cursor.fetchall()
    if result:
        tkmb.showinfo(title = "Aurion AI", message = "Logged in Successfully!")
        try:
            App.destroy()
            subprocess.run(["python", "Homepage.py"])
        except FileNotFoundError:
            tkmb.showerror(title="Script Not Found", message="AurionAI not found.")
    else:
        tkmb.showerror(title = "Aurion AI", message = "Login failed. Please try again.")

def SignUp():
  user = Username.get()
  password = Password.get()

  if not user or not password:
      tkmb.showerror(title="Signup Failed", message="Password must contain at least:\n One Number \n One uppercase letter \n One special character ")
      return

  elif not any(char.isdigit() for char in password) or \
         not any(char.isupper() for char in password) or \
         not any(char in string.punctuation for char in password):
        tkmb.showerror(title="Signup Failed", message="Password must contain at least:\n One Number \n One uppercase letter \n One special character ")
        return False
  
  cursor.execute("SELECT * FROM Users WHERE Username=?", (user,)) 
  existing_user = cursor.fetchone()
  if existing_user:
        tkmb.showerror(title="Signup Failed", message="Username already exists.")
        return False

  cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (user, password))
  connection.commit()
  tkmb.showinfo(title="Aurion AI", message="Signed Up Successfully!")
  try:
    App.destroy()
    subprocess.run(["python", "Homepage.py"])
  except FileNotFoundError:
    tkmb.showerror(title="Script Not Found", message="AurionAI not found.")

def Registered():
  Label.configure(text = "")
  SubmitButton.configure(state = "disabled")

  Message = CTkMessagebox(title = "AurionAI", message = "Successfully Registered.", icon="check", option_1="Okay", fg_color = "#333333", bg_color = "#2B2B2B", text_color = "white", title_color = "white", button_text_color = "white")

def ToggleCheck(Value):
    if Value == "Login":
        Label.configure(text=" LOGIN")
        SubmitButton.configure(text="LOG IN", state="normal", command = Login)
        Username.delete(0, tk.END)
        Password.delete(0, tk.END)
    elif Value == "Sign up":
        Label.configure(text=" SIGN UP")
        SubmitButton.configure(text="SIGN UP", command = SignUp)
    else:
        print("Error.")

    MakeGUI()

def MakeGUI():
    Label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    UsernameLabel.place(relx=0.5, rely=0.27, anchor=tk.CENTER)
    Username.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
    PasswordLabel.place(relx=0.5, rely=0.47, anchor=tk.CENTER)
    Password.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    SubmitButton.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
    Toggle.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

#~~ {{ MAIN CODE }} ~~

Mainframe = ctk.CTkFrame(App,
    width=550,
    height=600,
    bg_color = "#000066",
    corner_radius=35)
Mainframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

Label = ctk.CTkLabel(master=Mainframe,
    text=" LOGIN",
    font=('Lexend', 30, 'bold'),
    text_color="white")

UsernameLabel = ctk.CTkLabel(master=Mainframe,
    text="USERNAME",
    font=('Lexend', 16, "bold"),
    text_color="white")

Username = ctk.CTkEntry(master=Mainframe,
    width=350,
    height=50,
    corner_radius=10,
    text_color="black",
    placeholder_text="Enter your Username",
    state="normal",
    font=('Lexend', 14),
    fg_color="#E5E5E5")

PasswordLabel = ctk.CTkLabel(master=Mainframe,
    text="PASSWORD",
    font=('Lexend', 16, "bold"),
    text_color="white")

Password = ctk.CTkEntry(master=Mainframe,
    width=350,
    height=50,
    corner_radius=10,
    text_color="black",
    placeholder_text="Enter your Password",
    state="normal",
    show="•", font=('Lexend', 14),
    fg_color="#E5E5E5")

SubmitButton = ctk.CTkButton(master=Mainframe,
    width=350,
    height=50,
    text="LOG IN",
    font=('Lexend', 18, "bold"),
    # fg_color="#7a4190",
    text_color="white",
    cursor="hand2")

Toggle = ctk.CTkSegmentedButton(Mainframe,
    values=["Login", "Sign up"],
    width=350,
    height=50,
    dynamic_resizing=False,
    fg_color="white",
    text_color="white",
    corner_radius=30,
    font=('Lexend', 14, "bold"),
    command=ToggleCheck)

Toggle.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

App.mainloop()