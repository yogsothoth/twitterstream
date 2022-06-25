from flask import Flask, request, jsonify, redirect, render_template
from flask_socketio import SocketIO
#import tweepy
#from tweeterstream.tweetfetcher import TweetFetcher

app = Flask(__name__)
socketio = SocketIO(app)

#fetcher = TweetFetcher()

@socketio.on('connect to stream')
def handle_connect_to_stream(json):
    print('received json: ' + str(json))

#@app.get("/tweets")
#def get_tweets():
#    fetcher.fetch()
#    return jsonify([t.data for t in fetcher.fetch()]) #.data]) #tweets.data])

@app.post("/tweets")
def add_tweet():
    if request.is_json:
        tweet = request.get_json()
        print("POST callback: ")
        print(tweet)
#        tweet["id"] = _find_next_id()
        #tweets.append(country)
        socketio.emit('new tweet', data=tweet)
        return tweet, 201
    print(request)
    return {"error": "Malformed request: invalid JSON or unknown format"}, 415

@app.get("/")
def web_root():
#    return redirect("/tweets")
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app)



    
# API KEY Lt2VzyPkVvMWDYUUTeX1DC7fT
# API KEY SECRET  SMQ6ppc3oXxgAIPAciQz1X6byfv0J46Du3Z1BOd7V4CtPGTvtJ
# BEARER TOKEN AAAAAAAAAAAAAAAAAAAAALfbdwEAAAAAD6MRJOUNcMv0KzSNmsGajRHZJPM%3DwdlHy8NJakiZUDNaXLnS9KDpTo6wSEVRgYhzpGBL7t2fYsxBaO

