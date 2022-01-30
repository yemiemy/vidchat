from django.http import JsonResponse
from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.conf import settings
import random
import time
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