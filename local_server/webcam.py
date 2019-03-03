import cv2
import base64
import requests

from fbchat import log, Client
from fbchat.models import *
from secrets import *

client = Client(email, pw)

video = cv2.VideoCapture(0)

while 1:
	ret,frame = video.read()
	cv2.imshow('my webcam', frame)
	r = requests.get('http://localhost:3000/camstat')
	print "alright"
	if(r.json()['cam']):
		print "yeet"
		cv2.imwrite('image.png', frame)
		r = requests.post('https://math-alexa.appspot.com/image', json={ 'image': "data:image/jpg;base64," + base64.b64encode(open('image.png', "rb").read()).decode() })
		print r.text
		f = requests.post('http://localhost:3000/resp', json={ 'resp': r.text })
	
	r = requests.get('http://localhost:3000/camstatf')
	if(r.json()['cam']):
		print "yeet2"
		cv2.imwrite('image.png', frame)
		f = requests.get('http://localhost:3000/thread')
		client.sendLocalFiles('image.png', thread_id=f['thread'], thread_type=ThreadType['USER'])
	
	if cv2.waitKey(1) == 27: 
		break  # esc to quit
cv2.destroyAllWindows()