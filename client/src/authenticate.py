import os
import requests
import bcrypt


def signin(email, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    data = {
        'email': email,
        'password': hashed_password
    }

    url = 'http://localhost:8000/authentication/signin/'
    
    response = requests.post(url, data=data)

    print(response)

    env_file_path = '/home/pehlivanoglu/Desktop/mail_enc/client/Key-Pairs/.env'

    with open(env_file_path, 'w') as file:
        file.write(f'MYAPP_ISSIGNEDIN={flag}\n')

signin("test@test.com", "123456")