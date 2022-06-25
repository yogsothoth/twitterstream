from flask import Flask, request, jsonify, redirect, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('connect to stream')
def handle_connect_to_stream(json):
    print('received json: ' + str(json))

@app.post("/tweets")
def add_tweet():
    if request.is_json:
        tweet = request.get_json()
        print("POST callback: ")
        print(tweet)
        socketio.emit('new tweet', data=tweet)
        return tweet, 201
    print(request)
    return {"error": "Malformed request: invalid JSON or unknown format"}, 415

@app.get("/")
def web_root():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app)
