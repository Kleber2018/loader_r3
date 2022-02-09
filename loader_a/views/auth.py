#para jwt
import hmac
import hashlib
import base64
import json
import datetime
import sqlite3

from flask import jsonify

#bd = '/etc/loader/loader/loader_banco.db'
bd = '/etc/loader/load/conf_banco.db'
#https://medium.com/@gustavolpss/json-web-tokens-jwt-em-python-c76fb34d8d9


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
    capture_exception(e)


secret_key = '52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54' #utilizar a data armazenada em key.conf


def create_jwt(payload):
    try:
        arquivo = open('/etc/loader/load/key.conf', 'r')
        secret_key = arquivo.readline()
        arquivo.close()
    except  Exception as e:
        try:
            arquivo = open('/etc/loader/load/key.conf', 'w')
            arquivo.write(f'{datetime.now()}')
            arquivo.close()
        except Exception as e:
            capture_exception(e)
            print('erro ao criar arquivo', e)
        print('erro ao acessar key.conf - create_jwt')

    payload = json.dumps(payload).encode()
    header = json.dumps({
        'typ': 'JWT',
        'alg': 'HS256'
    }).encode()
    b64_header = base64.urlsafe_b64encode(header).decode()
    b64_payload = base64.urlsafe_b64encode(payload).decode()
    signature = hmac.new(
        key=secret_key.encode(),
        msg=f'{b64_header}.{b64_payload}'.encode(),
        digestmod=hashlib.sha256
    ).digest()
    jwt = f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'
    return jwt


def verify_and_decode_jwt(jwt):
    global secret_key
    try:
        arquivo = open('/etc/loader/load/key.conf', 'r')
        secret_key = arquivo.readline()
        arquivo.close()
    except Exception as e:
        capture_message('erro ao acessar key.conf - verify jwt')
        print('erro ao acessar key.conf - verify jwt')
    try:
        b64_header, b64_payload, b64_signature = jwt.split('.')
        b64_signature_checker = base64.urlsafe_b64encode(
            hmac.new(
                key=secret_key.encode(),
                msg=f'{b64_header}.{b64_payload}'.encode(),
                digestmod=hashlib.sha256
            ).digest()
        ).decode()
        # payload extraido antes para checar o campo 'exp'
        payload = json.loads(base64.urlsafe_b64decode(b64_payload))
        unix_time_now = datetime.datetime.now().timestamp()
        if payload.get('exp') and payload['exp'] < unix_time_now:
            capture_message('Token expirado')
            raise Exception('Token expirado')
        if b64_signature_checker != b64_signature:
            capture_message('Assinatura invalida')
            raise Exception('Assinatura invalida')
        return payload
    except Exception as e:
        return {'erro': 'Token invalido'}

def verify_key_mac():
    try:
        from uuid import getnode as get_mac
        arquivo = open('/etc/loader/load/load.conf', 'r')
        token = arquivo.readline()
        arquivo.close()
        decoded = verify_and_decode_jwt(token)
        if f"{get_mac()}" == f"{decoded['cod']}":
            return  1
    except Exception as e:
        capture_exception(e)
        print('erro ativação key', e)
        return 0

def verify_key():
    try:
        arquivo = open('/etc/loader/load/load.conf', 'r')
        token = arquivo.readline()
        arquivo.close()
        decoded = verify_and_decode_jwt(token)
        print(f"código: {decoded['cod']}")
        if f"{getserial()}" == f"{decoded['cod']}":
            return  1
        else:
            return 0
    except Exception as error:
        capture_message('erro na ativação')
        print('erro ativação key', error)
        return 0


