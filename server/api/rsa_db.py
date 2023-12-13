import firebase_admin
from firebase_admin import credentials, firestore

class rsa_db_operations:
    def __init__(self):
        cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "mail-enc",
  "private_key_id": "273fe1464dd590197c75b4e12bc07b3afa5731c0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDaRTDYQnRMRxbA\n+CJaqoKAeHBc9zfv/oCSJKF2P6OAvS10ncJdv/kWNFV4o3q7Z55wFLJahHlUHt7t\nhsvGZ+a3+Qu1v1CsCrloz21zUPvm6kB+gvSqIPUI4AxyxRhA6m8AB7x1my/TPFTN\ncJygUrGwwIfTElXT3Y96FbwaIrTyRS9ys5PAlnuEGcD4zDurPcnE3TNpZuE/SE5T\nC4PRIulwyKLDXYgGFCSm5tbYYE7WmidOxwrVOJZ0iOrXKWs165m8AbAU5VBrQqsp\ndHDJeYjIhDOuBVijldAJWxoqrPjdkUuwWTeoqcHWoG9N+9BrdqSO/ZvfIhimr/YB\n3C6edddxAgMBAAECggEADhZgzdcS1ijRF/j2j/8o921j5H7Tk5VLq2MFhXIbtZTq\n000qp3iwSmsWnc0rVYodXeLav2CFINVHPRxcmDx01dM98BKI0eR1TVr0l6NBRt4/\n9bUHtoKfCLNxNOfHUMqbXxdLZhRzNJZ/FgKv0TcqdHEmCGJKu3xgJMM0sJkkhZhW\nphCaNdrYbCQJvYgGqM0TrX+vDrbFh4Uh5UBuFj/s6XNu9ClsP8ygtDaq5MpQ0PCd\nadqKYfGKfZj3rt33idX10C95+qD20VPdSwzMCtnl5+t+k1Qx6EeiY1gFSz5dvSgE\n9OkRiH/kOyQOAewhLMxmUiiOgcJ6tVWFmiCUZrHSOQKBgQD5cu8kTLCTMjmW51Jj\nj7T/CexfjmysdXvv47cYxfckfpFxeQgiUk2lra9q2sjLLTWf24/nfgqvchIBZwgD\ncopwC6vhPeolY8/l9WQm17ETiCZFjMyumtvoXT9dSUqnjAGGXm70VXdqc6GkpTsm\nXHfbLCFp/JYX5ijOnZaZIYGr7QKBgQDgAKPJePAwi03EhHZu63xBRN6oRnnDRVMy\nqfn8tdqMZ8zKKhUjS68k6mLcQyjsVwvC9zpPry8BgAAwrEK1YAMFbVG7oKpncXFC\nkh7Er2dQX75nPvY8j39EyZacO5KyQ6A0tK0ZLVL/2/E3LWjZsbIBtXsRAx5wYxE6\nzN+5DwgRFQKBgF92zfCNbPIYQZPv2UcDA1ireoujXRGvMIxBEJxpfsi3q3/KuwMv\njkm+q6hwLHIdTi1sgKkuQnacaCmjPZzcJAD3ZoMgB9DhXvn5rKd02m7IJyVs2hRk\nbY6CyTIxT2HJoffDgiD96GKT+COjnHx03OXDANKn+OUSj0Fra+wUt6SNAoGAEYYb\nShyq9bFAMTqHpV/IxbZkkNeKmQsoWhNQGkQDx+4q6Dnok21NU17+wuqCHhMlOWhr\n6GX1EHH6EdS4F0ZeliMaPMpx6kvGp4WU4KA0PeZvl9YmH1C+jRwUKz7B2C5QLy9f\nR1PzZU7IjR+BT16GZXnUGd2bmQE3DNmQOwMBB40CgYAgfAa2a5V0oQIXXCOymmL3\nuEZqITnhk03wi4PLMEUJtUpzCzSX3zhijxO53nvpeUufMnf7tivVvY+KT5OPP9u0\nH/C6uWTUGc6QqRD21u64kPK54p8bRaiz6n7ZC9pZFe1zC/HKRi+6u+y1vJxN+FZY\nGaJWHxtDZwvm9uPJniKOsg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-1sffa@mail-enc.iam.gserviceaccount.com",
  "client_id": "115682718021327074573",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-1sffa%40mail-enc.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
        try:
            firebase_admin.initialize_app(cred)
        except Exception:
            print("cred")
        self.db = firestore.client()

    def add(self, mail_address, public_key, start_date, end_date):
        doc_ref = self.db.collection(u'public_keys').document(public_key)
        doc_ref.set({
            u'mail_address': mail_address,
            u'public_key': public_key,
            u'start_date': start_date,
            u'end_date': end_date
        })

    def read(self, mail_address):
        users_ref = self.db.collection(u'public_keys')
        docs = users_ref.stream()

        for doc in docs:
            if doc.to_dict()["mail_address"] == mail_address:
                return doc.to_dict()["public_key"]

    def delete(self, public_key):
        self.db.collection(u'public_keys').document(public_key).delete()

