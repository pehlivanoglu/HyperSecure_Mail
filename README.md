## Usage:
RSA class in rsa.ipynb file is used for creating public-private key pairs. Can be simply used as 

x = RSA()

x.run(necessary_parameters)


It will automatically create key pair in Key-Pair folder.

encrypt and decrypt classes in enc_dec.ipynb file are used for encrypting and decrypting file or a text with symmetric key. Then symmetric key will be encrypted with public key. Can be simply used as

y = encrypt() #or decrypt()

y = run(necessary_parameters)


## Issues:
<del>1- in enc_dyc_tes.ipynb file, encrypting short text files is problematic due to 16byte encyrption method. Will be solved.</del>

2-encrypting short text files is problematic due to 16byte encyrption method. Will be solved.
