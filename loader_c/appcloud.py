#!/usr/bin/env python3
#TESTE UTILIZANDO O GOOGLE IOT COM FLOWDATA

import datetime
import json
import os
import ssl
import time
import paho.mqtt.client as mqtt

class Medicao:
    def __init__(self, temp, umid, temp2):
        self.temperatura = temp
        self.umidade = umid
        self.temperatura2 = temp2

class MedicaoMqtt:
    def __init__(self, temp, umid, alert, id, time):
        self.temp = temp
        self.umid = umid
        self.alert = alert
        self.id = id
        self.time = time


Broker = "estufatabaco.cloud.shiftr.io" #broker publico utilizado.
porta_broker = 1883 #porta utilizada para comunicacao com o broker MQTT
                    #utilize a porta 1883 para comunicacao com conexao nao segura
keep_alive_broker = 60 #tempo (em segundos) do keep-alive
topico_subscribe = "Topico_1"  #topico MQTT que o programa ira "ouvir" (fazer subscribe)
                                     #dica: troque o nome do topico por algo "unico", 
                                     #Dessa maneira, ninguem ira saber seu topico de
                                     #subscribe e interferir em seus testes
#Callback - conexao ao broker realizada

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
ns = 'medidores/'+getserial()
global id_ns
id_ns = getserial()
from sentry_sdk import capture_exception, capture_message, init
try:
    aa = open('/etc/loader/load/sentry.conf', 'r')
    lines = aa.readlines()
    init(
        lines[0],
        server_name=ns,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
    aa.close()
except Exception as e:
    print("erro sentry.conf")


import pyrebase

f = open('/etc/loader/load/firebase.conf', 'r')
r = f.readlines()
config = json.loads(r[0])
f.close()

firebase = pyrebase.initialize_app(config)
auth_fire = firebase.auth()

db = firebase.database()
print("--------------------f--------------------")


import socketio

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

from views import auth
from views import calc
from views import firmware

global us
global user


try:

    tempFile = open( '/etc/loader/load/cloud.conf')
    jwt_user = tempFile.read()
    tempFile.close()
    tempVFile = open( '/etc/loader/loader/version.conf')
    version_local = tempVFile.readlines()
    tempVFile.close()
    us = auth.verify_and_decode_jwt(jwt_user)
    user = auth_fire.sign_in_with_email_and_password(us['user'], us['key'])
except Exception as e:
    capture_exception(e)
    print('erro de autenticação', e)


def armazenaLog(tipo):
    try:
        global user
        global ns
        from datetime import datetime
        hora = f'{datetime.now()}'
        dt = {'hora': hora, 'log': tipo, 'version': version_local[0]}
        db.child(ns).child("log").push(dt, user['idToken']) #edita o mesmo arquivo
    except Exception as e:
        capture_exception(e)
        print('erro de autenticação', e)

armazenaLog('inicialização')

def verify_firmware():
    firmw = db.child(ns).child("firmware").get(user['idToken']) #edita o mesmo arquivo
    print('firmware22', firmw.val())
    fw = firmw.val()
    version_local = 0
    try:
        tempFile = open( '/etc/loader/loader/version.conf')
        version_local = tempFile.read()
        version_local = int(version_local)
        tempFile.close()
    except Exception as e:
        capture_exception(e)
        print(e)
    try:
        global importance
        importance = 0
        global version_web
        version_web = 0
        for t in firmw.each():
            if t.key() ==  'importance':
                importance = t.val()
            if t.key() ==  'version':
                version_web = t.val()
        print('testeeee', importance, version_web)
        capture_message('verify_firmware 131')
        if importance == 9:
            if version_web > version_local:
                armazenaLog('atualizando')
                print('executar código de atualização')
                capture_message('atualizar_firmware 134')
                firmware.atualizar_firmware()
                arquivo = open( '/etc/loader/loader/version.conf', 'w')
                arquivo.write(str(version_web))
                arquivo.close()
    except Exception as e:
        capture_message('atualizar_firmware 140')
        capture_exception(e)
        print(e)
    armazenaLog('verify_firmware')

def main():
    try:
        client = mqtt.Client(getserial())
        client.username_pw_set("estufatabaco", "GqscH64RcmvHKZW6")
        client.connect(Broker, porta_broker, keep_alive_broker)
    except Exception as e:
        capture_exception(e)

    sio = socketio.Client()
    global contador
    contador = 490
    global contador2
    contador2 = 9
    global contador3
    global contador_media
    contador_media = 3
    contador3 = 22
    global medicoes
    medicoes = []
    global filtro
    filtro = 0
    @sio.event
    def connect():
        print('connection established')
    @sio.event
    def medicao(data):
        global us
        global ns
        global contador
        global medicoes
        contador += 1
        global contador2
        contador2 += 1
        global contador_media
        contador_media += 1
        global filtro
        global user
        global contador3
        
        if contador2 > 7:
            contador2 = 0
            data['cpu'] = round(get_cpu_temp())
            try:
                #msgmqtt = {'temp': data['temperatura'], 'umid': data['umidade'], 'alert': data['alerta'], 'time': data['updated'] ,'id': id_ns }
                client.publish(id_ns+"_moni", json.dumps({'temp': data['temperatura'], 'umid': data['umidade'], 'alert': data['alerta'], 'time': data['updated'] ,'id': id_ns }))
                #print(json.dumps(msgmqtt))
            except Exception as e:
                print('erro de mqtt', e)
                capture_exception(e)

            try:
                db.child(ns).child("medicao").set(data, user['idToken']) #edita o mesmo arquivo
            except Exception as e:
                capture_exception(e)
                try:
                    user = auth_fire.sign_in_with_email_and_password(us['user'], us['key'])
                except Exception as e:
                    print('erro de autenticação', e)
                print('erro de autenticação', e)

        if contador_media > 6:
            contador_media = 0
            m = Medicao(float(data['temperatura']), float(data['umidade']), float(data['temperatura2']))
            medicoes = calc.array_medicoes(medicoes, m )
        
        if contador > 500:
            contador3 += 1
            if contador3 > 20:
                contador3 = 0
                verify_firmware()
            contador = 0
            med = calc.get_media(medicoes)
            data['temperatura'] = med.temperatura
            data['temperatura2'] = med.temperatura2
            data['umidade'] = med.umidade
            data['cpu'] = round(get_cpu_temp())
            data['filtro'] = filtro
            if filtro == 0:
                filtro = 1
            elif filtro == 1:
                filtro = 2
            else:
                filtro = 0
            try:
                print('armazenando', data)
                user = auth_fire.sign_in_with_email_and_password(us['user'], us['key'])
                db.child(ns).child("medicoes").push(data, user['idToken']) # cria novo arquivo
                try:
                    #msgmqtt = {'temp': data['temperatura'], 'umid': data['umidade'], 'alert': data['alerta'], 'time': data['updated'] ,'id': id_ns }
                    capture_message( json.dumps({'temp': data['temperatura'], 'umid': data['umidade'], 'alert': data['alerta'], 'time': data['updated'] ,'id': id_ns }))
                    client.publish(id_ns+"_moni", json.dumps({'temp': data['temperatura'], 'umid': data['umidade'], 'alert': data['alerta'], 'time': data['updated'] ,'id': id_ns }))
                except Exception as e:
                    print('erro de mqtt', e)
            except Exception as e:
                capture_exception(e)
                print('erro de autenticação', e)


    @sio.event
    def disconnect():
        print('disconnected from server')
    vr_erro = 0 #caso de erro de conexão ele tenta 10 vezes com intervalo de tempo exponencial

    while True:
        vr_erro = vr_erro+1
        try:
            sio.connect('http://0.0.0.0:35494')
            print('my sid is', sio.sid)
            break
        except Exception as e:
            capture_exception(e)
            print('erro no servidor', e)
            if vr_erro > 9:
                print('erro socket')
                break
            time.sleep(5.0*vr_erro)     
    sio.wait()  


if __name__ == '__main__':
    main()
