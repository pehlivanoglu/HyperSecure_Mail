from django.shortcuts import render
from django.http import HttpResponse

def get_key(request):
    return HttpResponse("Your key has been sent", content_type="text/plain")
