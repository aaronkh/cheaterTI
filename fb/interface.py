from fbchat import log, Client
from fbchat.models import *
from time import sleep
from secrets import *

import serial
import json

ser = serial.Serial('/dev/cu.usbmodem141301', 9600, timeout=1)
sleep(1)

client = Client(email, pw)

count = 0

while True:
	line = ser.readline()
	if line:
		message = Message(text=line)
		try:
			m = None
			with open("messages.json", 'r') as f:
				m = json.loads(f.read())
			m = m[len(m)-1]
			client.send(message, thread_id=int(m["id"]), thread_type=ThreadType[m["type"]])
		except Exception as e:
			pass

	with open("messages.json", "r") as f:
		try:
			ms = json.loads(f.read())
			for m in ms[count:]:
				print m["msg"]
				print count
				count+=1
				ser.write((m["msg"]+"\n").encode())
		except Exception as e:
			print e