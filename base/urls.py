import imp
from django.urls import path
from .views import create_member, delete_member, get_member, get_token, lobby, room
urlpatterns = [
    path('', lobby),
    path('room/', room),
    path('get-token/', get_token),
    path('create-member/', create_member),
    path('get-member/', get_member),
    path('delete-member/', delete_member),
]
