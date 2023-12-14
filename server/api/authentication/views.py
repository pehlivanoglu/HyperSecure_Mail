from django.http import JsonResponse
from firebase_admin import auth
from django.views.decorators.csrf import csrf_exempt
import pyrebase


firebaseConfig = {

  "apiKey": "AIzaSyAtKobThYX08vakl_QcuzsjOCctkx_EH54",
  "authDomain": "mail-enc.firebaseapp.com",
  "projectId": "mail-enc",
  "storageBucket": "mail-enc.appspot.com",
  "messagingSenderId": "762435065526",
  "appId": "1:762435065526:web:1cd23a8652e5e94dbbb817",
  "measurementId": "G-N29T2S3M10",
  "databaseURL": "https://mail-enc-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:            
            user = auth.create_user_with_email_and_password(email, password)
            return JsonResponse({"status": "success", "uid": user["idToken"]})
        except Exception as e:
            return JsonResponse({"status": "failed", "error": str(e)})
    else:
        return JsonResponse({"status": "failed", "error": "Invalid request"})

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            return JsonResponse({"status": "success", "uid": user["idToken"]})
        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'args') and len(e.args) > 1:
                error_message = e.args[1]
            return JsonResponse({"status": "failed", "error": error_message})
    else:
        return JsonResponse({"status": "failed", "error": "Invalid request"})
