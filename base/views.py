from django.http import JsonResponse
from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.conf import settings
import random
import time
import json
from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def get_token(request):
    #Build token with uid
    channelName = request.GET.get('channel')
    uid=random.randint(1,230)
    expirationTimeInSeconds = 3600*24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1 # 1 represents the host while 2 represents the guests
    token = RtcTokenBuilder.buildTokenWithUid(settings.APP_ID, settings.APP_CERTIFICATE, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')
    
def room(request):
    return render(request, 'base/room.html')

@csrf_exempt
def create_member(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        username=data.get('username'),
        uid=data.get('UID'),
        room_name=data.get('room_name')
    )

    return JsonResponse({'username':data.get('username')}, safe=False)

def get_member(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(uid=uid, room_name=room_name)
    
    return JsonResponse({'username': member.username}, safe=False)

@csrf_exempt
def delete_member(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        username=data.get('username'),
        uid=data.get('UID'),
        room_name=data.get('room_name')
    )
    member.delete()
    return JsonResponse({'message':'Member was deleted.'}, safe=False)