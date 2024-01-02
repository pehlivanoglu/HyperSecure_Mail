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


def signup(email, password, password_again):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        if password==password_again:
            authClient = UserAuthClient()
            token = authClient.signup(email, password)

            rsa = RSA()
            pkeyClient = PublicKeyClient(token)
            pkeyClient.post_public_key(rsa.run())
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
        #check if mail exists
        f.write(publicKeyClient.get_public_key(receiver))
    
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
    
    # os.remove("./data/mail")
    # os.remove("./otherskeys/enc_sym_key")
    # os.remove("./enc_data/mail")
    # os.remove("./otherskeys/enc_sym_key")
    
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
        mail = y.run(f"{mail['sending_time']}")
        mail = mail.decode().split("-")
        subject = mail[0]
        body = mail[1]
        mailbox.append({"from":sender,
                        "subject":subject,
                        "body":body,
                        "sending_date":time})
    
    return mailbox
    
    
    
    

isSignedIn = False
token = ""

while not isSignedIn:
    action = input("~~~~~~~~~~~~ Welcome to End to End Encrypted Https Mail System ~~~~~~~~~~~~\n1-Sign In\n2-Sign Up\n")
    while action!="1" and action!="2":
        action = input("Invalid operation, try again!\n1-Sign In\n2-Sign Up\n")
    
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
        email = input("Please enter new email address: ")
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

print("\n~~ Succesfully authorized! ~~\n")

while isSignedIn:
    action = input("~~~~~ Please select an operation: ~~~~~\n1-Send Mail\n2-See mails\n3-See sent mails\n4-Logout\n")
    while action!="1" and action!="2" and action!="3" and action!="4":
        action = input("Invalid operation, try again!\n1-Send Mail\n2-See mails\n3-See sent mails\n")
    
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
    
    elif action=="4":
        print("Logging out...",end="")
        isSignedIn= False
        token = ""