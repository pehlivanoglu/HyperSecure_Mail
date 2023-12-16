import requests

class UserAuthClient:
    def __init__(self):
        self.base_url = "http://localhost:3000"

    def signup(self, email, password):
        url = f"{self.base_url}/signup"
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        return response.json()

    def signin(self, email, password):
        url = f"{self.base_url}/signin"
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        return response.json()