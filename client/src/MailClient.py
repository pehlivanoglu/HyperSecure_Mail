import requests

class MailClient:
    def __init__(self,auth_token):
        self.base_url = "http://localhost:3000"
        self.headers = {
            'Authorization': f'Bearer {auth_token}'        }

    def get_mails(self):
        url = f"{self.base_url}/getMails"
        response = requests.get(url, headers=self.headers)
        return response.json()