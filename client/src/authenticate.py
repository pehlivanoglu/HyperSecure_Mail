import requests


def signup(email, password):

    data = {
        'email': email,
        'password': password
    }
    
    url = 'http://localhost:8000/authentication/signup/'

    response = requests.post(url, data=data)

    env_file_path = '/home/pehlivanoglu/Desktop/mail_enc/client/Key-Pairs/.env'

    if response.json()["status"] != "failed":
        with open(env_file_path, 'w') as file:
            file.write(f'MYAPP_TOKEN={response.json()["uid"]}\n')
    else:
        print("email in use!")

def signin(email, password):
    data = {
        'email': email,
        'password': password
    }
    
    url = 'http://localhost:8000/authentication/signin/'

    response = requests.post(url, data=data)  
    
    env_file_path = '/home/pehlivanoglu/Desktop/mail_enc/client/Key-Pairs/.env'
    
    if response.json()["status"] != "failed":
        with open(env_file_path, 'w') as file:
            file.write(f'MYAPP_TOKEN={response.json()["uid"]}\n')
    else:
        print("wrong email or password")

signin("testa@test.com", "123456")