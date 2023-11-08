#!/usr/bin/python
"""
We are using a small REST server to control our robot.
"""
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
from multiprocessing import Process, Queue

from robot.Control import *

_debug = False


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on_error_default
def default_error_handler(e):
    #print("======================= ERROR")
    #print(request.event["message"])
    #print(request.event["args"])
    pass


@socketio.on('control', namespace='/control')
def control(message):
    data = message["data"]
    if "left" in data.keys():
        x = data["left"][0]
        y = data["left"][1]
        if _debug: print ("[Server] Left: ",x,",",y)
        control.q.put(("left",x,y))
    elif "right" in data.keys():
        x = data["right"][0]
        y = data["right"][1]
        if _debug: print ("[Server] Right: ",x,",",y)
        control.q.put(("right",x,y))
    elif "A" in data.keys():
        if _debug: print ("[Server] A")
    elif "B" in data.keys():
        if _debug: print ("[Server] B")

if __name__ == "__main__":
    

    control = Control(Queue(), comPort="COM100", baudRate="9600", verbose=False)
    control.start()
    
    socketio.run(app, host="0.0.0.0",port=5001, debug=True, use_reloader=False)
