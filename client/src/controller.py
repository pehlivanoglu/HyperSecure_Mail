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
    with open(f"./sentMails/{email_addr}{currTime}", 'w+') as f:
        f.write(f"To:{receiver}\nSubject:{subject}\nBody:{body}\nTimestamp:{currTime}")
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
    folder_path = './sentMails'
    start_with = email_addr
    sent = []

    for file in os.listdir(folder_path):
        if file.startswith(start_with):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r') as f:
                sent.append(f.read())


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

    con = input("\nDo you want to delete your sent mails.\nThey are not stored anywhere, if you don't save , you wont be able to see mails you have sent again!\nYes: y, No: n\n")

    if con == "y":
        folder_path = "./sentMails"
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
    
    
    
    



while not isSignedIn:
    action = input("~~~~~~~~~~~~ Welcome to End to End Encrypted Https Mail System ~~~~~~~~~~~~\n1-Sign In\n2-Sign Up\n3-Exit\n")
    while action!="1" and action!="2" and action!="3":
        action = input("Invalid operation, try again!\n1-Sign In\n2-Sign Up\n3-Exit")
    
    if action=="1":
        print("\n~~ SIGN IN ~~ ")
        email = input("Please enter your email: ")
        password = input("Please enter your password: ")
        token = signin(email, password)
        while type(token) != dict:
            print(token)
            print("Try again")
            email = input("Please enter your email: ")
            password = input("Please enter your password: ")
            token = signin(email, password)
        isSignedIn = True
    elif action=="2":
        print("\n~~ SIGN UP ~~ ")
        email = input("Please enter new email address (must be like username@hypersecure.com) : ")
        pattern = r'^.+@hypersecure\.com$'
        while not re.match(pattern, email):
            email = input("Please enter your email (must be like username@hypersecure.com) : ")
        password = input("Please enter password: ")
        password_again = input("Please enter password again: ")
        token = signup(email, password, password_again)
        while type(token) != dict:
            print(token)
            print("Try again")
            email = input("Please enter your email: ")
            password = input("Please enter your password: ")
            password_again = input("Please enter password again: ")
            token = signup(email, password, password_again)
        isSignedIn = True
    elif action=="3":
        isSignedIn = exit()

print("\n~~ Succesfully authorized! ~~\n")

while isSignedIn:
    action = input("~~~~~ Please select an operation: ~~~~~\n1-Send Mail\n2-See mails\n3-Logout\n")
    while action!="1" and action!="2" and action!="3" and action!="4":
        action = input("Invalid operation, try again!\n1-Send Mail\n2-See mails\n3-Logout\n")
    
    if action=="1":
        print("\n~~ COMPOSE A NEW MAIL ~~")
        receiver = input("Receiver: ")
        subject = input("Subject: ")
        body = input("Body: ")
        response = sendMail(receiver, subject, body, token)
        print(response)
    elif action=="2":
        print("\n~~ MAILBOX ~~\n")
        response = mailbox(token)
        counter = 1
        for mail in response:
            print("`````````````````````````````````````````````````")
            print(counter,end="-\n")
            print(f"From: {mail['from']}")
            print(f"Subject: {mail['subject']}")
            print(f"Body: {mail['body']}")
            print(f"Sent at: {mail['sending_date']}")
            print("`````````````````````````````````````````````````")
            counter += 1

    # elif action=="3":
    #     print("\n~~ SENT MAILS ~~\n")
    #     response = sentMails()
    #     counter = 1
    #     for mail in response:
    #         print("`````````````````````````````````````````````````")
    #         print(counter,end="-\n")
    #         print(f"From: {mail['from']}")
    #         print(f"Subject: {mail['subject']}")
    #         print(f"Body: {mail['body']}")
    #         print(f"Sent at: {mail['sending_date']}")
    #         print("`````````````````````````````````````````````````")
    #         counter += 1
    
    elif action=="3":
        print("\nLOGGING OUT...\n")
        logout()
        isSignedIn= False
        token = ""
        print("\nLOGGED OUT...\n")