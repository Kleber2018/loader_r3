import time
time.sleep(1.0)
from flask import Flask,render_template,request,redirect,session,flash,url_for,jsonify
import sqlite3
import sys
from flask_cors import CORS
import socket 
from datetime import datetime,timedelta
import json
j=Flask(__name__)
CORS(j)
bd='/etc/loader/load/loader_banco.db'
U='3.1.0'
j.secret_key='flask'
from views import auth
class Usuario:
 def __init__(o,jU,s,G,c,f,u):
  o.login=jU
  o.senha=u
  o.nome=s
  o.Telefone=G
  o.email=c
  o.privilegios=f
class Medicao:
 def __init__(o,x,m,M,C,I):
  o.id_medicao=x
  o.temperatura=m
  o.umidade=M
  o.alerta=C
  o.data=I
class Config:
 def __init__(o,L,v,Y,n,J,q,X,r,A,V):
  o.etapa=L
  o.intervalo_seconds=v
  o.temp_min=Y
  o.temp_max=n
  o.umid_ajuste=J
  o.escala_temp=q
  o.alerta_desat=X
  o.speaker=r
  o.updated=A
  o.obs=V
@j.route('/updatedatasistema',methods=['GET',])
def updatedatasistema():
 try:
  h=request.args['datetime']
  H=auth.verify_autentication_api(request.args['token'])
  if 'autenticado' in H:
   print('autenticado')
  else:
   return jsonify({'erro':'Necessario estar logado'})
 except:
  return jsonify({'erro':'Necessario estar logado'})
 import os
 from datetime import datetime
 try:
  print(f"sudo date -s  '{datetime_request}'")
  c=os.popen(f"sudo date -s '{datetime_request}'")
  c.read()
  c.close()
  F=datetime.now()
 except Exception:
  return jsonify({'datetime':f"{now}"})
 return jsonify({'datetime':f"{now}"}) 
@j.route('/scan',methods=['GET','POST'])
def scan():
 from datetime import datetime
 try:
  z=auth.verify_key()
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  s.connect(('10.255.255.255',1))
  IP=s.getsockname()[0]
  s.close()
  F=datetime.now()
  return jsonify({'retorno':f"{IP}",'datetime':f"{now}",'nome':'Estufa 1','a':f"{active}",'version':f"{version}"}) 
 except Exception as e:
  return jsonify({'erro':f"{e}"}) 
@j.route('/sis',methods=['POST'])
def sis():
 from datetime import datetime
 try:
  ns=auth.getserial()
  F=datetime.now()
  return jsonify({'retorno':f"{ns}",'datetime':f"{now}",'nome':'Estufa 1'}) 
 except Exception as e:
  print(f"Erro SIS: {e}")
  return jsonify({'retorno':f"erro",'nome':'Estufa 1'}) 
@j.route('/loader',methods=['POST'])
def loader():
 try:
  print(request.json['cod'])
  print(request.json['key'])
  if 'cod' in request.json:
   if 'key' in request.json:
    e={'cod':request.json['cod'],'key':request.json['key']}
    i=auth.create_jwt(e)
    Q=open('/etc/loader/load/load.conf','w')
    Q.write(i)
    Q.close()
    return jsonify({'token':f"{jwt_created}"})
   else:
    return jsonify({'erro':'Key invalido!'})
  else:
   return jsonify({'erro':'Cod invalida!'})
 except Exception as e:
  print(f"Erro Loader: {e}")
  return jsonify({'erro':f"Erro Loader: {e}"})
