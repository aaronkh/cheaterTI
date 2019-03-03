import lyft_secrets
# import webbrowser, os
import requests, json, urllib, webbrowser

params = "san jose state"
current = {"lat": 37.72671448802936, "lng":-122.48222808889392}

# url = 'https://api.lyft.com/oauth/authorize?client_id='+lyft_secrets.id+'&scope=public%20profile%20rides.read%20rides.request%20offline&state=authing&response_type=code'
# webbrowser.open(url)


def post_with_auth(*args, **kwargs):
    return requests.post(*args, auth=(lyft_secrets.id, lyft_secrets.secret), **kwargs)

def get_with_auth(*args, **kwargs):
    return requests.get(*args, auth=(lyft_secrets.id, lyft_secrets.secret), **kwargs)
 

def new_access_token():
    r = post_with_auth('https://api.lyft.com/oauth/token', json={"grant_type": "refresh_token", "refresh_token": lyft_secrets.refresh_token})
    r_json = json.loads(r.text)
    return r_json["access_token"]
    
# print post_with_auth('https://api.lyft.com/oauth/token', json = {
#     "grant_type": "authorization_code",
#     "code": '1XLXqb4LotdABI41'
# }).text
access_token = new_access_token()

place = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?", params={
    "key": lyft_secrets.google_key,
    "input": params,
    "inputtype": "textquery",
    "fields": "geometry"
})
loc = json.loads(place.text)['candidates'][0]['geometry']['location']

r = requests.post('https://api.lyft.com/v1/rides', 
headers = {
    "Authorization" : "Bearer "+access_token
},
json={
    "ride_type": "lyft",
    "origin": current,
    "destination": loc
}).text

ride_id = json.loads(r)["ride_id"]

requests.post('https://api.lyft.com/v1/rides/'+ride_id+'/cancel', headers={
    "Content-Type": "application/json",
    "Authorization": "Bearer "+access_token
})


