import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def sign_in():
    # In a real application, validate credentials here
    # messagebox.showinfo("Sign In", "Sign In Successful!")
    show_main_menu()


def show_main_menu():
    # Hide sign in frame and show main menu frame
    frame_signin.pack_forget()
    frame_main_menu.pack()


def open_send_email_page():
    frame_main_menu.pack_forget()
    frame_send_email.pack()


def see_emails():
    # Logic to see emails
    messagebox.showinfo("See Emails", "See Emails logic goes here")


def sign_out():
    # Hide main menu frame and show sign in frame
    frame_main_menu.pack_forget()
    clear_entry(entry_username, entry_password)
    frame_signin.pack()


def register():
    username = entry_username_register.get()
    password = entry_password_register.get()
    confirm_password = entry_confirm_password.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        clear_entry(entry_password_register, entry_confirm_password, entry_username_register)
    elif username == "":
        messagebox.showerror("Error", "Name field cannot be left empty.")
        clear_entry(entry_password_register, entry_confirm_password, entry_username_register)
    elif password == "":
        messagebox.showerror("Error", "Please enter a password.")
        clear_entry(entry_password_register, entry_confirm_password, entry_username_register)
    elif len(password) < 8:
        messagebox.showerror("Error", "Password should contain least 8 characters.")
        clear_entry(entry_password_register, entry_confirm_password, entry_username_register)
    else:
        messagebox.showinfo("Success", f"Registered!\nUsername: {username}\nPassword: {password}")
        clear_entry(entry_password_register, entry_confirm_password, entry_username_register)
        # Here you could add code to store the username and password in a database or file
        frame_register.pack_forget()
        icon_label.pack()
        frame_signin.pack()


def create_registration_window():
    frame_signin.pack_forget()
    clear_entry(entry_username, entry_password)
    frame_register.pack()


def go_back_from_register():
    frame_register.pack_forget()
    clear_entry(entry_password_register, entry_confirm_password, entry_username_register, entry_user_mail_register,
                entry_user_surname_register)
    frame_signin.pack(pady=10, padx=10)


def send_email():
    # Logic to send email
    messagebox.showinfo("Send Email", "Send Email logic goes here")
    clear_entry(to_entry, cc_entry, title_entry)
    mail_entry.delete('1.0', tk.END)


def go_back_from_send_email():
    frame_send_email.pack_forget()
    frame_main_menu.pack(pady=10, padx=10)
    clear_entry(to_entry, cc_entry, title_entry)
    mail_entry.delete("1.0", tk.END)


def get_user_gender():
    gender_selected = gender.get()


def clear_entry(*entry):
    for text in entry:
        text.delete(0, tk.END)


# Styling constants
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#34282C"
TEXT_COLOR = "#333333"
FONT = ("Cambria", 12)

# Main window setup
window = tk.Tk()
window.geometry("400x550")
window.title("Mail Service")
window.configure(bg=BG_COLOR)

# Login Menu Frame
frame_signin = tk.Frame(window, bg=BG_COLOR)

img = ImageTk.PhotoImage(Image.open("/home/pehlivanoglu/Desktop/mail_enc/client/src/icon.png").resize((150, 150)))
window.iconbitmap(img)
icon_label = tk.Label(frame_signin, image=img)
icon_label.pack()