def autentication_api(user, senha):
    try:
        #enviado pelo param do get na url
        #print(request.args.get('user'))
        conn = sqlite3.connect(bd)
        cur = conn.cursor()
        cur.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario "
                    "WHERE login = ? and senha = ?", (user.lower(), senha.lower()))
        usuario = cur.fetchall()
        cur.close()
        conn.close()
        # retorna ('kleber', '1234', 'Kleber Santos', '988572209', 'klebers@alunos.utfpr.edu.br', 'admin')
        if len(usuario) == 1:
            print('antes', usuario[0][0])
            print(usuario[0][0])
            payload = {
                'login': user.lower(),
                'senha': senha.lower()
                # 'exp': (datetime.datetime.now() + datetime.timedelta(weeks=2)).timestamp(),
            }
            jwt_created = create_jwt(payload)
            return {'token': jwt_created}
        else:
            return {'erro': 'Usuario ou senha invalido!'}
    except Exception as e:
        capture_exception(e)
        print(f"Erro bd 172: {e}")
        return {'erro': f"Erro BD: {e}", 'description': 'Erro no banco de dados, reinicie a central!'}

#para não ter usuário duplicado
def get_user_bd(user):
    try:
        #enviado pelo param do get na url
        #print(request.args.get('user'))
        conn = sqlite3.connect(bd)
        cur = conn.cursor()
        cur.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario "
                    "WHERE login = ?", (user.lower(),))
        usuario = cur.fetchall()
        cur.close()
        conn.close()
        # retorna ('kleber', '1234', 'Kleber Santos', '988572209', 'klebers@alunos.utfpr.edu.br', 'admin')
        if len(usuario) == 1:
            print('antes', usuario[0][0])
            return {'existe': user.lower()}
        else:
            return {'inexistente': 'Usuário não existe'}
    except Exception as e:
        capture_exception(e)
        print(f"Erro bd 195: {e}")
        return {'erro': f"Erro BD: {e}", 'description': 'Erro no banco de dados, reinicie a central!'}


    #return_token = verify_autentication_api(jwt_created)
    #if 'autenticado' in return_token:
    #    print('autenticado')
    #else:
    #    print('não autenticado')
def verify_autentication_api(token):
    decoded_jwt = verify_and_decode_jwt(token)
    if 'senha' in decoded_jwt:
        if 'login' in decoded_jwt:
            print('existe')
        else:
            return {'erro': 'Usuario invalido!'}
    else:
        return {'erro': 'Senha invalida!'}
    try:
        # enviado pelo param do get na url
        # print(request.args.get('user'))
        conn = sqlite3.connect(bd)
        cur = conn.cursor()
        cur.execute("SELECT login, senha, nome, telefone, email, privilegios FROM usuario "
                    "WHERE login = ? and senha = ?", (decoded_jwt['login'], decoded_jwt['senha']))
        usuario = cur.fetchall()
        cur.close()
        conn.close()
        if len(usuario) == 1:
            return {'autenticado': 'ok'}
        else:
            return {'erro': 'Usuario ou senha invalido!'}
    except Exception as e:
        capture_exception(e)
        print(f"Erro SQLite: {e}")
        return {'erro': f"Erro BD: {e}", 'description': 'Erro no banco de dados, reinicie a central!'}

def button_login(user, senha, bd):
    try:
        from datetime import datetime, timedelta
        arquivo = open('/etc/loader/load/login_livre.conf', 'r')
        horario = arquivo.readline()
        arquivo.close()
        hora_login_livre = datetime.fromisoformat(horario)
        agora = datetime.now()
        print(agora, hora_login_livre, agora+timedelta(minutes = 2))
        print(agora > hora_login_livre, hora_login_livre+timedelta(minutes = 2) > agora)
        login_retorno2 = get_user_bd(user.lower())
        retornoj2 = jsonify(login_retorno2)
        if 'inexistente' in retornoj2.json:
            if agora > hora_login_livre and hora_login_livre+timedelta(minutes = 2) > agora:
                try:
                    conn = sqlite3.connect(bd)
                    cur = conn.cursor()
                    cur.execute("INSERT INTO usuario(login, senha, nome, telefone, email, privilegios) VALUES (?, ?, ?, '', '', 'default');", ( user.lower(), senha.lower(), user ))
                    conn.commit()
                    cur.close()
                    conn.close()
                    return 1
                except Exception as e:
                    capture_exception(e)
                    print(f"Erro SQLite: {e}")
                    return 0
            else:
                return 3
        else:
            return 2
    except Exception as e:
        capture_exception(e)
        print('erro ao criar arquivo', e)
        return 0




