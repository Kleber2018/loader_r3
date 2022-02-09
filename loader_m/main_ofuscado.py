#!/usr/bin/env python3
import time
import board
import RPi.GPIO as GPIO
import threading 
import json
try:
 GPIO.setup(21,GPIO.OUT)
 GPIO.setup(6,GPIO.OUT)
 GPIO.setup(5,GPIO.OUT)
 GPIO.setup(13,GPIO.OUT)
 GPIO.setup(26,GPIO.OUT)
 GPIO.setup(12,GPIO.OUT)
 GPIO.output(26,False) 
 GPIO.output(21,False) 
 GPIO.output(5,True) 
 GPIO.output(6,False) 
 GPIO.output(13,False) 
except RuntimeError as error:
 print('Erro LED',error.args[0])
except Exception as error:
 print('erro led')
import tm1637
global g
global j
global x
try:
 g=tm1637.TM1637(23,24,4)
 g.show('inic')
except Exception as error:
 print('Erro no display',error)
try:
 j=tm1637.TM1637(14,15,5)
 j.show('inic')
except Exception as error:
 print('Erro no display',error)
try:
 x=tm1637.TM1637(17,27,1)
 x.numbers(00,00)
except Exception as error:
 print('Erro no display',error)
time.sleep(0.4)
from views import service
from views import bdnew
import busio
import sqlite3
import sys
import adafruit_sht31d
import os
import glob
from datetime import datetime,timedelta
bd='/etc/loader/load/loader_banco.db'
r='/etc/loader/load/umid_banco.db' 
C='/etc/loader/load/monitor_banco4.db' 
import socketio
N=socketio.Client()
@N.event
def connect():
 print('connection established')
@N.event
def message(data):
 print('message received with ',data)
@N.event
def disconnect():
 print('disconnected from server')
o=0 
while True:
 o=o+1
 try:
  N.connect('http://0.0.0.0:35494')
  break
 except Exception as e:
  j.show('SOKT')
  if o>9:
   print('erro socket')
   break
  print('erro no servidor',e)
  time.sleep(5.0*o)
def iniciaSensorTemp():
 try:
  print('inicia sensor de temperatura')
  k='/sys/bus/w1/devices/'
  w=glob.glob(k+'28*')[0]
  b=w+'/w1_slave'
  GPIO.setmode(GPIO.BCM)
  return b
 except RuntimeError as error:
  print('Sensor temperatura erro21',error.args[0])
  g.show('er21')
  return False
 except Exception as error:
  print('Sensor temperatura erro2',error)
  g.show('err2')
  time.sleep(5)
  return False
class ConfigFaixa:
 def __init__(e,Y,W,J,S,P,E):
  e.temp_min=Y
  e.temp_max=W
  e.umid_ajuste=J
  e.etapa=S
  e.updated=P
  e.expiration=E
class ConfigGeral:
 def __init__(e,t,J,s,D,B,S):
  e.intervalo_seconds=t
  e.umid_ajuste=J
  e.escala_temp=s
  e.alerta_desat=D 
  e.speaker=B
  e.etapa=S
global n
n=0
def Desligar(channel):
 print('deligar')
 global n
 n=1
 GPIO.output(26,True) 
 g.write([0,0,0,0])
 j.write([0,0,0,0])
 time.sleep(0.5)
 g.show('desl')
 j.show('desl')
 time.sleep(2)
 g.write([0,0,0,0])
 j.write([0,0,0,0])
 os.system("sudo shutdown -h now")
 g.write([0,0,0,0])
 j.write([0,0,0,0])
 sys.exit()
def Login_livre(channel):
 print('gpio 16')
 try:
  g.show('logi')
  j.show('T 10')
  GPIO.output(26,True) 
  y=open('/etc/loader/load/login_livre.conf','w')
  y.write(f'{datetime.now()}')
  y.close()
  import socket 
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  s.connect(('10.255.255.255',1))
  IP=s.getsockname()[0]
  print(IP)
  h=IP.split('.')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[0])
  g.show('IP 1')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[0])
  g.show('IP 1')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[1])
  g.show('IP 2')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[1])
  g.show('IP 2')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[2])
  g.show('IP 3')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[2])
  g.show('IP 3')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[3])
  g.show('IP 4')
  time.sleep(2)
  j.show('    ')
  g.show('    ')
  j.show(h[3])
  g.show('IP 4')
 except Exception as e:
  print(f"Erro Ao criar arquivo: {e}")
