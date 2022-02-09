#!/usr/bin/env python3
import time
time.sleep(2.0)
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
import sqlite3
import sys

from flask_cors import CORS, cross_origin
import socket #https://wiki.python.org.br/SocketBasico
from datetime import datetime, timedelta
import json

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
from sentry_sdk.integrations.flask import FlaskIntegration
try:
    aa = open('/etc/loader/load/sentry.conf', 'r')
    lines = aa.readlines()
    aa.close()
    init(
        lines[1],
        integrations=[FlaskIntegration()],
        server_name=ns,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
except Exception as e:
    print("erro sentry.conf")

# render template: passando o nome do modelo e a variáveis ele vai renderizar o template
# request: faz as requisições da nosa aplicação
# redirect: redireciona pra outras páginas
# session: armazena informações do usuário
# flash:mensagem de alerta exibida na tela
# url_for: vai para aonde o redirect indica

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

bd_m = '/etc/loader/load/loader_banco.db'
bd_conf = '/etc/loader/load/conf_banco.db'
version = '3.1.0'

# chave secreta da sessão
app.secret_key = 'flask'
#app.config.from_object('config')
class Usuario:
    def __init__(self, login, nome, telefone, email, privilegios, senha):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.Telefone = telefone
        self.email = email
        self.privilegios = privilegios

class Medicao:
    def __init__(self, id_medicao, temperatura, umidade, alerta, data):
        self.id_medicao = id_medicao
        self.temperatura = temperatura
        self.umidade = umidade
        self.alerta = alerta
        self.data = data

class Config:
    def __init__(self, etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs):
        self.etapa = etapa
        self.intervalo_seconds = intervalo_seconds
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.umid_ajuste = umid_ajuste
        self.escala_temp = escala_temp
        self.alerta_desat = alerta_desat
        self.speaker = speaker
        self.updated = updated
        self.obs = obs

class ConfigEtapa:
    def __init__(self,  temp_min, temp_max, umid_ajuste, etapa, updated, expiration, intervalo_seconds, id_etapa, obs):
        self.temp_min = temp_min
        self.intervalo_seconds = intervalo_seconds
        self.temp_max = temp_max
        self.umid_ajuste = umid_ajuste
        self.etapa = etapa
        self.updated = updated
        self.expiration = expiration
        self.obs = obs
        self.id_etapa = id_etapa
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

from views import auth

# PARA ALTERAR DATATIME DO RASPBERRY - http://127.0.0.1:5000/updatedatasistema?datetime="Mon Aug 28 20:10:11 UTC-3 2019"
@app.route('/updatedatasistema', methods=['GET', ])
def updatedatasistema():
    try:
        datetime_request = request.args['datetime']
        return_token = auth.verify_autentication_api(request.args['token'])
        if 'autenticado' in return_token:
            print('autenticado')
        else:
            return jsonify({'erro': 'Necessario estar logado'})
    except Exception as e :
        capture_exception(e)
        return jsonify({'erro': 'Necessario estar logado'})
    import os
    from datetime import datetime
    try:
        # c = os.popen('sudo date -s "Mon Aug 28 20:10:11 UTC-3 2019"')
        print(f"sudo date -s  '{datetime_request}'")
        c = os.popen(f"sudo date -s '{datetime_request}'")
        c.read()
        c.close()
        now = datetime.now()
    except Exception as e :
        capture_exception(e)
        return jsonify({'datetime': f"{now}"})
    return jsonify({'datetime': f"{now}"})  # ip do raspberry
    # return jsonify({'retorno' : f"{request.remote_addr}"}) #ip do requisitante

# PARA ALTERAR DATATIME DO RASPBERRY - http://127.0.0.1:5000/updatedatasistema?datetime="Mon Aug 28 20:10:11 UTC-3 2019"
@app.route('/atualizar', methods=['GET', ])
def atualizar():
    try:
        return_token = auth.verify_autentication_api(request.args['token'])
        if 'autenticado' in return_token:
            print('autenticado')
        else:
            return jsonify({'erro': 'Necessario estar logado'})
    except Exception as e :
        capture_exception(e)
        return jsonify({'erro': 'Necessario estar logado'})
    import os
    from datetime import datetime
    import subprocess
    try:
        arquivo = open('/etc/loader/loader/version.conf', 'r')
        version = arquivo.readline()
        arquivo.close()
        subprocess.run(["sudo", "python3", "/etc/loader/loader/atualiza.py"])
        now = datetime.now()
        arquivo = open('/etc/loader/loader/version.conf', 'w')
        arquivo.write(version + 0.1)
        arquivo.close()
        return jsonify({'retorno': f"Atualização concluída {version}"})
    except Exception as e :
        capture_exception(e)
        return jsonify({'erro': f"{e}"})

@app.route('/rollback_atualizar', methods=['GET', ])
def rollback_atualizar():
    try:
        return_token = auth.verify_autentication_api(request.args['token'])
        if 'autenticado' in return_token:
            print('autenticado')
        else:
            return jsonify({'erro': 'Necessario estar logado'})
    except Exception as e :
        capture_exception(e)
        return jsonify({'erro': 'Necessario estar logado'})
    import os
    from datetime import datetime
    import subprocess
    try:
        arquivo = open('/etc/loader/loader/version.conf', 'r')
        version = arquivo.readline()
        arquivo.close()
        subprocess.run(["sudo", "python3", "/etc/loader/loader/rollback_updt.py"])
        now = datetime.now()
        arquivo = open('/etc/loader/loader/version.conf', 'w')
        arquivo.write(version - 0.1)
        arquivo.close()
        return jsonify({'retorno': f"Desfeito ultima atualização"})
    except Exception as e :
        capture_exception(e)
        return jsonify({'erro': f"{e}"})


# PARA Alterar hora do sistema
@app.route('/scan', methods=['GET', 'POST'])
@cross_origin()
def scan():
    from datetime import datetime
    try:
        active = auth.verify_key()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        s.close()
        now = datetime.now()
        return jsonify(
            {'retorno': f"{IP}", 'datetime': f"{now}", 'nome': 'Estufa 1', 'a': f"{active}", 'version': f"{version}"})  # ip do raspberry
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': f"{e}"})  # ip do raspberry
    # return jsonify({'retorno' : f"{request.remote_addr}"}) #ip do requisitante

# PARA Alterar hora do sistema
@app.route('/sis', methods=['POST'])
def sis():
    from datetime import datetime
    try:
        # mac = ''
        # fd = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        # fd.bind(('eth0', 9999))
        # mac = fd.getsockname()[-1]
        # print(mac)
        # # print(':'.join(['%02x' % ord(n) for n in mac]))
        #from uuid import getnode as get_mac
        #mac = get_mac()
        ns = auth.getserial()
        now = datetime.now()
        return jsonify({'retorno': f"{ns}", 'datetime': f"{now}", 'nome': 'Estufa 1'})  # ip do raspberry
    except Exception as e:
        print(f"Erro SIS: {e}")
        capture_exception(e)
        return jsonify({'retorno': f"erro", 'nome': 'Estufa 1'})  # ip do raspberry
    # return jsonify({'retorno' : f"{request.remote_addr}"}) #ip do requisitante


@app.route('/loader', methods=['POST'])
def loader():
    try:
        print(request.json['cod'])
        print(request.json['key'])
        if 'cod' in request.json:
            if 'key' in request.json:
                payload = {
                    'cod': request.json['cod'],
                    'key': request.json['key']
                    # 'exp': (datetime.datetime.now() + datetime.timedelta(weeks=2)).timestamp(),
                }
                jwt_created = auth.create_jwt(payload)
                arquivo = open('/etc/loader/load/load.conf', 'w')
                arquivo.write(jwt_created)
                arquivo.close()
                # return {'token': jwt_created} # armazenar para utilizar posteriormente
                return jsonify({'token': f"{jwt_created}"})
            else:
                return jsonify({'erro': 'Key invalido!'})
        else:
            return jsonify({'erro': 'Cod invalida!'})
    except Exception as e :
        capture_exception(e)
        print(f"Erro Loader: {e}")
        return jsonify({'erro': f"Erro Loader: {e}"})


# configuração da rota index.
@app.route('/', methods=['GET', 'OPTIONS'])
def index():
    logado = 1
    medicoes = []
    temperaturas = []
    umidades = []
    dias = []
    alertas = []
    a = auth.verify_key()
    a = 1  # deletar no futuro
    conf = getLocalConfigGeral()
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        cur.execute(
            "SELECT id_medicao, temperatura, umidade, strftime('(%d) %H:%M',created) FROM medicoes"
            " WHERE oculto = '0' or oculto = '2' ORDER BY id_medicao DESC LIMIT 50")
        for id_medicao, temperatura, umidade, data in cur:
            temp = round(temperatura, 1)
            if conf.escala_temp == 'C':
                temp = round(((temperatura - 32) * 5/9), 1)
            medicoes.append(
                {'id': id_medicao, 'temperatura': float(temp),
                 'umidade': float(umidade),
                 'data': f"{data}"})
            temperaturas.insert(0, float(temp))
            umidades.insert(0, float(umidade))
            dias.insert(0, f"{data}")
        cur.execute(
            "SELECT id_medicao, temperatura, umidade, alerta, strftime('(%d) %H:%M',created) FROM medicoes"
            " WHERE alerta = 1 and status = 0 ORDER BY created DESC LIMIT 25")
        for id_medicao, temperatura, umidade, alerta, created in cur:
            descricao = ''
            if alerta == 1:
                descricao == f"Temperatura: {temperatura} está fora"
            elif alerta == 3:
                descricao == f"Umidade: {umidade} está fora"
            elif alerta == 4:
                descricao == f"Umidade: {umidade} e Temperatura: {temperatura} estão fora"
            alertas.append(
                {'id': id_medicao,
                 'temperatura': float(temperatura),
                 'umidade': float(umidade),
                 'descricao': descricao,
                 'created': f"{created}"})
        cur.execute("SELECT temperatura, umidade, alerta, strftime('(%d) %H:%M',updated) "
                    "FROM medicao WHERE id_medicao = 1")
        rows = cur.fetchall()

        medicao = {'temp': 0, 'umid': 0, 'alert': 0, 'upd': 'erro'}
        if len(rows) > 0:
            tm = round(rows[0][0], 1)
            if conf.escala_temp == 'C':
                tm = round(((round(rows[0][0], 1) - 32) * 5/9), 1)
            medicao = {'temp': tm, 'umid': round(rows[0][1], 1), 'alert': rows[0][2], 'upd': rows[0][3], 'escala': conf.escala_temp}
        cur.close()
        conn.close()
        if 'usuario_logado' not in session or session['usuario_logado'] == None:
            logado = 0
    except Exception as e :
        capture_exception(e)
        print(f"Erro SQLite: {e}")
    return render_template('lista.html', titulo='Medições', medicoes=medicoes, temperaturas=temperaturas,
                           umidades=umidades, dias=dias, alertas=alertas, a=a, logado=logado, medicao=medicao )


def verificaAlerta(alerta):
    retorno = {'tem_alert': '', 'temp_umid': ''}
    if alerta == 11 or alerta == 44 or alerta == 47:
        retorno.tem_alert = 'alta'
    elif alerta == 12 or alerta == 45 or alerta == 48:
        retorno.tem_alert = 'baixo'
    else: 
         retorno.tem_alert = ''
    if alerta == 33 or alerta == 44 or alerta == 45:
        retorno.temp_umid = 'alta'
    elif alerta == 36 or alerta == 47 or alerta == 48:
        retorno.temp_umid = 'baixo'
    else: 
        retorno.temp_umid = ''

# API ACOMPANHAMENTO MEDIÇÃO
@app.route('/medicao', methods=['GET'])
def medicao():
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        cur.execute("SELECT temperatura, temperatura2, umidade, alerta, updated "
                    "FROM medicao WHERE id_medicao = 1")
        retornoBD = []
        for temperatura, temperatura2, umidade, alerta, updated in cur:
            retornoBD.append(
                {'temperatura': float(temperatura),
                'temperatura2': float(temperatura2),
                 'umidade': float(umidade),
                 'alerta': alerta,
                 'updated': f"{updated}"})
        cur.close()
        conn.close()
        return jsonify(retornoBD)
    except Exception as error:
        capture_exception(error)
        print(f"Erro Medição SQLITE: {error}")
        return jsonify({'erro': f"{error}"})

# API
@app.route('/medicoes', methods=['GET'])
def medicoes():
    # para GET http://127.0.0.1:5000/medicao?datainicial=2020-12-10&datafinal=2021-01-20&oculto=1,1,1,1
    # print(request.args['datainicial']) #'2020-12-15'
    # print(request.args['datafinal']) # '2020-12-25'
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        print(request.args['oculto'])
        ocultopesq = request.args['oculto'].split(',')
        if len(ocultopesq) != 4:
            ocultopesq = [0, 1, 2, 3]
        cur.execute("SELECT id_medicao, temperatura, umidade, alerta, created FROM medicoes"
                    " WHERE created >= ? and created <= ? and (oculto = ? or oculto = ? or oculto = ? or oculto = ?) ORDER BY id_medicao DESC LIMIT 60",
                    (request.args['datainicial'], request.args['datafinal'], ocultopesq[0], ocultopesq[1], ocultopesq[2], ocultopesq[3]))
        retornoBD = []
        for id_medicao, temperatura, umidade, alerta, created in cur:
            retornoBD.append(
                {'id': id_medicao,
                 'temperatura': float(temperatura),
                 'umidade': float(umidade),
                 'alerta': alerta,
                 'data': f"{created}"})
        cur.close()
        conn.close()
        return jsonify(retornoBD)
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        #sys.exit(1)
        return jsonify({'erro': f"{e}"})


# API
@app.route('/alertas', methods=['GET'])
def alertas():
    # para GET http://127.0.0.1:5000/medicao?datainicial=2020-12-10&datafinal=2021-01-20
    # print(request.args['datainicial']) #'2020-12-15'
    # print(request.args['datafinal']) # '2020-12-25'
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        cur.execute(
            "SELECT id_medicao, temperatura, umidade, alerta, created FROM medicoes"
            " WHERE alerta > 0 and status = 0 ORDER BY id_medicao DESC LIMIT 25")
        retornoBD = []
        for id_medicao, temperatura, umidade, alerta, created in cur:
            retornoBD.append(
                {'id': id_medicao,
                 'temperatura': float(temperatura),
                 'umidade': float(umidade),
                 'alerta': alerta,
                 'data': f"{created}"})
        cur.close()
        conn.close()
        return jsonify(retornoBD)
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return jsonify({'erro': f"{e}"})

# API Alertas por data
@app.route('/alertasperiodo', methods=['GET'])
def alertasperiodo():
    # para GET http://127.0.0.1:5000/medicao?datainicial=2020-12-10&datafinal=2021-01-20
    # print(request.args['datainicial']) #'2020-12-15'
    # print(request.args['datafinal']) # '2020-12-25'
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        cur.execute(
            "SELECT id_medicao, temperatura, umidade, alerta, created FROM medicoes"
            " WHERE  created >= ? and created <= ? and alerta > 0 ORDER BY id_medicao DESC LIMIT 50",
            (request.args['datainicial'], request.args['datafinal']))
        retornoBD = []
        for id_medicao, temperatura, umidade, alerta, created in cur:
            retornoBD.append(
                {'id': id_medicao,
                 'temperatura': float(temperatura),
                 'umidade': float(umidade),
                 'alerta': alerta,
                 'data': f"{created}"})
        cur.close()
        conn.close()
        return jsonify(retornoBD)
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return jsonify({'erro': f"{e}"})

## api de configurações
@app.route('/apiconfig', methods=['GET'])
def apiconfig():
    try:
        configui = configRetorno()
        return jsonify(configui)
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': f"{e}"})

## api de configurações
@app.route('/apiconfigetapa', methods=['GET'])
def apietapaconfig():
    try:
        configEtapa = configRetornoEtapa()
        return jsonify(configEtapa)
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': f"{e}"})

## api de configurações
@app.route('/apiconfiggeral', methods=['GET'])
def apiconfiggeral():
    try:
        configui = configRetorno()
        return jsonify(configui)
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': f"{e}"})

def configRetorno():
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        cur.execute(
            "SELECT nome,  etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs "
            "FROM config WHERE id_config = 1")
        configs = []
        for nome, etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs in cur:
            configs.append(
                {'nome' : nome,
                'etapa': etapa,
                'intervalo_seconds': int(intervalo_seconds),
                'temp_min': float(temp_min),
                'temp_max': float(temp_max),
                'umid_ajuste': umid_ajuste,
                'escala_temp': escala_temp,
                'alerta_desat': alerta_desat,
                'speaker': speaker,
                'updated': f"{updated}",
                'obs': obs})
        cur.close()
        conn.close()
        return configs[0]
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return {'erro': f"{e}"}

def configRetornoEtapa():
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        cur.execute(
            "SELECT  temp_min, temp_max, umid_min, umid_max, umid_ajuste, etapa, updated, expiration, intervalo_seconds, id_etapa, obs FROM etapa WHERE status = 1")

        configs = []
        for temp_min, temp_max, umid_min, umid_max, umid_ajuste, etapa, updated, expiration, intervalo_seconds, id_etapa, obs  in cur:
            configs.append(
                {'id_etapa' : id_etapa,
                'etapa': etapa,
                'intervalo_seconds': int(intervalo_seconds),
                'temp_min': float(temp_min),
                'temp_max': float(temp_max),
                'umid_min': float(umid_min),
                'umid_max': float(umid_max),
                'umid_ajuste': umid_ajuste,
                'expiration': expiration,
                'updated': f"{updated}",
                'obs': obs})

        if len(configs) > 0:
            cur.close()
            conn.close()
            return configs[0]
        else:
            cur.execute("UPDATE etapa SET status = 1 WHERE id_config = 5;")
            conn.close()
            return {'erro': f"Erro: Tente novamente"}
        
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return {'erro': f"{e}"}


@app.route('/apietapasconfig', methods=['GET'])
def apietapasconfig():
    try:
        configEtapas = getconfigetapas()
        return jsonify(configEtapas)
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': f"{e}"})


def getconfigetapas():
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        cur.execute(
            "SELECT  temp_min, temp_max, umid_min, umid_max, umid_ajuste, etapa, updated, expiration, intervalo_seconds, id_etapa, obs, status FROM etapa;")
        configs = []
        for temp_min, temp_max, umid_min, umid_max, umid_ajuste, etapa, updated, expiration, intervalo_seconds, id_etapa, obs, status  in cur:
            configs.append(
                {'id_etapa' : id_etapa,
                'etapa': etapa,
                'intervalo_seconds': int(intervalo_seconds),
                'temp_min': float(temp_min),
                'temp_max': float(temp_max),
                'umid_min': float(umid_min),
                'umid_max': float(umid_max),
                'umid_ajuste': umid_ajuste,
                'expiration': expiration,
                'updated': f"{updated}",
                'obs': obs,
                'status': status})
        cur.close()
        conn.close()
        return configs
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return {'erro': f"{e}"}

def getLocalConfigEtapa():
    try:
        # global configFaixa
        con = sqlite3.connect(bd_conf)
        cursor = con.cursor()
        cursor.execute(
            "SELECT  temp_min, temp_max, umid_ajuste, etapa, updated, expiration, intervalo_seconds, id_etapa, obs FROM etapa WHERE status = 1")

        rows = cursor.fetchall()
        if len(rows) > 0:
            con.close()
            return ConfigEtapa(float(rows[0][0]), float(rows[0][1]), int(rows[0][2]), rows[0][3], rows[0][4],
                               rows[0][5], rows[0][6], rows[0][7], rows[0][8]).toJSON()
        else:
            cursor.execute(
                "SELECT  temp_min, temp_max, umid_ajuste, etapa, updated, expiration, intervalo_seconds, id_etapa, obs FROM etapa WHERE id_config = 5;")
            rows = cursor.fetchall()
            cursor.execute("UPDATE etapa SET status = 1 WHERE id_config = 5;")
            con.close()
            return ConfigEtapa(float(rows[0][0]), float(rows[0][1]), int(rows[0][2]), rows[0][3], rows[0][4],
                               rows[0][5], rows[0][6], rows[0][7], rows[0][8])
    except Exception as e:
        print('Erro consultar BD getLocalConfigFaixa', e)
        time.sleep(2)
        return False

def getLocalConfigGeral():
    try:
        con = sqlite3.connect(bd_conf)
        cursor = con.cursor()
        cursor.execute(
            "SELECT etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs FROM config WHERE id_config = 1;")
        rows = cursor.fetchall()
        if len(rows) > 0:
            con.close()
            return Config(rows[0][0], int(rows[0][1]), int(rows[0][2]), int(rows[0][3]), int(rows[0][4]), rows[0][5], rows[0][6], rows[0][7], rows[0][8], rows[0][9])
        else:
                return {'erro': f"Nenhum registro encontrado"}
    except Exception as e:
        capture_exception(e)
        print('Erro consultar BD getLocalConfigGeral', e)
        return {'erro': f"{e}"}

# configuração da rota novo, ela só poderá ser acessda se o usuário estiver logado, caso contrário redireciona para a tela de login
@app.route('/novo')
def novo():
    usuarios = []
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        cur.execute("SELECT login, nome, telefone, email, privilegios FROM usuario")
        for login, nome, telefone, email, privilegios in cur:
            usuarios.append(Usuario(login, nome, telefone, email, privilegios, ' '))
        cur.close()
        conn.close()
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo='Novo Usuario', usuarios=usuarios)

