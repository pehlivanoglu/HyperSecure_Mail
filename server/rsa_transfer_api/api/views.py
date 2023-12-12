from django.shortcuts import render
from django.http import HttpResponse
from db.firebase_connections import firebase_connection

def get_key(request):
    try:
        print(1)
        db = firebase_connection()
        print(2)
        receiver_mail_address = request.headers.get('receiver-mail', 'did not receive')
        print(receiver_mail_address)
        public_key = db.read(receiver_mail_address)
        return HttpResponse(public_key, content_type="text/plain")
    except Exception:
        print("except")
    