def PulaEtapa(channel):
 print('Pular etapa')
 try:
  a=sqlite3.connect(bd)
  print('atualizando etapa')
  f=a.cursor()
  f.execute("SELECT id_config FROM config WHERE status = 1")
  K =1
  p=f.fetchall()
  if len(p)>0:
   K=p[0][0]+1
  if K>5:
   K=1
  print(((str(K)),str(datetime.now())))
  f.execute("UPDATE config SET status = 0, updated = ? WHERE status = 1;",(str(datetime.now()),))
  f.execute("UPDATE config SET status = 1, updated = ? WHERE id_config = ?;",(str(datetime.now()),str(K)))
  a.commit()
  a.close()
 except Exception as error:
  print(f"erro ao atualizar configuração: {error}")
 try:
  if q.etapa=='Padrão':
   q.etapa='Amarelação'
   GPIO.output(21,True) 
   GPIO.output(5,False) 
   GPIO.output(6,False) 
   GPIO.output(13,False) 
  elif q.etapa=='Amarelação':
   q.etapa= 'Murchamento'
   GPIO.output(21,False) 
   GPIO.output(5,True) 
   GPIO.output(6,False) 
   GPIO.output(13,False) 
  elif q.etapa== 'Murchamento':
   q.etapa='Secagem da Lâmina'
   GPIO.output(21,False) 
   GPIO.output(5,False) 
   GPIO.output(6,True) 
   GPIO.output(13,False) 
  elif q.etapa=='Secagem da Lâmina':
   q.etapa='Secagem do Talo'
   GPIO.output(21,False) 
   GPIO.output(5,False) 
   GPIO.output(6,False) 
   GPIO.output(13,True) 
  elif q.etapa=='Secagem do Talo':
   q.etapa='Padrão'
   GPIO.output(21,False) 
   GPIO.output(5,False) 
   GPIO.output(6,False) 
   GPIO.output(13,False) 
  else:
   GPIO.output(21,True) 
   GPIO.output(5,True) 
   GPIO.output(6,True) 
   GPIO.output(13,True) 
 except Exception as e:
  verificaLedEtapa('')
  print(f"Erro Ao acender LED: {e}")
service.add_system_monitor(C)
def verificaLedEtapa(etapa_faixa):
 try:
  if etapa_faixa=='Amarelação':
   GPIO.output(21,True) 
   GPIO.output(5,False) 
   GPIO.output(6,False) 
   GPIO.output(13,False) 
  elif etapa_faixa=='Murchamento':
   GPIO.output(21,False) 
   GPIO.output(5,True) 
   GPIO.output(6,False) 
   GPIO.output(13,False) 
  elif etapa_faixa=='Secagem da Lâmina':
   GPIO.output(21,False) 
   GPIO.output(5,False) 
   GPIO.output(6,True) 
   GPIO.output(13,False) 
  elif etapa_faixa=='Secagem do Talo':
   GPIO.output(21,False) 
   GPIO.output(5,False) 
   GPIO.output(6,False) 
   GPIO.output(13,True) 
  elif etapa_faixa=='Padrão':
   GPIO.output(21,False) 
   GPIO.output(5,False) 
   GPIO.output(6,False) 
   GPIO.output(13,False) 
  else:
   GPIO.output(21,True) 
   GPIO.output(5,True) 
   GPIO.output(6,True) 
   GPIO.output(13,True) 
 except Exception as E:
  print('erro no acender led etapa',E) 
try:
 GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP)
 GPIO.add_event_detect(16,GPIO.FALLING,callback=Login_livre,bouncetime=2000)
 GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_UP)
 GPIO.add_event_detect(19,GPIO.FALLING,callback=PulaEtapa,bouncetime=2000)
except RuntimeError as error:
 print('Erro na função de desligamento e liberar login',error.args[0])
except Exception as error:
 print('Erro na função de desligamento e liberar login',error.args[0])