@app.route('/criar', methods=['POST', ])
def criar():
    try:
        login_retorno2 = auth.get_user_bd(request.form['login'].lower())
        retornoj2 = jsonify(login_retorno2)
        if 'inexistente' in retornoj2.json:
            conn = sqlite3.connect(bd_conf)
            cur = conn.cursor()
            cur.execute("INSERT INTO Usuario(login, senha, nome, telefone, email, privilegios) VALUES (?, ?, ?, ?, ?, ?);",
                        (
                            request.form['login'].lower(),
                            request.form['Senha'].lower(),
                            request.form['Nome'],
                            request.form['Telefone'],
                            request.form['Email'],
                            'adm'
                        ))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        else:
            flash(f"Erro: Esse login de usuário já existe!")
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        if conn:
            conn.close()
        return redirect(url_for('novo'))

# configuração da rota login .
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

# configuração da rota autenticar que verifica se existe o usuário no bd
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        login = request.form['login'],
        senha = request.form['senha'],
        print(login, senha)
        cur.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario "
                    "WHERE login = ? and senha = ?", (login[0].lower(), senha[0].lower(),))
        usuario = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        flash(f"Erro SQLite: {e}")
        return redirect(url_for('login'))
    if len(usuario) == 1:
        session['usuario_logado'] = usuario[0][0]
        flash(usuario[0][2] + ' acesso permitido!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        try:
            login = request.form['login'],
            senha = request.form['senha'],
            insert_valida = auth.button_login(login[0].lower(), senha[0].lower(), bd_conf)
        except Exception as e:
            print("erro"  , e)

        if insert_valida == 1:
            try:
                conn = sqlite3.connect(bd_conf)
                cur = conn.cursor()
                login = request.form['login'],
                senha = request.form['senha'],
                print(login, senha)
                cur.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario "
                            "WHERE login = ? and senha = ?", (login[0].lower(), senha[0].lower(),))
                usuario = cur.fetchall()
                cur.close()
                conn.close()
            except Exception as e:
                capture_exception(e)
                print(f"Erro SQLite: {e}")
                flash(f"Erro SQLite: {e}")
                return redirect(url_for('login'))
            if len(usuario) == 1:
                session['usuario_logado'] = usuario[0][0]
                flash(usuario[0][2] + ' acesso permitido!')
                proxima_pagina = request.form['proxima']
                return redirect(proxima_pagina)
            else:
                flash('Acesso negado, digite novamente!')
                return redirect(url_for('login'))
        else:
            flash('Acesso negado, digite novamente!')
            return redirect(url_for('login'))



