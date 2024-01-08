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
import platform
import subprocess
import shutil

directory_path = os.getcwd()

for dir in ["/sentMails","/data","/enc_data","/mailbox","/mykeys","/otherskeys"]:
    if not os.path.exists(directory_path+dir):
        os.makedirs(directory_path+dir)



def delete_file_permanently(file_path):
    try:
        if platform.system() == "Windows":
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys("{DEL}")
            os.remove(file_path)
        elif platform.system() == "Darwin":
            subprocess.run(["rm", file_path])
        elif platform.system() == "Linux":
            os.remove(file_path)
        else:
            print("Unsupported operating system.")
    except FileNotFoundError:
        pass
    except Exception as e:
        pass

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

def sendMail(receiver, subject, body, token, flag=False):
    with open("./data/mail", 'w+') as f:
        f.write(f"loremipsumdolorx{subject}-{body}")
    
    with open(f"./otherskeys/public_key.pem", "w") as f:
        publicKeyClient = PublicKeyClient(token)
        pkey_r = publicKeyClient.get_public_key(receiver)
        f.write(pkey_r)
        
    x = encrypt()
    x.run()

    with open("./otherskeys/enc_sym_key", 'rb') as f:
            sym_key = f.read()
    with open("./enc_data/mail", 'rb') as f:
            file_data = f.read()

    mailClient = MailClient(token)
    if flag == False:
        response = mailClient.send_mail(receiver, "Encrypted Subject", file_data, sym_key)
        currTime = time.time()
        with open(f"./sentMails/{email_addr}{currTime}", 'w+') as f:
            f.write(f"To:{receiver}\nSubject:{subject}\nBody:{body}\nTimestamp:{currTime}")
    else:
        response = mailClient.send_mail(receiver, email_addr, file_data, sym_key)
    return response
        
    

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

def sentMails():
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
        to = mail["subject"]
        mail = y.run(mail['receiver'])
        mail = mail.decode().split("-")
        subject = mail[0]
        body = mail[1]
        mailbox.append({"from":sender,
                        "to" : to,
                        "subject":subject,
                        "body":body,
                        "sending_date":time})
        
        with open(f"./sentMails/{time}", 'w') as f:
            f.write(f"From:{sender}\nSubject:{subject}\nBody:{body}\nTimestamp:{time}")


def logout():
    flag = input("Do you want to delete your private key from this computer? (Yes: y / No: n): ").lower()
    if flag == "y":
        private_key_file = f"./mykeys/private{email_addr}.pem"
        try:
            with open(private_key_file, 'r') as f:
                print("\nYour private key:\n")
                print(f.read())
        except:
            print("Private key not found or already deleted.")

        confr = input("\nSave your private key before deleting. Have you saved it? (Yes: y / No: n): ").lower()
        while confr != "y":
            confr = input("Please save your private key. Confirm once saved (Yes: y / No: n): ").lower()

        delete_file_permanently(private_key_file)
        print("Your private key has been deleted.\n")
    
    print("\nLogout completed successfully.\n")


    
    
    
    



while not isSignedIn:
    print("\n~~~~~~~~~~~~ Welcome to End to End Encrypted Https Mail System ~~~~~~~~~~~~\n")
    action = input("1-Sign In\n2-Sign Up\n3-Exit\nChoose an option: ")

    while action not in ["1", "2", "3"]:
        action = input("Invalid operation, try again!\nChoose an option (1-Sign In, 2-Sign Up, 3-Exit): ")
    
    if action == "1":
        print("\n~~ SIGN IN ~~")
        email = input("Please enter your email: ")
        password = input("Please enter your password: ")
        token = signin(email, password)
        while not isinstance(token, dict):
            print(f"\nError: {token}\nTry again.\n")
            email = input("Please enter your email: ")
            password = input("Please enter your password: ")
            token = signin(email, password)
        isSignedIn = True
        print("\nSuccess: Logged in successfully!\n")

    elif action == "2":
        print("\n~~ SIGN UP ~~")
        email = input("Please enter new email address (must be like username@hypersecure.com): ")
        pattern = r'^.+@hypersecure\.com$'
        while not re.match(pattern, email):
            email = input("Invalid format. Enter email (like username@hypersecure.com): ")
        password = input("Please enter password: ")
        password_again = input("Please re-enter password: ")
        token = signup(email, password, password_again)
        while not isinstance(token, dict):
            print(f"\nError: {token}\nTry again.\n")
            email = input("Please enter your email: ")
            password = input("Please enter your password: ")
            password_again = input("Please re-enter password: ")
            token = signup(email, password, password_again)
        isSignedIn = True
        print("\nSuccess: Account created successfully!\n")

    elif action == "3":
        print("\nExiting the system. Goodbye!\n")
        break

while isSignedIn:
    print("\n~~~~~ Please select an operation: ~~~~~")
    action = input("1-Send Mail\n2-See mails\n3-Logout\nChoose an option: ")

    while action not in ["1", "2", "3"]:
        action = input("Invalid operation, try again!\nChoose an option (1-Send Mail, 2-See Mails, 3-Logout): ")
    
    if action == "1":
        print("\n~~ COMPOSE A NEW MAIL ~~")
        receiver = input("Receiver: ")
        subject = input("Subject: ")
        body = input("Body: ")
        response = sendMail(receiver, subject, body, token)
        print(f"\n{response}\n")

    elif action == "2":
        print("\n~~ MAILBOX ~~\n")
        response = mailbox(token)
        if response:
            for count, mail in enumerate(response, start=1):
                print(f"{'-'*40}\n{count}-\nFrom: {mail['from']}\nSubject: {mail['subject']}\nBody: {mail['body']}\nSent at: {mail['sending_date']}\n{'-'*40}")
        else:
            print("No mails to display.\n")

    elif action == "3":
        print("\nLOGGING OUT...")
        logout()
        isSignedIn = False
        token = ""
        print("\nLOGGED OUT successfully.\n")

