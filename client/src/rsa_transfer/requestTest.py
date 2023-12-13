import requests

# The URL of the API endpoint or resource you're requesting
url = 'http://localhost:8000/rsa_transfer/get_key'

# Custom headers you want to send
headers = {
    'receiver-mail': 'test@test.com'
}

# Send the GET request
response = requests.get(url, headers=headers, verify=False) #Do not use false value for production

# Print the response text (or do something else with it)
print(response.text)
