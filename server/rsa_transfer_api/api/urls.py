from django.urls import path
from . import views

urlpatterns = [
    path('getkey/', views.get_key, name='get_public_key'),
]