@app.route('/keycloud', methods=['POST', ])
def keycloud():
    try:
        if 'key' in request.json:
            if 'user' in request.json:
                payload = {
                    'user': request.json['user'],
                    'key': request.json['key']
                    # 'exp': (datetime.datetime.now() + datetime.timedelta(weeks=2)).timestamp(),
                }
                jwt_created = auth.create_jwt(payload)
                print(jwt_created)
                arquivo = open('/etc/loader/load/cloud.conf', 'w')
                arquivo.write(jwt_created)
                arquivo.close()
                return jsonify({'token': jwt_created})
            else:
                return jsonify({'erro': 'Usuario invalido!'})
        else:
            return jsonify({'erro': 'Senha invalida!'})
    except Exception as e:
        capture_exception(e)
        print(e)
        return jsonify({'erro': 'Erro na requisicao'})


@app.route('/loginapi', methods=['POST', ])
def loginapi():
    try:
        if 'senha' in request.json:
            if 'user' in request.json:
                login_retorno = auth.autentication_api(request.json['user'].lower(), request.json['senha'].lower())
                retornoj = jsonify(login_retorno)
                if 'erro' in retornoj.json:
                    insert_valida = auth.button_login(request.json['user'].lower(), request.json['senha'].lower(), bd_conf)
                    if insert_valida == 1:
                        login_retorno = auth.autentication_api(request.json['user'].lower(), request.json['senha'].lower())
                        return jsonify(login_retorno)
                    elif insert_valida == 2:
                        return jsonify({'erro': 'Login de usuário já cadastrado e com senha inválida'})
                    elif insert_valida == 3:
                        return jsonify({'erro': 'Usuário não existe e cadastro de novo usuário recusado'})
                    else:
                        return jsonify({'erro': 'Erro no login, Cadastro de novo usuário recusado'})
                else:
                    return jsonify(login_retorno) #token
            else:
                return jsonify({'erro': 'Usuario invalido!'})
        else:
            return jsonify({'erro': 'Senha não identificada!'})
    except:
        return jsonify({'erro': 'Erro na requisicao'})

