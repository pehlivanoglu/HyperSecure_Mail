import curses
import re
from apiClient import UserAuthClient
from apiClient import PublicKeyClient
from apiClient import MailClient
from encryption import encrypt
from encryption import decrypt
from encryption import RSA
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import base64
import os
import sys

email_addr = ""
isSignedIn = False
token = ""

def signup(email, password, password_again):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        if password==password_again:
            authClient = UserAuthClient()
            token = authClient.signup(email, password)

            rsa = RSA()
            pkeyClient = PublicKeyClient(token)
            pkeyClient.post_public_key(rsa.run(email))
            global email_addr
            email_addr = email
            return token
        else:
            return "Passwords do not match!"
    else:
        return "Invalid email type!"

def signin(email, password):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        if password:
            authClient = UserAuthClient()
            token = authClient.signin(email, password)
            try:
                token["token"]
                global email_addr
                email_addr = email
                try:
                    with open(f"./mykeys/private{email_addr}.pem", 'r') as f:
                        pass
                except:
                    print("""Your private key does not exist in the local, please provide your private key:\nFor example:\n\n-----BEGIN END PRIVATE KEY-----\n...MIIEBTCCAu2gAwIBAgIUSi0tMerZ...\n-----END PRIVATE KEY-----\n\nYour private key:\n""")
                    print("\nOn Unix-based systems (like Linux and macOS), press Ctrl-D after pasting.On Windows, press Ctrl-Z followed by Enter.\n")
                    privkey = sys.stdin.read()
                    with open(f"./mykeys/private{email_addr}.pem", 'w+') as f:
                        f.write(privkey)

                return token
            except:
                return "Invalid email or password!"
        else:
            return "Please provide a password!"
    else:
        return "Invalid email type!"

def sendMail(receiver, subject, body, token):
    with open("./data/mail", 'w+') as f:
        f.write(f"loremipsumdolorx{subject}-{body}")
    
    with open(f"./otherskeys/public_key.pem", "w") as f:
        publicKeyClient = PublicKeyClient(token)
        try:
            pkey_r = publicKeyClient.get_public_key(receiver)
            f.write(pkey_r)
            x = encrypt()
            x.run()

            with open("./otherskeys/enc_sym_key", 'rb') as f:
                    sym_key = f.read()
            with open("./enc_data/mail", 'rb') as f:
                    file_data = f.read()

            mailClient = MailClient(token)
            response = mailClient.send_mail(receiver, "Encrypted Subject", file_data, sym_key)
            currTime = time.time()
            with open(f"./sentMails/{currTime}", 'w+') as f:
                f.write(f"To:{receiver}\nSubject:{subject}\nBody:{body}\nTimestamp:{currTime}")
            return response
        except:
            print("Receiver's mail address does not exist in our system!")
            return
    

def mailbox(token):
    mailClient = MailClient(token)
    response = mailClient.get_mails()
    mailbox = []
    for mail in response:
        with open("./otherskeys/enc_sym_key", 'wb') as f:
            f.write(base64.b64decode(mail['sym_key']))

        with open("./enc_data/mail", 'wb') as f:
            f.write(base64.b64decode(mail['body']))

        y = decrypt()
        sender = mail['sender']
        time = mail['sending_time']
        mail = y.run(mail['receiver'])
        mail = mail.decode().split("-")
        subject = mail[0]
        body = mail[1]
        mailbox.append({"from":sender,
                        "subject":subject,
                        "body":body,
                        "sending_date":time})
        
        with open(f"./mailbox/{time}", 'w') as f:
            f.write(f"From:{sender}\nSubject:{subject}\nBody:{body}\nTimestamp:{time}")
    
    return mailbox

def logout():
    try:
        os.remove("./data/mail")
    except:
        pass
    try:
        os.remove("./enc_data/mail")
    except:
        pass
    try:
        os.remove("./otherskeys/enc_sym_key")
    except:
        pass
    try:
        os.remove("./otherskeys/public_key.pem")
    except:
        pass
        
    flag = input("Do you want to delete your private key from thic computer?\nYes: y, No: n\n")

    if flag=="y":
        try:
            with open(f"./mykeys/private{email_addr}.pem", 'r') as f:
                print(f.read())
        except:
            pass

        confr = input("If you want to delete, please save your private key.\nIt is not stored anywhere, if you don't save it, you wont be able to connect your mail account again!\nDid you save your private key? Yes: y, No: n\n")
        while confr == "n":
            confr = input("\nIf you want to delete, please save your private key.\nIt is not stored anywhere, if you don't save it, you wont be able to connect your mail account again!\nDid you save your private key? Yes: y, No: n\n")
        
        try:
            os.remove(f"./mykeys/private{email_addr}.pem")
        except:
            pass
        try:
            os.remove(f"./mykeys/public{email_addr}.pem")
        except:
            pass
        print("Your private and public key is deleted!")

    
    folder_path = "./mailbox"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
            
    
    folder_path = "./sentMails"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)


def init_curses():
    window = curses.initscr()
    curses.cbreak()
    curses.noecho()
    window.keypad(True)
    return window

def main_menu(window):
    while True:
        window.clear()
        window.addstr("Welcome to the End-to-End Encrypted Mail System\n")
        window.addstr("1 - Sign In\n")
        window.addstr("2 - Sign Up\n")
        window.addstr("3 - Exit\n")
        window.refresh()

        choice = window.getch()

        if choice == ord('1'):
            signin_form(window)
        elif choice == ord('2'):
            signup_form(window)
        elif choice == ord('3'):
            break

def signin_form(window):
    window.clear()
    curses.echo()

    window.addstr("~~ SIGN IN ~~\n")
    email = get_input(window, "Please enter your email: ")
    password = get_input(window, "Please enter your password: ")
    token = signin(email, password)
    # Handle the sign-in logic and token

def signup_form(window):
    window.clear()
    curses.echo()

    window.addstr("~~ SIGN UP ~~\n")
    email = get_input(window, "Please enter new email address: ")
    password = get_input(window, "Please enter password: ")
    password_again = get_input(window, "Please enter password again: ")
    token = signup(email, password, password_again)
    # Handle the sign-up logic and token

def get_input(window, prompt):
    window.addstr(prompt)
    input_str = window.getstr()
    return input_str.decode()

def display_message(window, message):
    window.addstr(message)
    window.refresh()
    window.getch()


def main():
    window = init_curses()
    try:
        main_menu(window)
    finally:
        curses.endwin()

if __name__ == "__main__":
    main()