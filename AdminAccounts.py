import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import ttk

Connect = sqlite3.connect("Assets/database.db")
cursor = Connect.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, Type TEXT, Username TEXT, Password TEXT)")
Connect.commit()
Connect.close()

Root = ctk.CTk()
Root.geometry("900x600")
Root.title("Ai ")
Root.resizable(0,0)

Databaseframe = ctk.CTkFrame(Root,
    width = 850,
    height = 450)

def DeleteUsers():
    SelectUser = Tree.selection()
    if SelectUser:
        UserID = Tree.item(SelectUser)["values"][0]
        Connect = sqlite3.connect("Assets/database.db")
        cursor = Connect.cursor()
        cursor.execute("DELETE FROM Users WHERE id = ?", (UserID,))
        Connect.commit()
        Connect.close()
        ViewUsersDetails()
    else:
        pass


DeleteButton = ctk.CTkButton(Databaseframe,
    width = 200,
    height = 50,
    corner_radius = 10,
    text = "Delete",
    fg_color = "#505050",
    cursor = "hand2",
    font = ('Helvetica' ,18, "bold"),
    command = DeleteUsers)

def ViewUsersDetails():
    for item in Tree.get_children():
        Tree.delete(item)
    Connect = sqlite3.connect("Assets/database.db")
    cursor = Connect.cursor()
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()
    for row in rows:
        Tree.insert("", tk.END, values=row)
    Connect.close()



Tree = ttk.Treeview(Databaseframe, 
    col = ("Col1", "Col2", "Col3", "Col4"),    
    show = "headings",
    height = 15)

Tree.column("#1", anchor = tk.CENTER)
Tree.heading("#1", text = "ID")
Tree.column("#2", anchor = tk.CENTER)
Tree.heading("#2", text = "Username")
Tree.column("#3", anchor = tk.CENTER)
Tree.heading("#3", text = "Password")

ViewUsersDetails()

Databaseframe.place(relx = 0.45, rely = 0.6, anchor = tk.CENTER)
DeleteButton.place(relx = 0.77, rely = 0.85, anchor = tk.CENTER)
Tree.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)
Root.mainloop()