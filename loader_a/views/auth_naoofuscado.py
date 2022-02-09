





import hmac
import hashlib
import base64
import json
import datetime
import sqlite3
#ofuscado
bd = '/etc/loader/loader/conf_banco.db'
u='52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54' 
def create_jwt(n):
 try:
  G=open('/etc/loader/loader/key.conf','r')
  u=G.readline()
  G.close()
 except:
  print('erro ao acessar key.conf - create_jwt')
 n=json.dumps(n).encode()
 f=json.dumps({'typ':'JWT','alg':'HS256'}).encode()
 b64_header=base64.urlsafe_b64encode(f).decode()
 b64_payload=base64.urlsafe_b64encode(n).decode()
 signature=hmac.new(key=u.encode(),msg=f'{b64_header}.{b64_payload}'.encode(),digestmod=hashlib.sha256).digest()
 I=f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'
 return I
def verify_and_decode_jwt(I):
 try:
  G=open('/etc/loader/loader/key.conf','r')
  u=G.readline()
  G.close()
 except:
  print('erro ao acessar key.conf - verify jwt')
 try:
  b64_header, b64_payload,q=I.split('.')
  p=base64.urlsafe_b64encode(hmac.new(key=u.encode(),msg=f'{b64_header}.{b64_payload}'.encode(),digestmod=hashlib.sha256).digest()).decode()
  n=json.loads(base64.urlsafe_b64decode(b64_payload))
  s=datetime.datetime.now().timestamp()
  if n.get('exp')and n['exp']<s:
   raise Exception('Token expirado')
  if p!=q:
   raise Exception('Assinatura invalida')
  return n
 except:
  return{'erro':'Token invalido'}
def verify_key_mac():
 try:
  from uuid import getnode as get_mac
  G=open('/etc/loader/load/load.conf','r')
  k=G.readline()
  G.close()
  decoded=verify_and_decode_jwt(k)
  if f"{get_mac()}"==f"{decoded['cod']}":
   return 1
 except Exception as error:
  print('erro ativação key',error)
  return 0
def verify_key():
 try:
  G=open('/etc/loader/load/load.conf','r')
  k=G.readline()
  G.close()
  decoded=verify_and_decode_jwt(k)
  print(f"código: {decoded['cod']}")
  if f"{getserial()}"==f"{decoded['cod']}":
   return 1
  else:
   return 0
 except Exception as error:
  print('erro ativação key',error)
  return 0
def autentication_api(C,B):
 try:
  P=sqlite3.connect(bd)
  g=P.cursor()
  g.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario " "WHERE login = ? and senha = ?",(C,B))
  m=g.fetchall()
  g.close()
  P.close()
  if len(m)==1:
   print('antes',m[0][0])
   print(m[0][0])
   n={'login':C,'senha':B}
   K=create_jwt(n)
   return{'token':K}
  else:
   return{'erro':'Usuario ou senha invalido!'}
 except Exception as e:
  print(f"Erro bd: {e}")
  return{'erro':f"Erro BD: {e}",'description':'Erro no banco de dados, reinicie a central!'}
def verify_autentication_api(k):
 Q=verify_and_decode_jwt(k)
 if 'senha' in Q:
  if 'login' in Q:
   print('existe')
  else:
   return{'erro':'Usuario invalido!'}
 else:
  return{'erro':'Senha invalida!'}
 try:
  P=sqlite3.connect(bd)
  g=P.cursor()
  g.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario " "WHERE login = ? and senha = ?",(Q['login'],Q['senha']))
  m=g.fetchall()
  g.close()
  P.close()
  if len(m)==1:
   return{'autenticado':'ok'}
  else:
   return{'erro':'Usuario ou senha invalido!'}
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return{'erro':f"Erro BD: {e}",'description':'Erro no banco de dados, reinicie a central!'}
def getserial():
 R="0000000000000000"
 try:
  f=open('/proc/cpuinfo','r')
  for e in f:
   if e[0:6]=='Serial':
    R=e[10:26]
  f.close()
 except:
  R="ERROR000000000"
 return R
# Created by pyminifier (https://github.com/liftoff/pyminifier)