# configuração da rota logout
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado')
    return redirect(url_for('index'))

##key utilizado pelo JWT
@app.route('/resetarkey', methods=['GET', ])
def resetarkey():
    try:
        return_token = auth.verify_autentication_api(request.args['token'])
        if 'autenticado' in return_token:
            print('autenticado 491')
        else:
            return jsonify({'erro': 'Necessario estar logado'})
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': 'Necessario estar logado'})
    try:
        arquivo = open('/etc/loader/load/key.conf', 'w')
        arquivo.write(f'{datetime.now()}')
        arquivo.close()
        return jsonify({'retorno': 'Resetado todos os acessos com sucesso'})
    except Exception as e:
        capture_exception(e)
        print('erro ao criar arquivo', e)
        return jsonify({'erro': e})

## formulário de configuração
@app.route('/config')
def config():
    config = ''
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        cur.execute(
            "SELECT etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs "
            "FROM config WHERE id_config = 1")
        for etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, updated, obs in cur:
            config = Config(etapa, int(intervalo_seconds), float(temp_min), float(temp_max), int(umid_ajuste), str(escala_temp),
                            int(alerta_desat), int(speaker), str(updated), obs)
        cur.close()
        conn.close()
    except Exception as e:
        capture_exception(e)
        flash(f"Erro SQLite: {e}")
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('config.html', titulo='Configuração', config=config)