label_username = tk.Label(frame_signin, text="Email address:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, pady=10)
label_username.pack()
entry_username = tk.Entry(frame_signin, font=FONT)
entry_username.pack()

label_password = tk.Label(frame_signin, text="Password:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, pady=10)
label_password.pack()
entry_password = tk.Entry(frame_signin, show="*", font=FONT)
entry_password.pack()

button_signin = tk.Button(frame_signin, width=10, text="Sign In", command=sign_in, bg=BUTTON_COLOR,
                          fg='white', font=FONT)
button_signin.pack(pady=15, padx=10)

button_signup = tk.Button(frame_signin, width=10, text="Sign Up", command=create_registration_window, bg=BUTTON_COLOR,
                          fg='white', font=FONT)
button_signup.pack(pady=0, padx=10)

# Main Menu Frame
frame_main_menu = tk.Frame(window, bg=BG_COLOR)

button_send_email = tk.Button(frame_main_menu, text="Create new email", command=open_send_email_page, bg=BUTTON_COLOR,
                              fg='white', font=FONT)
button_send_email.pack(fill='x', padx=5, pady=5)

button_see_emails = tk.Button(frame_main_menu, text="See Emails", command=see_emails, bg=BUTTON_COLOR, fg='white',
                              font=FONT)
button_see_emails.pack(fill='x', padx=5, pady=5)

button_sign_out = tk.Button(frame_main_menu, text="Sign Out", command=sign_out, bg=BUTTON_COLOR, fg='white', font=FONT)
button_sign_out.pack(fill='x', padx=5, pady=5)

# Register Menu
frame_register = tk.Frame(window, bg=BG_COLOR)
label_title = tk.Label(frame_register, text="REGISTRATION FORM", bg=BG_COLOR, font=("Cambria", 18), fg="Red", pady=30)
label_title.pack()

label_username_register = tk.Label(frame_register, text="Name:", font=("Cambria", 10),
                                   fg=TEXT_COLOR, padx=20, anchor='e')
label_username_register.pack(pady=2, padx=20, anchor=tk.W)
entry_username_register = tk.Entry(frame_register, font=("Cambria", 10))
entry_username_register.pack(pady=2, padx=20)

label_user_surname_register = tk.Label(frame_register, text="Surname:", font=("Cambria", 10),
                                       fg=TEXT_COLOR, padx=20, anchor='e')
label_user_surname_register.pack(pady=2, padx=20, anchor=tk.W)
entry_user_surname_register = tk.Entry(frame_register, font=("Cambria", 10))
entry_user_surname_register.pack(pady=2, padx=20)

label_user_mail_register = tk.Label(frame_register, text="Mail address:", font=("Cambria", 10),
                                    fg=TEXT_COLOR, padx=20)
label_user_mail_register.pack(pady=2, padx=20, anchor=tk.W)
entry_user_mail_register = tk.Entry(frame_register, font=("Cambria", 10))
entry_user_mail_register.pack(pady=2, padx=20)

label_gender_select = tk.Label(frame_register, text="Gender:", font=("Cambria", 10), fg=TEXT_COLOR, padx=20)
label_gender_select.pack(pady=10, padx=20)

gender = tk.IntVar()

male_radio = tk.Radiobutton(frame_register, text="Male", value=1, command=get_user_gender, state="normal")
male_radio.pack()

female_radio = tk.Radiobutton(frame_register, text="Female", value=2, command=get_user_gender, state="normal")
female_radio.pack(pady=10)

label_password_register = tk.Label(frame_register, text="Please enter password:", font=("Cambria", 10),
                                   fg=TEXT_COLOR, padx=20)
label_password_register.pack(pady=2, padx=20, anchor=tk.W)
entry_password_register = tk.Entry(frame_register, show="*", font=("Cambria", 10))
entry_password_register.pack(pady=5, padx=20)

label_confirm_password = tk.Label(frame_register, text="Confirm Password:", font=("Cambria", 10),
                                  fg=TEXT_COLOR, padx=20)
label_confirm_password.pack(pady=2, padx=20, anchor=tk.W)
entry_confirm_password = tk.Entry(frame_register, show="*", font=("Cambria", 10))
entry_confirm_password.pack(pady=2, padx=20)

button_register = tk.Button(frame_register, text="Register", command=register, padx=10)
button_register.pack(pady=20)

button_go_back = tk.Button(frame_register, text="Back", command=go_back_from_register, padx=20)
button_go_back.pack()

# Send E-mail Frame
frame_send_email = tk.Frame(window, bg=BG_COLOR)

labels = ["To:", "Cc:", "Title:", "Mail:"]
for i, label_text in enumerate(labels):
    label = tk.Label(frame_send_email, text=label_text)
    label.grid(row=i, column=2, sticky="w", padx=5, pady=5)

# Entry fields
to_entry = tk.Entry(frame_send_email)
to_entry.grid(row=0, column=3, padx=5, pady=5)

cc_entry = tk.Entry(frame_send_email)
cc_entry.grid(row=1, column=3, padx=5, pady=5)

title_entry = tk.Entry(frame_send_email)
title_entry.grid(row=2, column=3, padx=5, pady=5)

mail_entry = tk.Text(frame_send_email, height=10, width=40)
mail_entry.grid(row=3, column=3, padx=5, pady=5)

send_button = tk.Button(frame_send_email, text="Send", command=send_email, pady=10, padx=20)
send_button.grid(row=6, column=3, pady=20)
button_go_back_send_email = tk.Button(frame_send_email, text="Back", command=go_back_from_send_email, pady=10, padx=20)
button_go_back_send_email.grid(row=7, column=3, pady=10)

# Start with Sign In frame
frame_signin.pack(padx=10, pady=10)

window.mainloop()
