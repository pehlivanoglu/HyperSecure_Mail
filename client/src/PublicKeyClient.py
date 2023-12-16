import requests

class PublicKeyClient:
    def __init__(self, auth_token):
        self.base_url = "http://localhost:3000"
        self.headers = {
            'Authorization': f'Bearer {auth_token}'
        }

    def get_public_key(self, email):
        url = f"{self.base_url}/key"
        headers = self.headers.copy()
        headers['email'] = email
        response = requests.get(url, headers=headers)
        return response.json()

    def post_public_key(self, public_key):
        url = f"{self.base_url}/key"
        headers = self.headers.copy()
        headers['public_key'] = public_key
        response = requests.post(url, headers=headers)
        return response.json()
