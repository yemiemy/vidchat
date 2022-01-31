from django.http import JsonResponse
from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.conf import settings
import random
import time
import json

from base.utils import room_generator
from .models import Room, RoomMember

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def delete_outdated_rooms():
    rooms = Room.objects.all()
    for room in rooms:
        room.deletes_in_seconds()

def create_meeting(request):
    delete_outdated_rooms()

    room = room_generator()
    return JsonResponse({'room_name':room.room_name}, safe=False)

def get_token(request):
    delete_outdated_rooms()

    #Build token with uid
    channelName = request.GET.get('channel')
    try:
        channel = Room.objects.get(room_name=channelName.upper())
    except:
        return JsonResponse({
            'message':"Couldn't find the meeting you're trying to join. You can create a new meeting or confirm the meeting code."
            }, safe=False, status=404)
    uid=random.randint(1,230)
    expirationTimeInSeconds = settings.EXPIRATION_TIME_IN_SECONDS
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1 # 1 represents the host while 2 represents the guests
    token = RtcTokenBuilder.buildTokenWithUid(settings.APP_ID, settings.APP_CERTIFICATE, channel.room_name, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)

def lobby(request):
    delete_outdated_rooms()
    return render(request, 'base/lobby.html')
    
def room(request):
    delete_outdated_rooms()
    return render(request, 'base/room.html')

@csrf_exempt
def create_member(request):
    delete_outdated_rooms()

    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        username=data.get('username'),
        uid=data.get('UID'),
        room_name=data.get('room_name')
    )

    return JsonResponse({'username':data.get('username')}, safe=False)

def get_member(request):
    delete_outdated_rooms()

    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(uid=uid, room_name=room_name)
    
    return JsonResponse({'username': member.username}, safe=False)

@csrf_exempt
def delete_member(request):
    delete_outdated_rooms()
    
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        username=data.get('username'),
        uid=data.get('UID'),
        room_name=data.get('room_name')
    )
    member.delete()
    return JsonResponse({'message':'Member was deleted.'}, safe=False)