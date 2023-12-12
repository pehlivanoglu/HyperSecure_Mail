import firebase_admin
from firebase_admin import credentials, firestore

class firebase_connection:
    def __init__(self):
        cred = credentials.Certificate('mail-enc-firebase-adminsdk-1sffa-d3175f0fa2.json')
        firebase_admin.initialize_app(cred)

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
            print(doc.to_dict())

    def delete(self, public_key):
        self.db.collection(u'public_keys').document(public_key).delete()



