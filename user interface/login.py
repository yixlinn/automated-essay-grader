import tkinter as tk
from tkinter import messagebox

# creates the window
root = tk.Tk()
root.title("Login Page")
root.geometry("1920x1080")

# defining a username and password
correct_username = "user"
correct_password = "password123"

# creating a section for a login information so that it is placed in the centre
login_frame = tk.Frame(root)
login_frame.pack(expand=True)

# defining a font and font size
font_style = ("Arial", 18)

# adding input text boxes for username
username_label = tk.Label(login_frame, text="Username:", font=font_style)
username_label.pack(pady=10)
username_entry = tk.Entry(login_frame, font=font_style, width=30)
username_entry.pack(pady=10)

# adding input text boxes for password
password_label = tk.Label(login_frame, text="Password:", font=font_style)
password_label.pack(pady=10)
# this would hide the input and show * instead
password_entry = tk.Entry(login_frame, font=font_style, show="*", width=30)
password_entry.pack(pady=10)

# function to check login credentials
def login():
    username = username_entry.get()
    password = password_entry.get()
    # checking the username and password against the ones defined earlier on
    if username == correct_username and password == correct_password:
        messagebox.showinfo("Login Successful", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")

# login button
login_button = tk.Button(login_frame, text="Login", font=font_style, command=login)
login_button.pack(pady=20)

root.mainloop()