@app.route('/excluiruser', methods=['POST', ])
def excluiruser():
    try:
        if 'usuario_logado' not in session or session['usuario_logado'] == None:
            return redirect(url_for('login', proxima=url_for('novo')))
        print((f"{request.form['login']}"))
        flash('Você deletou o usuário:', request.form['login'])
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        print('excluindo ', (request.form['login']))
        print((request.form['login'],))
        cur.execute("DELETE FROM usuario WHERE login = ?;", (request.form['login'],))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('novo'))
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return redirect(url_for('novo'))



## Para realizar update nas configurações enviadas pelo form config
@app.route('/salvarconfig', methods=['POST', ])
def salvarconfig():
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        intervalo = request.form['intervalo']
        print("intervalo", intervalo)
        if int(intervalo) < 60:
            intervalo = 60
        print((
                request.form['etapa'],
                intervalo,
                request.form['umidAjuste'],
                request.form['escalaTemp'],
                request.form['alertaDesat'],
                request.form['speaker'],
                request.form['obs']
            ))
        cur.execute(
            "UPDATE Config SET etapa = ?, intervalo_seconds= ?, umid_ajuste = ?, escala_temp = ?, alerta_desat = ?, speaker = ?, updated = datetime('now'), obs = ? WHERE id_config = 1;",
            (
                request.form['etapa'],
                intervalo,
                request.form['umidAjuste'],
                request.form['escalaTemp'],
                request.form['alertaDesat'],
                request.form['speaker'],
                request.form['obs']
            ))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return redirect(url_for('config'))


