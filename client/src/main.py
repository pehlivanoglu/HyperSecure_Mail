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
import getpass
import signal

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def color_text(text, color):
    return color + text + Color.RESET

try:
    def signal_handler(signum, frame):
        if signum == signal.SIGTSTP:
            raise KeyboardInterrupt
        
    def clear_terminal():
        os_name = platform.system()
        if os_name == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    clear_terminal()
    signal.signal(signal.SIGTSTP, signal_handler)
    
    directory_path = os.getcwd()
    print(f"\nCurrent working directory: {directory_path}")
    for dir in ["/.data","/.enc_data","/.mykeys","/.otherskeys"]:
        if not os.path.exists(directory_path+dir):
            os.makedirs(directory_path+dir)

    def delete_file_permanently(file_path):
        try:
            if platform.system() == "Darwin":
                subprocess.run(["rm", file_path])
            elif platform.system() == "Linux":
                os.remove(file_path)
            else:
                print(color_text("\nUnsupported operating system.\n", Color.RED))
        except FileNotFoundError:
            pass
        except Exception as e:
            print(color_text(f"\nError: {str(e)}", Color.RED))

    email_addr = ""
    isSignedIn = False
    token = ""

    

    def signup(email, password, password_again):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            if password==password_again:
                authClient = UserAuthClient()
                token = authClient.signup(email, password)

                if token != "This email is in use!":
                    rsa = RSA()
                    pkeyClient = PublicKeyClient(token)
                    pkeyClient.post_public_key(rsa.run(email))
                    global email_addr
                    email_addr = email
                    return token
                else:
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
                        with open(f"{directory_path}/.mykeys/private{email_addr}.pem", 'r') as f:
                            pass
                    except:
                        clear_terminal()
                        
                        print(color_text("""\n!!!!!!!! WARNING !!!!!!!! Your private key does not exist in the local, please provide your private key to sign-in:\n\nFor example:\n\n-----BEGIN PRIVATE KEY-----\n... MIIEBTCCAu2gAwIBAgIUSi0tMerZ ...\n-----END PRIVATE KEY-----\n""", Color.RED))
                        print(color_text("\nOn Unix-based systems (like Linux and macOS), press Ctrl-D or Command-D to finish pasting. On Windows, press Ctrl-Z.\n", Color.YELLOW))
                        print("Your private key:\n")
                        privkey = sys.stdin.read()
                        with open(f"{directory_path}/.mykeys/private{email_addr}.pem", 'w+') as f:
                            f.write(privkey)

                    return token
                except:
                    return "Invalid email or password!"
            else:
                return "Please provide a password!"
        else:
            return "Invalid email type!"

    def sendMail(receiver, subject, body, token, flag=False):
        with open(f"{directory_path}/.data/mail", 'w+') as f:
            f.write(f"loremipsumdolorx{subject}-{body}")
        
        with open(f"{directory_path}/.otherskeys/public_key.pem", "w") as f:
            publicKeyClient = PublicKeyClient(token)
            pkey_r = publicKeyClient.get_public_key(receiver)
            f.write(pkey_r)
            
        x = encrypt()
        x.run()

        with open(f"{directory_path}/.otherskeys/enc_sym_key", 'rb') as f:
                sym_key = f.read()
        with open(f"{directory_path}/.enc_data/mail", 'rb') as f:
                file_data = f.read()

        mailClient = MailClient(token)

        if not flag:
            response = mailClient.send_mail(receiver, "Encrypted Subject", file_data, sym_key)
            return response
        
        elif flag:
            response = mailClient.send_mail(email_addr, receiver, file_data, sym_key)
        
            
        

    def mailbox(token):
        mailClient = MailClient(token)
        response = mailClient.get_mails()
        mailbox = []
        if response == "Mailbox empty":
            return "Mailbox empty"
        
        for mail in response:
            if mail["subject"] == "Encrypted Subject":
                with open(f"{directory_path}/.otherskeys/enc_sym_key", 'wb') as f:
                    f.write(base64.b64decode(mail['sym_key']))

                with open(f"{directory_path}/.enc_data/mail", 'wb') as f:
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
    
        return mailbox

    def sentMails(token):
        mailClient = MailClient(token)
        response = mailClient.get_sent_mails()
        sent = []
        if response == "No sent mails":
            return "No sent mails"

        for mail in response:
            if mail["subject"] != "Encrypted Subject":
                with open(f"{directory_path}/.otherskeys/enc_sym_key", 'wb') as f:
                    f.write(base64.b64decode(mail['sym_key']))

                with open(f"{directory_path}/.enc_data/mail", 'wb') as f:
                    f.write(base64.b64decode(mail['body']))
                
                y = decrypt()
                time = mail['sending_time']
                mail = y.run(mail['receiver'])
                mail = mail.decode().split("-")
                to = mail[0]
                subject = mail[1]
                body = mail[2]
                sent.append({   "to":to,
                                "subject":subject,
                                "body":body,
                                "sending_date":time})

        
        if len(sent) == 0:
            return "No sent mails"
        
        return sent


    def logout():
        flag = input(color_text("\nDo you want to keep your private key in this computer?\nChoose yes only if you trust this computer! (Yes: y / No: n): ",Color.RED)).lower()
        if flag == "n":
            private_key_file = f"{directory_path}/.mykeys/private{email_addr}.pem"
            try:
                with open(private_key_file, 'r') as f:
                    print("\nYour private key:\n\n")
                    print(f.read())
                    confr = input(color_text("\n\nYour private key is not stored anywhere.\nYou will not be able to sign in anymore if you delete without saving.\nSave (copy somewhere you think is safe) your private key before deleting. Have you saved it? (Yes: y / No: n): ",Color.RED)).lower()
                    while confr != "y":
                        confr = input("\nPlease save your private key. Confirm once saved (Yes: y / No: n): ").lower()

                    delete_file_permanently(private_key_file)
                    print("\nYour private key has been deleted.\n")
            except:
                print("Private key not found or already deleted.")

            time.sleep(2)
            
            clear_terminal()


        
        
        
        



    while not isSignedIn:
        print(color_text("\n\n~~~~~~~~~~~~ Welcome to HYPERSECURE : End to End Encrypted Https Mail Service ~~~~~~~~~~~~\n\n",Color.CYAN))
        action = input("\n1-Sign In\n2-Sign Up\n3-Exit\n\nChoose an option: ")

        while action not in ["1", "2", "3"]:
            action = input("\nInvalid operation, try again!\nChoose an option (1-Sign In, 2-Sign Up, 3-Exit): ")
            clear_terminal()
        
        if action == "1":
            print("\n~~ SIGN IN ~~")
            email = input("\nPlease enter your email: ")
            password = getpass.getpass("Please enter your password: ")
            token = signin(email, password)
            while not isinstance(token, dict):
                clear_terminal()
                print(f"\nError: {token}\nTry again.\n")
                email = input("\nPlease enter your email: ")
                password = getpass.getpass("Please enter your password: ")
                token = signin(email, password)
            isSignedIn = True
            clear_terminal()
            print("\nSuccess: Logged in successfully!\n")
            

        elif action == "2":
            clear_terminal()
            print("\n~~ SIGN UP ~~")
            email = input("\n\nPlease enter new email address (must be like <username>@hypersecure.com): ")
            pattern = r'^.+@hypersecure\.com$'
            while not re.match(pattern, email):
                clear_terminal()
                email = input("\n\nInvalid format. Enter email (like <username>@hypersecure.com): ")
            password = getpass.getpass("\nPlease enter your password: ")
            password_again = getpass.getpass("\nPlease re-enter your password: ")
            token = signup(email, password, password_again)
            while not isinstance(token, dict):
                clear_terminal()
                print(f"\nError: {token}\n\nTry again.\n")
                email = input("\n\nPlease enter your email: ")
                password = getpass.getpass("\nPlease enter your password: ")
                password_again = getpass.getpass("\nPlease re-enter your password: ")
                token = signup(email, password, password_again)
            isSignedIn = True
            clear_terminal()
            print("\nSuccess: Account created successfully!\n")
            

        elif action == "3":
            print("\nExiting the system. Goodbye!\n")
            break

    while isSignedIn:
        print("\n~~~~~ Please select an operation: ~~~~~")
        action = input("\n\n1-Compose a new mail\n2-Mailbox\n3-See Sent Mails\n4-Send mail to external mail address (Beta)\n5-Logout\nChoose an option: ")

        while action not in ["1", "2", "3","4", "5"]:
            clear_terminal()
            action = input("\n\nInvalid operation, try again!\nChoose an option (1-Compose a new mail, 2-Mailbox, 3-See Sent Mails, 4-Send mail to external mail address (Beta), 5-Logout): ")
        
        if action == "1":
            clear_terminal()
            print("\n~~ COMPOSE A NEW MAIL ~~")
            receiver = input("\nReceiver: ")
            subject = input("\nSubject: ")
            body = input("\nBody: ")
            try:
                response = sendMail(receiver, subject, body, token)
                sendMail(email_addr, f"{receiver}-{subject}", body, token, flag=True)
                print(f"\n{response}\n")
            except:
                clear_terminal()
                print(f"\nWARNING!!!: {receiver} is not enrolled to our service, mail could not be sent. Please contact the owner of {receiver} to get him/her enrolled :) !")
            

        elif action == "2":
            clear_terminal()
            print("\n~~ MAILBOX ~~\n")
            response = mailbox(token)
            if response != "Mailbox empty":
                for count, mail in enumerate(response, start=1):
                    print(f"\n{'-'*40}\n{count}-\nFrom: {mail['from']}\nSubject: {mail['subject']}\nBody: {mail['body']}\nSent at: {mail['sending_date']}\n{'-'*40}")
            else:
                print("\nNo mails to display.\n")

        elif action == "3":
            clear_terminal()
            print("\n~~ SENT MAILS ~~\n")
            response = sentMails(token)
            if response != "No sent mails":
                for count, mail in enumerate(response, start=1):
                    print(f"\n{'-'*40}\n{count}-\nTo: {mail['to']}\nSubject: {mail['subject']}\nBody: {mail['body']}\nSent at: {mail['sending_date']}\n{'-'*40}")
            else:
                print("\nNo mails sent.\n")


        elif action == "4":
            mailClient = MailClient(token)
            receiver = input("\nReceiver: ")
            response = mailClient.send_out_mail(receiver, "", "")

        elif action == "5":
            logout()
            isSignedIn = False
            token = ""



except KeyboardInterrupt:
    print(color_text("\n\nEXITING WITH KEYBOARD INTERRUPTION!\n", Color.YELLOW))
    logout()

except ValueError:
    print(color_text("Your private key is not valid!\n", Color.RED))
    print("Please check your private key's validity!")
    time.sleep(4)

except Exception:
    print("Connection error , please check your internet connection!")
    
finally:
    for dir in ["/.data","/.enc_data","/.otherskeys"]:
            if os.path.exists(directory_path+dir):
                shutil.rmtree(directory_path+dir)

    if not os.listdir(directory_path+"/.mykeys"):
            os.rmdir(directory_path+"/.mykeys")

    time.sleep(2)
    clear_terminal()
    print("\nLOGGED OUT from Hypersecure successfully.\n")
