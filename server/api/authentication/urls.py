from django.urls import path
from . import views

urlpatterns = [
    path('verify_token', views.verify_token, name='verify_token'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
]