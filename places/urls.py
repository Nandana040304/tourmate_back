from django.urls import path
from .views import nearby_places

urlpatterns = [
    path('nearby/', nearby_places),
]