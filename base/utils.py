import string
import random

from .models import Room
def room_generator(size=9, chars=string.ascii_uppercase):
	the_name =  "".join(random.choice(chars) for x in range(size))
	try:
		Room.objects.get(room_name=the_name)
		room_generator()
	except Room.DoesNotExist:
		return Room.objects.create(room_name=the_name)