@j.route('/',methods=['GET','OPTIONS'])
def index():
 g=1
 medicoes=[]
 d=[]
 D=[]
 K=[]
 alertas=[]
 a=auth.verify_key()
 b=getLocalConfigGeral()
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("SELECT id_medicao, temperatura, umidade, strftime('(%d) %H:%M',created) FROM medicoes" " WHERE oculto = '0' or oculto = '2' ORDER BY id_medicao DESC LIMIT 50")
  for x,m,M,I in k:
   a=round(m,1)
   if b.escala_temp=='C':
    a=round(((m-32)*5/9),1)
   medicoes.append({'id':x,'temperatura':float(a),'umidade':float(M),'data':f"{data}"})
   d.insert(0,float(a))
   D.insert(0,float(M))
   K.insert(0,f"{data}")
  k.execute("SELECT id_medicao, temperatura, umidade, alerta, strftime('(%d) %H:%M',created) FROM medicoes" " WHERE alerta = 1 and oculto < 9 ORDER BY created DESC LIMIT 25")
  for x,m,M,C,created in k:
   w=''
   if C==1:
    w==f"Temperatura: {temperatura} está fora"
   elif C==3:
    w==f"Umidade: {umidade} está fora"
   elif C==4:
    w==f"Umidade: {umidade} e Temperatura: {temperatura} estão fora"
   alertas.append({'id':x,'temperatura':float(m),'umidade':float(M),'descricao':w,'created':f"{created}"})
  k.execute("SELECT temperatura, umidade, alerta, strftime('(%d) %H:%M',updated) " "FROM medicao WHERE id_medicao = 1")
  S=k.fetchall()
  medicao={'temp':0,'umid':0,'alert':0,'upd':'erro'}
  if len(S)>0:
   tm=round(S[0][0],1)
   if b.escala_temp=='C':
    tm=round(((round(S[0][0],1)-32)*5/9),1)
   medicao={'temp':tm,'umid':round(S[0][1],1),'alert':S[0][2],'upd':S[0][3],'escala':b.escala_temp}
  k.close()
  O.close()
  if 'usuario_logado' not in jc or jc['usuario_logado']==None:
   g=0
 except Exception as e:
  print(f"Erro SQLite: {e}")
 return E('lista.html',titulo='Medições',medicoes=medicoes,temperaturas=d,umidades=D,dias=K,alertas=alertas,a=a,logado=g,medicao=medicao)
def verificaAlerta(C):
 R={'tem_alert':'','temp_umid':''}
 if C==11 or C==44 or C==47:
  R.tem_alert='alta'
 elif C==12 or C==45 or C==48:
  R.tem_alert='baixo'
 else:
  R.tem_alert=''
 if C==33 or C==44 or C==45:
  R.temp_umid='alta'
 elif C==36 or C==47 or C==48:
  R.temp_umid='baixo'
 else:
  R.temp_umid=''
@j.route('/medicao',methods=['GET'])
def medicao():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("SELECT temperatura, umidade, alerta, updated " "FROM medicao WHERE id_medicao = 1")
  T=[]
  for m,M,C,A in k:
   T.append({'temperatura':float(m),'umidade':float(M),'alerta':C,'updated':f"{updated}"})
  k.close()
  O.close()
  return jsonify(T)
 except Exception as error:
  print(f"Erro Medição SQLITE: {error}")
  return jsonify({'erro':f"{error}"})
@j.route('/medicoes',methods=['GET'])
def medicoes():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  print(request.args['oculto'])
  y=request.args['oculto'].split(',')
  if len(y)!=4:
   y=[0,1,2,3]
  k.execute("SELECT id_medicao, temperatura, umidade, alerta, created FROM medicoes" " WHERE created >= ? and created <= ? and (oculto = ? or oculto = ? or oculto = ? or oculto = ?) ORDER BY id_medicao DESC LIMIT 60",(request.args['datainicial'],request.args['datafinal'],y[0],y[1],y[2],y[3]))
  T=[]
  for x,m,M,C,created in k:
   T.append({'id':x,'temperatura':float(m),'umidade':float(M),'alerta':C,'data':f"{created}"})
  k.close()
  O.close()
  return jsonify(T)
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return jsonify({'erro':f"{e}"})
@j.route('/alertas',methods=['GET'])
def alertas():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("SELECT id_medicao, temperatura, umidade, alerta, created FROM medicoes" " WHERE alerta = 1 ORDER BY id_medicao DESC LIMIT 25")
  T=[]
  for x,m,M,C,created in k:
   T.append({'id':x,'temperatura':float(m),'umidade':float(M),'alerta':C,'data':f"{created}"})
  k.close()
  O.close()
  return jsonify(T)
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return jsonify({'erro':f"{e}"})
@j.route('/alertasperiodo',methods=['GET'])
def alertasperiodo():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("SELECT id_medicao, temperatura, umidade, alerta, created FROM medicoes" " WHERE  created >= ? and created <= ? and alerta > 0 ORDER BY id_medicao DESC LIMIT 50",(request.args['datainicial'],request.args['datafinal']))
  T=[]
  for x,m,M,C,created in k:
   T.append({'id':x,'temperatura':float(m),'umidade':float(M),'alerta':C,'data':f"{created}"})
  k.close()
  O.close()
  return jsonify(T)
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return jsonify({'erro':f"{e}"})
@j.route('/apiconfig',methods=['GET'])
def apiconfig():
 try:
  B=configRetorno()
  return jsonify(B)
 except Exception as e:
  return jsonify({'erro':f"{e}"})
