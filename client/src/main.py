from apiClient import UserAuthClient
from apiClient import PublicKeyClient
from apiClient import MailClient
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from encryption import RSA
from encryption import encrypt
from encryption import decrypt



#SIGNIN
authClient = UserAuthClient()
token = authClient.signin("ahmet", "pw")

dec = decrypt()
dec.run()
# sym_key, enc_data=enc.run(public_key=pkey,text_to_enc="123456789_10")
# print(enc_data)
# print(type(enc_data))
# print(str(enc_data))

# #SEND MAIL
# mailClient = MailClient(token)
# response = mailClient.send_mail(receiver="ahmet", subject="subject", body=str(enc_data), sym_key=str(sym_key), token=token)
# print(response)

#get key
# keyClient = PublicKeyClient(token)
# response = keyClient.get_public_key(email="ahmet")
# print(response)



# #SIGNUP
# authClient = UserAuthClient()
# token = authClient.signup("ceren","pw")
# print(token)

# #postkey
# x = RSA()
# public_key = x.generate_public_key()

# keyClient = PublicKeyClient(token)
# response = keyClient.post_public_key(public_key)
# print(response)




# #GET MAILS
# mailClient = MailClient(token)
# response = mailClient.get_mails()
# print(response)

# #GET SENT MAILS
# mailClient = MailClient(token)
# response = mailClient.get_sent_mails()
# print(response)