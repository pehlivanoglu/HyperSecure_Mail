from django.shortcuts import render
from django.http import HttpResponse
from rsa_db import rsa_db_operations

def get_key(request):
    db = rsa_db_operations()
    receiver_mail_address = request.headers.get('receiver-mail', '400 Bad Request')
    public_key = db.read(receiver_mail_address)
    if receiver_mail_address == "400 Bad Request":
        return HttpResponse(f"400 Bad Request : header name wrong", content_type="text/plain")
    if public_key == None:
        return HttpResponse(f"404 Error - Mail address not found! : {receiver_mail_address}", content_type="text/plain")
    return HttpResponse(public_key, content_type="text/plain")

def post_key(request):
    return HttpResponse("key created", content_type="text/plain")