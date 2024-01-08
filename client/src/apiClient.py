import requests
import base64
class UserAuthClient:
    def __init__(self):
        self.base_url = "https://34.125.137.216:443"

    def signup(self, email, password):
        url = f"{self.base_url}/signup"
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data, verify=False)
        if response.text == '{"error":"This email is in use!"}':
            return "This email is in use!"

        return response.json()

    def signin(self, email, password):
        url = f"{self.base_url}/signin"
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data, verify=False)
        return response.json()
    
    
class PublicKeyClient:
    def __init__(self, auth_token):
        self.base_url = "https://34.125.137.216:443"
        self.headers = {
            'Authorization': f'Bearer {auth_token["token"]}'
        }
        # print(auth_token["token"])


    def get_public_key(self, email):
        url = f"{self.base_url}/key"
        headers = self.headers.copy()
        headers['email'] = email
        response = requests.get(url, headers=headers,verify=False)
        return response.json()[0]["value"]

    def post_public_key(self, public_key):
        url = f"{self.base_url}/key"
        data = {
            "public_key": public_key
        }
        response = requests.post(url, headers=self.headers, json=data, verify=False)
        return response.text


class MailClient:
    def __init__(self,auth_token):
        self.base_url = "https://34.125.137.216:443"
        self.headers = {
            'Authorization': f'Bearer {auth_token["token"]}'        }

    def get_mails(self):
        url = f"{self.base_url}/getMails"
        response = requests.get(url, headers=self.headers,verify=False)
        try:
            response.json()[0]
            return response.json()
        except IndexError:
            return "Mailbox empty"
        
    def get_sent_mails(self):
        url = f"{self.base_url}/getSentMails"
        response = requests.get(url, headers=self.headers,verify=False)
        try:
            response.json()[0]
            return response.json()
        except IndexError:
            return "No sent mails"
        
    
    def send_mail(self, receiver, subject, body, sym_key):
        
        body_b64 = base64.b64encode(body).decode('utf-8')
        sym_key_b64 = base64.b64encode(sym_key).decode('utf-8')

        data = {
        "receiver": receiver,
        "subject": subject,
        "body": body_b64,
        "sym_key": sym_key_b64
        }
        url = f"{self.base_url}/sendMail"
        response = requests.post(url, json=data, headers=self.headers,verify=False)
        return response.text
    
    def send_out_mail(self, receiver, subject, body):    

        data = {
        "receiver": receiver,
        "subject": subject,
        "body": body,
        "sym_key": ""
        }
        url = f"{self.base_url}/sendOutMail"
        response = requests.post(url, json=data, headers=self.headers,verify=False)
        return response.text

