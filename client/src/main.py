from apiClient import UserAuthClient
from apiClient import PublicKeyClient
from apiClient import MailClient
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from encryption import RSA
from encryption import encrypt
from encryption import decrypt



authClient = UserAuthClient()
token = authClient.signin("kerem4", "pw")

mai= MailClient(token)
response = mai.send_mail("kerem4","a","body","aa")
print(response)
# postkey
# x = RSA()
# public_key = x.run()

# keyClient = PublicKeyClient(token)
# response = keyClient.post_public_key(public_key)
# # print(response)
# print(public_key)
# x.run()






# #SIGNIN
# authClient = UserAuthClient()
# token = authClient.signin("ceren", "pw")

# keyClient = PublicKeyClient(token)
# pkey = keyClient.get_public_key("ceren")

# with open("./keys/public_key.pem", "w+") as f:
#     f.write(pkey)

# y = encrypt()
# y.run()

# with open("./enc_data/mail", "rb") as f:
#     file_data = f.read()

# with open("./keys/enc_sym_key", "rb") as f:
#     sym = f.read()

# mailClient = MailClient(token)
# mailClient.send_mail("ceren","subj", file_data, token, sym)



#postkey
# x = RSA()
# public_key = x.run()

# keyClient = PublicKeyClient(token)
# response = keyClient.post_public_key(public_key)
# print(response)
# print(public_key)
# x.run()

# y = encrypt()
# y.run()
# z = decrypt()
# a = z.run()
# print(a)
# print(data, sym)
# print(y.load_public_key())
# keyClient = PublicKeyClient(token)
# response = keyClient.post_public_key(public_key)
# print(response)

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