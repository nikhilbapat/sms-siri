from flask import Flask, request, redirect, url_for, send_from_directory, Response
from twilio.rest import TwilioRestClient
import twilio.twiml
import urllib2
import urllib
import json

import os


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
    
    # ytData = urllib2.urlopen('https://www.googleapis.com/youtube/v3/search?safeSearch=moderate&part=snippet&q='+urllib.quote_plus(request.values.get('Body', None))+'&maxResults=1&key=AIzaSyAXIp7RY8GSt2JctHmqSFtmM-fn71hgtwA').read()
    # data = json.loads(ytData)

    # id = data['items'][0]['id']['videoId']
    # video_url = 'https://www.youtube.com/watch?v='+data['items'][0]['id']['videoId']
    # print "youtube-dl --extract-audio --prefer-ffmpeg --audio-format mp3 --audio-quality 0 -o \"tmp/" + request.values.get('Body', None) + ".%(ext)s\" \"ytsearch:" + request.values.get('Body', None) + "\""

    os.system("youtube-dl --extract-audio --prefer-ffmpeg --audio-format mp3 --audio-quality 0 -o \"tmp/" + request.values.get('Body', None) + ".%(ext)s\" \"ytsearch:" + request.values.get('Body', None) + "\"")
    #fileName = id + '.mp3'
    # url_for('tmp', filename= id + ".mp3")
    video_name = urllib.quote(request.values.get('Body', None).encode('utf-8'))



    resp.message(str(video_name))


	 
	# Make the call
	# Make the call
    call = client.calls.create(to=fromNumber,  # Any phone number
	                           from_="+14152003540", # Must be a valid Twilio number
	                           url=hostname + '/xml/' + video_name)
    print call.sid
    return str(resp)

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
























