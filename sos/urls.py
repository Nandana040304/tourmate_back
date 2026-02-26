from django.urls import path
from .views import send_sos

urlpatterns = [
    path('send-sos/', send_sos),
]