def iniciaSHT():
 try:
  m=busio.I2C(board.SCL,board.SDA)
  U=adafruit_sht31d.SHT31D(m)
  time.sleep(3.0)
  print("\033[1mSensor\033[0m = SHT31-D")
  print("\033[1mSerial Number\033[0m = ",U.serial_number,"\n")
  U.repeatability=adafruit_sht31d.REP_MED
  return U
 except RuntimeError as error:
  print('Sensor umidade erro26',error.args[0])
  j.show('er26')
  time.sleep(2)
  return False
 except Exception as error:
  print('Sensor umidade erro2',error)
  j.show('err2')
  return False
def main():
 global I
 try:
  b=iniciaSensorTemp()
  I=True
 except Exception:
  I=False
  g.show('er22')
 global A
 time.sleep(3)
 try:
  U=iniciaSHT()
  A=True
 except Exception as err:
  print('err25',err)
  A=False
 print(str(A))
 time.sleep(0.2)
 GPIO.output(26,False) 
 time.sleep(0.7)
 time.sleep(0.3)
 GPIO.output(26,False) 
 time.sleep(1.0)
 global q
 global u
 global H
 global X
 X=0
 try:
  u=service.getLocalConfigGeral(bd)
  q=service.getLocalConfigFaixa(bd)
  verificaLedEtapa(q.etapa)
  H=u.intervalo_seconds/2
 except Exception as e:
  print('erro 501',e)
  H=200
 global O
 O=0
 global R
 R=0
 global vr
 vr=0
 global M
 M=0
 global V
 O=0
 global d
 global z
 global F
 F=0
 global L
 try:
  L=read_temp(b)
  print("DS18B20: Temp: {:.1f} F / {:.1f} C".format(L[1],L[0],))
  V=L[0]
  R=L[1]
  if u.escala_temp=='F':
   if int(L[1])>99:
    g.show(str(str(int(L[1]))+'F'))
   else:
    g.show(str(str(int(L[1]))+'*F'))
  else:
   g.temperature(int(L[0]))
 except RuntimeError as error:
  print('Sensor temperatura erro4',error.args[0])
  g.show('err4')
  time.sleep(2)
  R=0
  V=0
 except Exception as error:
  print('Sensor temperatura erro3',error)
  g.show('err3')
  time.sleep(5)
  R=0
  V=0
 while True:
  print("Temperatura CPU: ",round(service.get_cpu_temp()),'C')
  Q=datetime.now()
  x.numbers(Q.hour,Q.minute)
  if n==1:
   g.write([0,0,0,0])
   j.write([0,0,0,0])
   break
  d=0
  z=0
  if I:
   try:
    L=read_temp(b)
    print("DS18B20: Temp: {:.1f} F / {:.1f} C".format(L[1],L[0],))
    V=round(L[0],1)
    R=round(L[1],1)
    if u.escala_temp=='F':
     if int(L[1])>99:
      g.show(str(str(int(L[1]))+'F'))
     else:
      g.show(str(str(int(L[1]))+'*F'))
    else:
     g.temperature(int(L[0]))
   except RuntimeError as error:
    print('Sensor temperatura erro5',error.args[0])
    g.show('err5')
    time.sleep(2)
    R=0
    V=0
   except Exception as error:
    print('Sensor temperatura erro6',error)
    g.show('err6')
    time.sleep(5)
    R=0
    V=0
    I=False
  if U:
   try:
    print("SHT31:    Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(round(float(U.temperature*(9/5)+32),2),U.temperature,U.relative_humidity))
    O=round(U.relative_humidity,1)
    j.show(str('U '+str(int(U.relative_humidity))))
   except RuntimeError as error:
    print('erro5',error.args[0])
    j.show('err5')
    O=0
    time.sleep(5)
   except Exception as error:
    print('erro6',error)
    j.show('err6')
    time.sleep(5)
    O=0
  if q.etapa!='Padrão':
   z=service.verificarAlerta(R,O,q,r,u)
  try:
   if H>u.intervalo_seconds:
    H=0
    if O!=0 or V!=0:
     try:
      service.add_medicao(R,O,M,z,bd)
      M=M+1
      if M>8:
       M=0
     except RuntimeError as error:
      print('erro12',error.args[0])
      time.sleep(5)
     except Exception as error:
      print('erro23',error)
      time.sleep(5)
   else:
    H=H+6
  except Exception as error:
   print('erro no vr para armazenar no bd',error)
   time.sleep(1)
  try:
   X=X+1
   if X>20:
    service.add_system_monitor(C)
    X=0
  except Exception as error:
   print('erro no vr para armazenar no bd',error)
   time.sleep(1)
  service.updt_medicao(R,O,z,bd)
  try:
   N.emit('medicao',{'temperatura':R,'umidade':O,'alerta':z,'updated':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())})
  except Exception as e:
   print('erro socket:',e)
  try:
   if vr%2==0:
    GPIO.output(26,True)
    if not I:
     try:
      b=iniciaSensorTemp()
      I=True
     except Exception:
      I=False
      g.show('er23')
    if not U:
     try:
      U=iniciaSHT()
      A=True
     except Exception:
      A=False
      j.show('er27')
   else:
    GPIO.output(26,False)
  except Exception as e:
   print('erro no  if vr % 2 == 0:',e)
  if z>0 and q.updated<str(datetime.now()-timedelta(minutes=1)):
   if F>3:
    i=0
    while(i<4):
     i=i+1
     time.sleep(1.4)
     if z==11 or z==44 or z==47:
      g.show(str('----'))
     elif z==12 or z==45 or z==48:
      g.show('-   ')
     if z==33 or z==44 or z==45:
      j.show(str('----'))
     elif z==36 or z==47 or z==48: 
      j.show(str('-   '))
     time.sleep(0.6)
     if U:
      j.show(str('U '+str(int(U.relative_humidity))))
     if u.escala_temp=='F':
      if int(L[1])>99:
       g.show(str(str(int(L[1]))+'F'))
      else:
       g.show(str(str(int(L[1]))+'*F'))
     else:
      g.temperature(int(L[0]))
   else:
    time.sleep(2)
    try:
     if vr%2==0:
      GPIO.output(26,False)
     else:
      GPIO.output(26,True)
    except Exception:
     print('erro no led status')
    time.sleep(2)
    try:
     if vr%2==0:
      GPIO.output(26,True)
     else:
      GPIO.output(26,False)
    except Exception:
     print('erro no led status')
    time.sleep(2)
   F=F+1
   u=service.getLocalConfigGeral(bd)
   q=service.getLocalConfigFaixa(bd)
   verificaLedEtapa(q.etapa)
   vr=vr+1
   if vr>5:
    vr=0
  else:
   F=0
   vr=vr+1
   if vr>5:
    vr=0
    u=service.getLocalConfigGeral(bd)
    q=service.getLocalConfigFaixa(bd)
    verificaLedEtapa(q.etapa)
   time.sleep(2)
   try:
    if vr%2==0:
     GPIO.output(26,False)
    else:
     GPIO.output(26,True)
   except Exception:
    print('erro no led status')
   time.sleep(2)
   try:
    if vr%2==0:
     GPIO.output(26,True)
    else:
     GPIO.output(26,False)
   except Exception:
    print('erro no led status')
   time.sleep(2)
def read_temp_raw(b):
 f=open(b,'r')
 v=f.readlines()
 f.close()
 return v
def read_temp(b):
 v=read_temp_raw(b)
 while v[0].strip()[-3:]!='YES':
  time.sleep(0.2)
  v=read_temp_raw(b)
 c=v[1].find('t=')
 if c!=-1:
  T=v[1][c+2:]
  gj=float(T)/1000.0
  gx=gj*9.0/5.0+32.0
  return round(gj,1),round(gx,1)
if __name__=='__main__':
 try:
  main()
  g.write([0,0,0,0])
  j.write([0,0,0,0])
  GPIO.output(26,False)
 except RuntimeError as error:
  print('erro66',error.args[0])
  print('atribuindo')
  time.sleep(5)
  GPIO.output(26,False)
 except Exception as error:
  print('erro67',error)
  GPIO.output(26,False)
  time.sleep(2)
  main()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