def configRetorno():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("SELECT etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs " "FROM config WHERE id_config = 5")
  P=[]
  for L,v,Y,n,J,q,X,r,A,V in k:
   P.append({'etapa':L,'intervalo_seconds':int(v),'temp_min':float(Y),'temp_max':float(n),'umid_ajuste':J,'escala_temp':q,'alerta_desat':X,'speaker':r,'updated':f"{updated}",'obs':V})
  k.close()
  O.close()
  return P[0]
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return{'erro':f"{e}"}
def getLocalConfigGeral():
 try:
  W=sqlite3.connect(bd)
  l=W.cursor()
  l.execute("SELECT etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs FROM config WHERE id_config = 5;")
  S=l.fetchall()
  if len(S)>0:
   W.close()
   return Config(S[0][0],int(S[0][1]),int(S[0][2]),int(S[0][3]),int(S[0][4]),S[0][5],S[0][6],S[0][7],S[0][8],S[0][9])
  else:
   l.execute("SELECT etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs FROM config WHERE id_config = 5;")
   S=l.fetchall()
   l.execute("UPDATE config SET etapa = 'Padrão' WHERE id_config = 5;")
   W.close()
   return Config(S[0][0],int(S[0][1]),int(S[0][2]),int(S[0][3]),int(S[0][4]),S[0][5],S[0][6],S[0][7],S[0][8],S[0][9])
 except Exception as e:
  print('Erro consultar BD getLocalConfigGeral',e)
  return{'erro':f"{e}"}
@j.route('/novo')
def novo():
 t=[]
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("SELECT login, nome, telefone, email, privilegios FROM usuario")
  for jU,s,G,c,f in k:
   t.append(Usuario(jU,s,G,c,f,' '))
  k.close()
  O.close()
 except Exception as e:
  print(f"Erro SQLite: {e}")
  if O:
   O.close()
 if 'usuario_logado' not in jc or jc['usuario_logado']==None:
  return jo(ju('login',proxima=ju('novo')))
 else:
  return E('novo.html',titulo='Novo Usuario',usuarios=t)
@j.route('/criar',methods=['POST',])
def criar():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("INSERT INTO Usuario(login, senha, nome, telefone, email, privilegios) VALUES (?, ?, ?, ?, ?, ?);",(request.form['login'].lower(),request.form['Senha'].lower(),request.form['Nome'],request.form['Telefone'],request.form['Email'],'adm'))
  O.commit()
  k.close()
  O.close()
  return jo(ju('index'))
 except Exception as e:
  print(f"Erro SQLite: {e}")
  if O:
   O.close()
  return jo(ju('novo'))
@j.route('/login')
def login():
 js=request.args.get('proxima')
 return E('login.html',proxima=js)
@j.route('/autenticar',methods=['POST',])
def autenticar():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  jU=request.form['login'],
  u=request.form['senha'],
  print(jU,u)
  k.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario " "WHERE login = ? and senha = ?",(jU[0].lower(),u[0].lower(),))
  jG=k.fetchall()
  k.close()
  O.close()
 except Exception as e:
  print(f"Erro SQLite: {e}")
  jx(f"Erro SQLite: {e}")
  return jo(ju('login'))
 if len(jG)==1:
  jc['usuario_logado']=jG[0][0]
  jx(jG[0][2]+' acesso permitido!')
  jf=request.form['proxima']
  return jo(jf)
 else:
  jx('Acesso negado, digite novamente!')
  return jo(ju('login'))
