from django.urls import path
from app.views import *

urlpatterns = [
    path("", home, name="home"),
    path("contact", contact, name="contact"),
    path("subscribe", subscribe, name="subscribe"),
    path("history", history, name="history"),
]
