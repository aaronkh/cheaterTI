from fbchat import log, Client
from fbchat.models import *
from time import sleep
from secrets import *

import serial
import json
import cv2
import requests
import base64

ser = serial.Serial('/dev/cu.usbmodem141301', 9600, timeout=1)
sleep(1)

video = cv2.VideoCapture(0)

client = Client(email, pw)

count = 0

while True:
	ret,frame = video.read()
	line = ser.readline()
	if line.startswith(':'):
		if(line.startswith(':I')):
			# take picture and get integral
			cv2.imwrite('image.png', frame)
			r = requests.post('https://math-alexa.appspot.com/image', json={ 'image': "data:image/jpg;base64," + base64.b64encode(open('image.png', "rb").read()).decode() })
			ser.write(('Answer: ' + r.text + '\n').encode())
			
		elif(line.startswith(':C')):
			# take picture and send to fb messenger
			cv2.imwrite('image.png', frame)
			try:
				m = None
				with open("messages.json", 'r') as f:
					m = json.loads(f.read())
				m = m[len(m)-1]
				client.sendLocalFiles('image.png', thread_id=int(m['id']), thread_type=ThreadType[m['type']])
			except Exception as e:
				pass
			
		elif(line.startswith(':W')):
			pass
			# send to wolframalpha
	elif line:
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
				print m["name"]
				print count
				count+=1
				ser.write((m["name"] + ": " + m["msg"]+"\n").encode())
		except Exception as e:
			print e

video.release()