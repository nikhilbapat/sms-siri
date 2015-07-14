from flask import Flask, request, redirect, url_for, send_from_directory, Response
from twilio.rest import TwilioRestClient
import twilio.twiml
import urllib2
import urllib
import json
import requests
import os
import pywapi
import math
# from googlemaps import GoogleMaps
import forecastio
import random
# MAPS_KEY = os.environ["MAPS_KEY"]
# print os.environ["MAPS_KEY"]




def wit(query):
    r = requests.get('https://api.wit.ai/message?v=20150713&q='+urllib.quote(query), headers={'Authorization': 'Bearer FBJW3CGWSYNHT3YNKQIRSSY4VHYT6A2E'})
    data = r.json()

    print type(data);

    # print data
    # print json.loads(data)["outcomes"]["entities"]["song"]["value"]

    return data


# song_name = nlp["outcomes"]["entities"]["song"]["value"]

hostname = 'http://3184ba4c.ngrok.io'
# os.system("ls -l")
 
app = Flask(__name__, static_url_path='')
 
# Get these credentials from http://twilio.com/user/account
account_sid = "AC164edce62c5dede2433562b414209093"
auth_token = "fb9d1620814c79140c51ccabe96f0b87"
client = TwilioRestClient(account_sid, auth_token)

# os.system("cd /Users/nikhilbapat/desktop/siri/audio")
# os.system("ls")


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
 
    fromNumber = request.values.get('From', None)

    resp = twilio.twiml.Response()
    
    smsBody = request.values.get('Body', None)


    nlp = wit(smsBody)
    # print nlp

    intent = nlp["outcomes"][0]["intent"]

    print intent


    if intent == "music":

        song_name = nlp["outcomes"][0]["entities"]["song"][0]["value"]

        os.system("youtube-dl --extract-audio --prefer-ffmpeg --audio-format mp3 --audio-quality 0 -o \"tmp/" + request.values.get('Body', None) + ".%(ext)s\" \"ytsearch:" + request.values.get('Body', None) + "\"")
        #fileName = id + '.mp3'
        # url_for('tmp', filename= id + ".mp3")
        video_name = urllib.quote(request.values.get('Body', None).encode('utf-8'))

        resp.message(str("Calling your phone now..."))    	 
    	# Make the call
    	# Make the call
        call = client.calls.create(to=fromNumber,  # Any phone number
    	                           from_="+14152003540", # Must be a valid Twilio number
    	                           url=hostname + '/xml/' + video_name)
        print call.sid
        return str(resp)

    elif intent == "weather":
        

        api_key = "ba320c245b3a986d26037bc98c7ef795"
        

        city = nlp["outcomes"][0]["entities"]["location"][0]["value"]
        # print nlp

        geocodeData = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?q="+urllib.quote(city)+"").read()
        print geocodeData

        geoData = json.loads(geocodeData)

        kelvin = geoData["main"]["temp"]

        fahrenheit = ((kelvin - 273.15)*1.8) + 32.0

        resp.message(str("It is " + str(int(fahrenheit)) + " degrees Fahrenheit"))

        return str(resp)

    elif intent == "random_number":
  
        if nlp["outcomes"][0]["entities"] != {}:
            nmin = nlp["outcomes"][0]["entities"]["min"][0]["value"]
            nmax = nlp["outcomes"][0]["entities"]["max"][0]["value"]

            randnum = random.randint(nmin,nmax)
            resp.message(str("Your random number is " + str(randnum)))
        else:
            randnum = random.random()
            resp.message(str("Your random number is " + str(randnum)))

        

        return str(resp)

    elif intent == "directions"


@app.route('/audio/<path:song>', methods=['GET', 'POST'])
def send_song(song):
    return send_from_directory('tmp', song)
     
 
@app.route('/xml/<path:name>', methods=['GET', 'POST'])
def send_xml(name):
    # @add_response_headers({'Content-Type': 'application/xml'})


    finalxml = '<Response><Play>' + hostname + '/audio/' + urllib.quote(name.encode('utf-8')) + '.mp3' + '</Play><Redirect/></Response>'

    return Response(finalxml, mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True)
