@j.route('/loginapi',methods=['POST',])
def loginapi():
 try:
  if 'senha' in request.json:
   if 'user' in request.json:
    jm=auth.autentication_api(request.json['user'],request.json['senha'])
    jM=jsonify(jm)
    if 'erro' in jM.json:
     print("verificar se existe")
     try:
      Q=open('/etc/loader/load/login_livre.conf','r')
      jC=Q.readline()
      Q.close()
      jI=datetime.fromisoformat(jC)
      jL=datetime.now()
      print(jL,jI,jL+jv(minutes=10))
      print(jL>jI,jI+jv(minutes=10)>jL)
      if jL>jI and jI+jv(minutes=10)>jL:
       try:
        O=sqlite3.connect(bd)
        k=O.cursor()
        k.execute("INSERT INTO Usuario(login, senha, nome, telefone, email, privilegios) VALUES (?, ?, 'auto', '', '', 'adm');",(request.json['user'].lower(),request.json['senha'].lower()))
        O.commit()
        k.close()
        O.close()
       except Exception as e:
        print(f"Erro SQLite: {e}")
        return jsonify({'erro':e})
       jm=auth.autentication_api(request.json['user'],request.json['senha'])
       return jsonify(jm)
      else:
       return jsonify(jm)
     except Exception as e:
      print('erro ao criar arquivo',e)
      return jsonify({'erro':e})
    else:
     return jsonify(jm)
   else:
    return jsonify({'erro':'Usuario invalido!'})
  else:
   return jsonify({'erro':'Senha invalida!'})
 except:
  return jsonify({'erro':'Erro na requisicao'})
@j.route('/logout')
def logout():
 jc['usuario_logado']=None
 jx('Usuário deslogado')
 return jo(ju('index'))
@j.route('/resetarkey',methods=['GET',])
def resetarkey():
 try:
  H=auth.verify_autentication_api(request.args['token'])
  if 'autenticado' in H:
   print('autenticado 491')
  else:
   return jsonify({'erro':'Necessario estar logado'})
 except:
  return jsonify({'erro':'Necessario estar logado'})
 try:
  Q=open('/etc/loader/loader/key.conf','w')
  Q.write(f'{datetime.now()}')
  Q.close()
  return jsonify({'retorno':'Resetado todos os acessos com sucesso'})
 except Exception as e:
  print('erro ao criar arquivo',e)
  return jsonify({'erro':e})
@j.route('/config')
def config():
 config=''
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("SELECT etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs " "FROM config WHERE id_config = 5")
  for L,v,Y,n,J,q,X,r,A,V in k:
   config=Config(L,int(v),float(Y),float(n),int(J),str(q),int(X),int(r),str(A),V)
  k.close()
  O.close()
 except Exception as e:
  jx(f"Erro SQLite: {e}")
  if O:
   O.close()
 if 'usuario_logado' not in jc or jc['usuario_logado']==None:
  return jo(ju('login',proxima=ju('novo')))
 else:
  return E('config.html',titulo='Configuração',config=config)