## API Para realizar update nas configurações enviadas pelo form config
@app.route('/apisalvarconfig', methods=['POST', ])
def apisalvarconfig():
    try:
        if 'token' in request.json:

            return_token = auth.verify_autentication_api(request.json['token'])

            if 'autenticado' in return_token:
                print('autenticado')
            else:
                return jsonify({'erro': 'Necessario estar logado!'})
        else:
            return jsonify({'erro': 'Necessario estar logado!'})
        print('salvando')
        if request.json['config']['intervalo_seconds'] < 60:
            intervalo = 60
        else:
            intervalo = request.json['config']['intervalo_seconds']
        
        try: #corrigir depois de implementar campos no app
            escala_temp = request.json['config']['escala_temp']
        except Exception as e:
            capture_exception(e)
            nome = 'Estufa 1'
            escala_temp = 'F'

        try:  # corrigir depois de implementar campos no app
            umid_ajuste = request.json['config']['umid_ajuste']
        except Exception as e:
            capture_exception(e)
            umid_ajuste = 0

        alerta_desat = 0
        speaker = 0
        try: #corrigir depois de implementar campos no app
            speaker = request.json['config']['speaker']
            alerta_desat = request.json['config']['alerta_desat']
        except Exception as e:
            capture_exception(e)
            alerta_desat = 0
            speaker = 0
        try: #corrigir depois de implementar campos no app
            nome = request.json['config']['nome']
        except Exception as e:
            capture_exception(e)
            nome = 'Estufa 1'

        obs = request.json['config']['obs']

        try: #corrigir depois de implementar campos no app
            etapa = request.json['config']['etapa']
        except Exception as e:
            capture_exception(e)
            etapa = 'Personalizada'


    except Exception as e:
        capture_exception(e)
        print(f"Erro 919: {e}")
        return jsonify({'retorno': f"{e}"})
    try:
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        cur.execute(
            "UPDATE config SET nome = ?, etapa = ?, intervalo_seconds= ?, umid_ajuste = ?, escala_temp = ?, alerta_desat = ?, speaker = ?, updated = datetime('now'), obs = ? WHERE id_config = 1;",
            (
                nome,
                etapa,
                intervalo,
                umid_ajuste,
                escala_temp,
                alerta_desat,
                speaker,
                obs
            ))
        conn.commit()
        cur.close()
        conn.close()
        print('salvo')
        return jsonify({'retorno': f"salvo"})
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return jsonify({'retorno': f"{e}"})

