from django.urls import path
from . import views

urlpatterns = [
    path('get_key', views.get_key, name='get_public_key'),
    path('post_key', views.post_key, name='post_public_key'),
]