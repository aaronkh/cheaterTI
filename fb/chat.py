from fbchat import log, Client
from fbchat.models import *
from time import sleep
from secrets import *

import os
import json
import emoji
import requests

tID = None 
tThread = None

# Subclass fbchat.Client and override required methods
class EchoBot(Client):
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(thread_id, message_object.uid)
		self.markAsRead(thread_id)

		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
		print message_object
		d = {
			"msg": emoji.demojize(message_object.text),
			"id": thread_id,
			"type": thread_type.name,
			"name": client.fetchUserInfo(author_id)[author_id].first_name
		}

		requests.post('http://localhost:3000/thread', json={ 'thread': thread_id })

		m = None
		if(os.stat("messages.json").st_size == 0): m = []
		else:
			with open("messages.json",'r') as f:
				m = f.read()
				m = json.loads(m)
				print m
		m.append(d)
		with open("messages.json", 'w+') as f:
			f.write(json.dumps(m))
		# If you're not the author, echo
		# if author_id != self.uid:
		# 	threadId = thread_id


client = EchoBot(email, pw)
client.listen()