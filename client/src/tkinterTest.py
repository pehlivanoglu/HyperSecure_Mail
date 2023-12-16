import tkinter as tk
from tkinter import messagebox, simpledialog

def sign_in():
    # In a real application, validate credentials here
    messagebox.showinfo("Sign In", "Sign In Successful!")
    show_main_menu()

def sign_up():
    messagebox.showinfo("Sign Up", "Sign Up logic goes here")

def show_main_menu():
    # Hide sign in frame and show main menu frame
    frame_signin.pack_forget()
    frame_main_menu.pack(padx=10, pady=10)

def send_email():
    # Logic to send email
    messagebox.showinfo("Send Email", "Send Email logic goes here")

def see_emails():
    # Logic to see emails
    messagebox.showinfo("See Emails", "See Emails logic goes here")

def sign_out():
    # Hide main menu frame and show sign in frame
    frame_main_menu.pack_forget()
    frame_signin.pack(padx=10, pady=10)

# Styling constants
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
TEXT_COLOR = "#333333"
FONT = ("Arial", 12)

# Main window setup
window = tk.Tk()
window.title("Sign In / Sign Up")
window.configure(bg=BG_COLOR)

# Sign In frame
frame_signin = tk.Frame(window, bg=BG_COLOR)

label_username = tk.Label(frame_signin, text="Username:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
label_username.pack()
entry_username = tk.Entry(frame_signin, font=FONT)
entry_username.pack()

label_password = tk.Label(frame_signin, text="Password:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
label_password.pack()
entry_password = tk.Entry(frame_signin, show="*", font=FONT)
entry_password.pack()

button_signin = tk.Button(frame_signin, text="Sign In", command=sign_in, bg=BUTTON_COLOR, fg='white', font=FONT)
button_signin.pack(pady=5)

button_signup = tk.Button(frame_signin, text="Sign Up", command=sign_up, bg=BUTTON_COLOR, fg='white', font=FONT)
button_signup.pack(pady=5)

# Main Menu frame (hidden initially)
frame_main_menu = tk.Frame(window, bg=BG_COLOR)

button_send_email = tk.Button(frame_main_menu, text="Send Email", command=send_email, bg=BUTTON_COLOR, fg='white', font=FONT)
button_send_email.pack(fill='x', padx=5, pady=5)

button_see_emails = tk.Button(frame_main_menu, text="See Emails", command=see_emails, bg=BUTTON_COLOR, fg='white', font=FONT)
button_see_emails.pack(fill='x', padx=5, pady=5)

button_sign_out = tk.Button(frame_main_menu, text="Sign Out", command=sign_out, bg=BUTTON_COLOR, fg='white', font=FONT)
button_sign_out.pack(fill='x', padx=5, pady=5)

# Start with Sign In frame
frame_signin.pack(padx=10, pady=10)

window.mainloop()