@j.route('/excluiruser',methods=['POST',])
def excluiruser():
 try:
  if 'usuario_logado' not in jc or jc['usuario_logado']==None:
   return jo(ju('login',proxima=ju('novo')))
  print(((f"{request.form['login']}"),))
  jx('Tem certeza que deseja excluir o usuário?')
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("DELETE FROM usuario WHERE login = ?;",((request.form['login']),))
  k.close()
  O.close()
  return jo(ju('novo'))
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return jo(ju('novo'))
@j.route('/salvarconfig',methods=['POST',])
def salvarconfig():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  jn=request.form['intervalo']
  print("intervalo",jn)
  if int(jn)<60:
   jn=60
  print((request.form['etapa'],jn,request.form['umidAjuste'],request.form['escalaTemp'],request.form['alertaDesat'],request.form['speaker'],request.form['obs']))
  k.execute("UPDATE Config SET etapa = ?, intervalo_seconds= ?, umid_ajuste = ?, escala_temp = ?, alerta_desat = ?, speaker = ?, updated = datetime('now'), obs = ? WHERE id_config = 5;",(request.form['etapa'],jn,request.form['umidAjuste'],request.form['escalaTemp'],request.form['alertaDesat'],request.form['speaker'],request.form['obs']))
  O.commit()
  k.close()
  O.close()
  return jo(ju('index'))
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return jo(ju('config'))
@j.route('/apisalvarconfig',methods=['POST',])
def apisalvarconfig():
 try:
  if 'token' in request.json:
   H=auth.verify_autentication_api(request.json['token'])
   if 'autenticado' in H:
    print('autenticado')
   else:
    return jsonify({'erro':'Necessario estar logado!'})
  else:
   return jsonify({'erro':'Necessario estar logado!'})
  if request.json['config']['intervalo_seconds']<60:
   jn=60
  else:
   jn=request.json['config']['intervalo_seconds']
  Y=request.json['config']['temp_min']
  n=request.json['config']['temp_max']
  J=request.json['config']['umid_ajuste']
  q=request.json['config']['escala_temp']
  X=0
  r=0
  id=5
  try:
   r=request.json['config']['speaker']
   X=request.json['config']['alerta_desat']
   id=request.json['config']['id']
  except:
   X=0
   r=0
   id=5
  V=request.json['config']['obs']
  L=request.json['config']['etapa']
 except Exception as e:
  print(f"Erro SQLite 585: {e}")
  return jsonify({'retorno':f"{e}"})
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("UPDATE config SET etapa = ?, intervalo_seconds= ?, temp_min = ?, temp_max = ?, umid_ajuste = ?, escala_temp = ?, alerta_desat = ?, speaker = ?, updated = datetime('now'), obs = ? WHERE id_config = ?;",(L,jn,Y,n,J,q,X,r,V,id))
  O.commit()
  k.close()
  O.close()
  print('salvo')
  return jsonify({'retorno':f"salvo"})
 except Exception as e:
  print(f"Erro SQLite: {e}")
  return jsonify({'retorno':f"{e}"})
@j.route('/silenciaralertas')
def silenciaralertas():
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("UPDATE medicoes SET alerta = 1 WHERE alerta = 2;;")
  O.commit()
  k.close()
  O.close()
  return jo(ju('index'))
 except Exception as e:
  jx(f"Erro SQLite: {e}")
  if O:
   O.close()
  return jo(ju('index'))
@j.route('/silenciaralertasapi',methods=['GET'])
def silenciaralertasapi():
 try:
  H=auth.verify_autentication_api(request.args['token'])
  if 'autenticado' in H:
   print('autenticado')
  else:
   return jsonify({'erro':'Necessario estar logado'})
 except:
  return jsonify({'erro':'´Parametros invalidos'})
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  k.execute("UPDATE medicoes SET alerta = 1 WHERE alerta = 2;")
  O.commit()
  k.close()
  O.close()
  return jsonify({'retorno':f"ok"})
 except Exception as e:
  print(f"Erro SQLite: {e}")
  if O:
   O.close()
  return jsonify({'retorno':f"{e}"})
@j.route('/apiocultarmedicoes',methods=['GET',])
def apiocultarmedicoes():
 try:
  if 'token' in request.json:
   H=auth.verify_autentication_api(request.json['token'])
   if 'autenticado' in H:
    print('autenticado')
   else:
    return jsonify({'erro':'Necessario estar logado!'})
  else:
   return jsonify({'erro':'Necessario estar logado!'})
  id=request.args['id']
 except:
  return jsonify({'erro':'´Parametros invalidos'})
 try:
  O=sqlite3.connect(bd)
  k=O.cursor()
  print(f"VALOR DE N: {id}")
  k.execute("UPDATE medicoes SET oculto = ? WHERE id_medicao = ?;",('9',id))
  O.commit()
  k.close()
  O.close()
  return jsonify({'retorno':f"alterado"})
 except Exception as e:
  if O:
   O.close()
  return jsonify({'retorno':f"Erro ao alterar",'erro':f"{e}"})
if __name__=="__main__":
 jJ=True 
 j.run(host='0.0.0.0',port=5000,debug=debug)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

