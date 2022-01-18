import imp
from django.urls import path
from .views import lobby, room
urlpatterns = [
    path('', lobby),
    path('room/', room),
]