@app.route('/apisalvaretapa', methods=['POST', ])
def apisalvaretapa():
    try:
        capture_message('apisalvaretapa')
        if 'token' in request.json:
            return_token = auth.verify_autentication_api(request.json['token'])
            if 'autenticado' in return_token:
                print('autenticado')
            else:
                return jsonify({'erro': 'Necessario estar logado!'})
        else:
            return jsonify({'erro': 'Necessario estar logado!'})
        try:  # corrigir depois de implementar campos no app
            intervalo = 60
            if request.json['config']['intervalo_seconds'] < 60:
                intervalo = 60
            else:
                intervalo = request.json['config']['intervalo_seconds']
        except Exception as e:
            print(e)
        temp_min = request.json['config']['temp_min']
        temp_max = request.json['config']['temp_max']

        try:
            umid_min = request.json['config']['umid_min']
            umid_max = request.json['config']['umid_max']
        except Exception as e:
            umid_min = 0
            umid_max = 0

        try:
            umid_ajuste = request.json['config']['umid_ajuste']
        except Exception as e:
            umid_ajuste = 0
        try:
            id_etapa = request.json['config']['id_etapa']
            etapa = request.json['config']['etapa']
        except Exception as e:
            capture_exception(e)
            id_etapa = 5
            etapa = 'Personalizada'
        obs = request.json['config']['obs']

    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite 585: {e}")
        return jsonify({'retorno': f"{e}"})
    try:
        print('alterando id', id_etapa)
        conn = sqlite3.connect(bd_conf)
        cur = conn.cursor()
        cur.execute("UPDATE etapa SET status = 0, updated = ? WHERE status = 1;", (str(datetime.now()),))
        conn.commit()
        cur.execute(
            "UPDATE etapa SET status = 1, etapa = ?, intervalo_seconds= ?, temp_min = ?, temp_max = ?, umid_min = ?, umid_max = ?, umid_ajuste = ?, updated = ?, obs = ? WHERE id_etapa = ?;",
            (
                etapa,
                intervalo,
                temp_min,
                temp_max,
                umid_min,
                umid_max,
                umid_ajuste,
                str(datetime.now()),
                obs,
                id_etapa
            ))
        conn.commit()
        cur.close()
        conn.close()
        print('salvo')
        return jsonify({'retorno': f"salvo"})
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return jsonify({'retorno': f"{e}"})

