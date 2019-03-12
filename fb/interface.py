from fbchat import log, Client
from fbchat.models import *
from time import sleep
from secrets import *
import lyft_secrets

import serial
import json
import cv2
import requests
import base64
import urllib
import cv2

ser = serial.Serial('/dev/cu.usbmodem142401', 9600, timeout=1)
sleep(1)

# lyft api stuff
lyft_status = ""
lyft_ride_id = ""
access_token = ""
current = {"lat": 37.72671448802936, "lng":-122.48222808889392}

url = "http://192.168.137.109"

def post_with_auth(*args, **kwargs):
    return requests.post(*args, auth=(lyft_secrets.id, lyft_secrets.secret), **kwargs)

def new_access_token():
	global access_token
	r = post_with_auth('https://api.lyft.com/oauth/token', json={"grant_type": "refresh_token", "refresh_token": lyft_secrets.refresh_token})
	r_json = json.loads(r.text)
	access_token = r_json["access_token"]

def cancelLyft():	
	global access_token
	requests.post('https://api.lyft.com/v1/rides/'+lyft_ride_id+'/cancel', headers={
		"Content-Type": "application/json",
		"Authorization": "Bearer "+access_token
	})

client = Client(email, pw)

count = 0

video = cv2.VideoCapture(0)

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
			
			ser.write(('Image sent').encode())
		# elif line.startswith(':L '):
		# 	line_lower = line.lower()
		# 	line_lower = line_lower[3:]
		# 	# refresh token
		# 	new_access_token()
		# 	if lyft_status == 'ordered' and line_lower == 'cancel':
		# 		cancelLyft()
		# 		ser.write(('Cancelled Lyft #'+str(lyft_ride_id)).encode())
		# 	else:
		# 		# get google map search
		# 		place = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?", params={
		# 			"key": lyft_secrets.google_key,
		# 			"input": line_lower,
		# 			"inputtype": "textquery",
		# 			"fields": "geometry"
		# 		})
		# 		loc = json.loads(place.text)['candidates'][0]['geometry']['location']

		# 		r = requests.post('https://api.lyft.com/v1/rides', 
		# 		headers = {
		# 			"Authorization" : "Bearer "+access_token
		# 		},
		# 		json={
		# 			"ride_type": "lyft",
		# 			"origin": current,
		# 			"destination": loc
		# 		}).text

		# 		# order lyft
		# 		lyft_status = 'ordered'
		# 		lyft_ride_id = json.loads(r)["ride_id"]
		# 		ser.write(('Please wait for Lyft to '+line_lower).encode())
		elif line.startswith(':T '):
			requests.post('https://math-alexa.appspot.com/twilio', json = {
				"message": line.lower()[3:]
			})
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