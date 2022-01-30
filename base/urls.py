import imp
from django.urls import path
from .views import get_token, lobby, room
urlpatterns = [
    path('', lobby),
    path('room/', room),
    path('get-token/', get_token),
]
