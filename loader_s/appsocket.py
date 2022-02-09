#!/usr/bin/env python3
#
# COM FLASK SOCKET
# import time
# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import time
# print('Iniciando Servidor Soccket')
#
# app = Flask(__name__)
# #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins='*')
#
# @app.route('/')
# def index():
#     print('conectado')
#
# @socketio.on('medicao')
# def medicao(data):
#     try:
#         emit('medicao', data, broadcast=True)
#     except Exception as error:
#         print('erro:', error)
#
# @socketio.on('connect')
# def test_connect():
#     print('New connect')
#
# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')
#
# if __name__ == '__main__':
#     vr = 0
#     while True:
#         vr = vr+1
#         try:
#             socketio.run(app, host='0.0.0.0', port=35494)
#         except Exception as e:
#             print("\n Execption occurs while starting the socketio server", str(e))
#         time.sleep(10*vr)
#         if vr > 9:
#             vr = 0

############################################################################
#

def getserial():
    #https://qastack.com.br/raspberrypi/2086/how-do-i-get-the-serial-number
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

global ns
ns = getserial()
from sentry_sdk import capture_exception, capture_message, init
try:
    aa = open('/etc/loader/load/sentry.conf', 'r')
    lines = aa.readlines()
    aa.close()
    init(
        lines[0],
        server_name=ns,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
except Exception as e:
    print("erro sentry.conf")




#capture_message("Hello World")
import time
import threading #https://www.tutorialspoint.com/python3/python_multithreading.htm
import eventlet
import socketio #https://python-socketio.readthedocs.io/en/latest/server.html
global sio
sio = socketio.Server(cors_allowed_origins="*")
# app = socketio.WSGIApp(sio, static_files={
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# })
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ok ', sid)
    sio.emit('my event', {'data': 'foobar'})

@sio.event
def my_message(sid, data):
    print('message ', data)
    sio.emit('my event', {'data': 'mensagem teste22'})
    sio.emit('message', {'data': 'mensagem teste44'})

@sio.event
def medicao(sid, data):
    print('Enviando mensagem ', data)
    #sio.emit('my event', {'data': 'mensagem teste'})
    sio.emit('medicao', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
        vr = 0
        while True:
            vr = vr+1
            try:
                eventlet.wsgi.server(eventlet.listen(('', 35494)), app)
            except Exception as e:
                capture_exception(e)
                #print("\n Execption occurs while starting the socketio server", str(e))
            time.sleep(5*vr)
            if vr > 20:
                vr = 0



