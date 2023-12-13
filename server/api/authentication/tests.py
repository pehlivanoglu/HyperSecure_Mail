import requests

# URL of the Django signin endpoint
url = 'http://localhost:8000/authentication/signin/'  # Replace with your actual URL

# Data to be sent in the POST request
data = {
    'email': 'test@test.com',
    'password': '123456'
}

# Sending the POST request
response = requests.post(url, data=data)

# Printing the response
print('Status Code:', response.status_code)
print('Response Body:', response.text)