@app.route('/silenciaralertas')
def silenciaralertas():
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        cur.execute("UPDATE medicoes SET alerta = 1 WHERE alerta = 0;;")
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        capture_exception(e)
        flash(f"Erro SQLite: {e}")
        if conn:
            conn.close()
        return redirect(url_for('index'))


# api do Ionic para silenciar os alertas
@app.route('/silenciaralertasapi', methods=['GET'])
def silenciaralertasapi():
    try:
        return_token = auth.verify_autentication_api(request.args['token'])
        if 'autenticado' in return_token:
            print('autenticado')
        else:
            return jsonify({'erro': 'Necessario estar logado'})
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': '´Parametros invalidos'})
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        cur.execute("UPDATE medicoes SET status = 1 WHERE status = 0;")
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'retorno': f"ok"})
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        if conn:
            conn.close()
        #flash(e)
        return jsonify({'retorno': f"{e}"})


## API para deletar medições
@app.route('/apiocultarmedicoes', methods=['GET', ])
def apiocultarmedicoes():
    try:
        if 'token' in request.json:
            return_token = auth.verify_autentication_api(request.json['token'])
            if 'autenticado' in return_token:
                print('autenticado')
            else:
                return jsonify({'erro': 'Necessario estar logado!'})
        else:
            return jsonify({'erro': 'Necessario estar logado!'})
        id = request.args['id']
    except Exception as e:
        capture_exception(e)
        return jsonify({'erro': '´Parametros invalidos'})
    try:
        conn = sqlite3.connect(bd_m)
        cur = conn.cursor()
        print(f"VALOR DE N: {id}")
        cur.execute(
            "UPDATE medicoes SET oculto = ? WHERE id_medicao = ?;",
            (
                '9',
                id
            ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'retorno': f"alterado"})
    except Exception as e:
        capture_exception(e)
        return jsonify({'retorno': f"Erro ao alterar", 'erro': f"{e}"})


if __name__ == "__main__":
    debug = True  # com essa opção como True, ao salvar, o "site" recarrega automaticamente.
    try:
        app.run(host='0.0.0.0', debug=debug, port=5000)
        #app.run()
    except Exception as e:
        capture_exception(e) 


# ##app.run(host='0.0.0.0', port=8080)
# sudo apt-get install --reinstall raspberrypi-boot[15,0 kB]loader raspberrypi-kernel
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
