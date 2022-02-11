#!/usr/bin/env python3
#python3 /home/estufaTabaco/main.py

from ast import Try
import time
import board
import RPi.GPIO as GPIO

from views import service

global ns
ns = service.getserial()

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


import threading #https://www.tutorialspoint.com/python3/python_multithreading.htm
import json

#iniciando LED
try:
    #GPIO.setup(21, GPIO.OUT) # LED 1
    #GPIO.setup(6, GPIO.OUT)
    #GPIO.setup(5, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT) #motor fornalha
    GPIO.setup(26, GPIO.OUT) #led run
    GPIO.setup(12, GPIO.OUT) # speaker
    GPIO.setup(20, GPIO.OUT) # led Motor fornalha
    GPIO.setup(22, GPIO.OUT) # flap led
    GPIO.setup(7, GPIO.OUT) # flap comando 1
    GPIO.setup(18, GPIO.OUT) # flap comando 1
    GPIO.output(7, False)  # Acende o LED 1
    GPIO.output(18, False)  # Acende o LED 2

    GPIO.output(27, False)  # Acende o LED 2
    #GPIO.output(21, True)  # Acende o LED 1
    #GPIO.output(5, True)  # Acende o LED 2
    #GPIO.output(6, True)  # Acende o LED 3
    #GPIO.output(13, True)  # Acende o LED 4

except RuntimeError as error:
    capture_exception(error)
    print('Erro LED', error.args[0])
except Exception as error:
    capture_exception(error)
    print('erro led')

#Display: https://pypi.org/project/raspberrypi-tm1637/
import tm1637
global display_temp
global display_humid
try:
    display_temp = tm1637.TM1637(23, 24, 4) #clk=5, dio=4, luminosidade=1 á 10
    display_temp.show('inic')
except Exception as error:
    print('Erro no display', error)
    capture_exception(error)

try:
    display_humid = tm1637.TM1637(14, 15, 5)
    display_humid.show('inic')
except Exception as error:
    print('Erro no display', error)
    capture_exception(error)



time.sleep(0.4)
import busio
import sqlite3
import sys
#para sht31
#import smbus
import adafruit_sht31d
import os
#para sensor de temperatura DS18B20
import glob
from datetime import datetime, timedelta

#bd = '/home/pi/estufa_banco.db'
bd = '/etc/loader/load/loader_banco.db'
bd_conf = '/etc/loader/load/conf_banco.db'
bd_umid = '/etc/loader/load/umid_banco.db' #tabela de umidade para referencia 




#inicializando SOCKET
import socketio
sio = socketio.Client()
@sio.event
def connect():
    print('connection established')
@sio.event
def message(data):
    print('message received with ', data)
    #sio.emit('my response', {'response': 'my response'})
@sio.event
def disconnect():
    print('disconnected from server')
vr_erro = 0 #caso de erro de conexão ele tenta 10 vezes com intervalo de tempo exponencial
while True:
    vr_erro = vr_erro+1
    try:
        sio.connect('http://0.0.0.0:35494')
        break
    except Exception as error:
        display_humid.show('SOKT')
        if vr_erro > 9:
            print('erro socket')
            break
        print('erro no servidor', error)
        capture_exception(error)
        time.sleep(5.0*vr_erro)


from simple_pid import PID


def speaker_alerta(stat, vr, ct_mudo):#se retornar 1 é pq está habilitado o alerta
    try:
        if vr == 1 and ct_mudo < 2:
            GPIO.output(12, stat) #True or False
        else:
            GPIO.output(12, False)
    except Exception as error:
        capture_exception(error)

def motor_fornalha_acionamento(stat, vr):#se retornar 1 é pq está habilitado o motor
    try:
        print('acionando comando 153:', stat, vr)
        if vr == 1:
            GPIO.output(27, stat) #True or False
        else:
            GPIO.output(27, False)
    except Exception as error:
        capture_exception(error)


global login_livre_status
login_livre_status = 11

def set_display_temp(val, tipo):
    global login_livre_status
    #tipo: C:celcius, F: fahrenheit, T: texto
    #val: em fahrenheit
    try:
        if login_livre_status > 10:
            if tipo == 'F':
                if int(val) > 99:
                    display_temp.show(str(str(int(val)) + 'F'))
                else:
                    display_temp.show(str(str(int(val)) + '*F'))
            elif tipo == 'C':
                display_temp.temperature(int(((val-32)/1.8)))
            elif tipo == 'T':
                display_temp.show(str(val))
            else:
                display_temp.show(str(val))
        else:
            login_livre_status =+ 1
    except Exception as error:
        capture_exception(error)

def set_display_umid(val):
    global login_livre_status
    #val: em %
    try:
        if login_livre_status > 10:
            if not str(val).isdigit(): #não numero
                display_humid.show(val)
            else:
                display_humid.show(str('U ' + str(int(val))))
        else:
            login_livre_status =+ 1
    except Exception as error:
        capture_exception(error)


def set_led_run(vr):
    try:
        if vr == 0:
            GPIO.output(26, True)
        else:
            GPIO.output(26, False)
    except Exception as error:
        capture_exception(error)
        print('erro no led status')


global DS18B20status
DS18B20status = False


def iniciaSensorTemp():
    try:
        global DS18B20status
        # Numero dos pinos da Raspberry Pi configurada no modo Broadcom.
        # Pull-up interno habilitado, necessita de um sinal nivel lógico baixo para ser acionado.
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        GPIO.setmode(GPIO.BCM)
        DS18B20status = True
        return device_file
    except RuntimeError as error:
        print('Sensor temperatura erro21', error.args[0])
        set_display_temp('er21', 'T')
        capture_exception(error)
        DS18B20status = False
        return False
    except Exception as error:
        print('Sensor temperatura erro2', error)
        set_display_temp('err2', 'T')
        capture_exception(error)
        DS18B20status = False
        return False

from views import calc
class Medicao:
    def __init__(self, temp, umid, temp2):
        self.temperatura = temp
        self.umidade = umid
        self.temperatura2 = temp2

class ConfigFaixa:
    def __init__(self, temp_min, temp_max, umid_ajuste, etapa, updated, expiration, umid_min, umid_max):
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.umid_ajuste = umid_ajuste
        self.etapa = etapa
        self.updated = updated
        self.expiration = expiration
        self.umid_min = umid_min
        self.umid_max = umid_max
        
class ConfigGeral:
    def __init__(self, intervalo_seconds, umid_ajuste, escala_temp, alerta_desat, speaker, etapa):
        self.intervalo_seconds = intervalo_seconds
        self.umid_ajuste = umid_ajuste
        self.escala_temp = escala_temp
        self.alerta_desat = alerta_desat #datetime até qual horário o alerta vai ficar parado
        self.speaker = speaker
        self.etapa = etapa



# Função habilita os comandos quando os botões forem pressionados.
global desligar
desligar = 0
def Desligar(channel):
    print('deligar')
    global desligar
    desligar = 1
    GPIO.output(26, True)  # Acende o LED
    display_temp.write([0, 0, 0, 0])
    display_humid.write([0, 0, 0, 0])
    time.sleep(0.5)
    display_temp.show('desl')
    display_humid.show('desl')
    time.sleep(2)
    display_temp.write([0, 0, 0, 0])
    display_humid.write([0, 0, 0, 0])
    os.system("sudo shutdown -h now") #os.system("sudo shutdown -r now") para reiniciar
    display_temp.write([0, 0, 0, 0])
    display_humid.write([0, 0, 0, 0])
    sys.exit()

def Login_livre(channel):
    global login_livre_status
    login_livre_status = 0
    print('gpio 16')
    try:
        display_temp.show('logi')
        display_humid.show('2 nn')

        GPIO.output(26, True)  # Acende o LED
        arquivo = open('/etc/loader/load/login_livre.conf', 'w')
        arquivo.write(f'{datetime.now()}')
        arquivo.close()
        import socket #https://wiki.python.org.br/SocketBasico
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        print(IP)

        IPsplited = IP.split('.')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[0])
        display_temp.show('IP 1')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[0])
        display_temp.show('IP 1')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[1])
        display_temp.show('IP 2')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[1])
        display_temp.show('IP 2')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[2])
        display_temp.show('IP 3')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[2])
        display_temp.show('IP 3')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[3])
        display_temp.show('IP 4')
        time.sleep(2)
        display_humid.show('    ')
        display_temp.show('    ')
        display_humid.show(IPsplited[3])
        display_temp.show('IP 4')
        login_livre_status = 21
    except Exception as error:
        login_livre_status = 21
        print(f"Erro Ao criar arquivo: {error}")
        capture_exception(error)

global contador_click
contador_click = 0

global contador_mudo_speak
contador_mudo_speak = 0

def PushButtonEtapa(channel):
    print('botão etapa')
    global contador_click
    global contador_mudo_speak
    contador_mudo_speak = 500
    contador_click += 1
    if contador_click > 1:
        #PulaEtapa()
        contador_click = 0
    else:
        speaker_alerta(False, 0, contador_mudo_speak)
        print('silencia alarme')



def PulaEtapa():  
    try:
        con = sqlite3.connect(bd_conf)
        print('atualizando etapa')
        cursor = con.cursor()
        cursor.execute(
            "SELECT id_etapa FROM etapa WHERE status = 1")
        id_c  = 1
        rows = cursor.fetchall()
        if len(rows) > 0:
            id_c = rows[0][0] + 1
        if id_c > 5:
            id_c = 1
        print(((str(id_c)), str(datetime.now())))
        cursor.execute("UPDATE etapa SET status = 0, updated = ? WHERE status = 1;", (str(datetime.now()),))
        cursor.execute("UPDATE etapa SET status = 1, updated = ? WHERE id_etapa = ?;", (str(datetime.now()), str(id_c)))
        con.commit()
        con.close()
    except Exception as error:
        print(f"erro ao atualizar configuração: {error}")
        capture_exception(error)
    try:
        if configFaixa.etapa == 'Personalizada':
            configFaixa.etapa = 'Amarelação'
            display_temp.show('etap')
            display_humid.show('amar')
        elif configFaixa.etapa == 'Amarelação':
            configFaixa.etapa =  'Murchamento'
            display_temp.show('etap')
            display_humid.show('murc')
        elif configFaixa.etapa ==  'Murchamento':
            configFaixa.etapa = 'Secagem da Lâmina'
            display_temp.show('etap')
            display_humid.show('lami')      
        elif configFaixa.etapa == 'Secagem da Lâmina':
            configFaixa.etapa = 'Secagem do Talo'
            display_temp.show('etap')
            display_humid.show('talo')
        elif configFaixa.etapa == 'Secagem do Talo':
            configFaixa.etapa = 'Personalizada'
            display_temp.show('etap')
            display_humid.show('----')
        else:
            display_temp.show('etap')
            display_humid.show('----')     
    except Exception as e:
        verificaLedEtapa('')
        print(f"Erro Ao acender LED: {e}")




def verificaLedEtapa(etapa_faixa):

    try:
        if etapa_faixa == 'Amarelação':
            display_temp.show('etap')
            display_humid.show('amar')
        elif etapa_faixa == 'Murchamento':
            display_temp.show('etap')
            display_humid.show('murc')
        elif etapa_faixa == 'Secagem da Lâmina':
            display_temp.show('etap')
            display_humid.show('lami')     
        elif etapa_faixa == 'Secagem do Talo':
            display_temp.show('etap')
            display_humid.show('talo')
        elif etapa_faixa == 'Personalizada':
            display_temp.show('etap')
            display_humid.show('----')       
        else:
            display_temp.show('etap')
            display_humid.show('----')
    except Exception as error:
        capture_exception(error)
        print('erro no acender led etapa', error)       

try:
    # Executa as funções para desligar  sistema raspbian.
    #GPIO18 BOTÃO PULAR ETAPA
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) #ou 18 ou 21
    GPIO.add_event_detect(6, GPIO.FALLING, callback=Login_livre, bouncetime=700)

    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(19, GPIO.FALLING, callback=PushButtonEtapa, bouncetime=700)

    #mais
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(5, GPIO.FALLING, callback=PushButtonEtapa, bouncetime=700)

    #menos
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(13, GPIO.FALLING, callback=PushButtonEtapa, bouncetime=700)
except RuntimeError as error:
    print('Erro na função de desligamento e liberar login', error.args[0])
    capture_exception(error)
except Exception as error:
    capture_exception(error)
    print('Erro na função de desligamento e liberar login', error.args[0])


def iniciaSHT():
    try:
        #Humidify SHT31
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_sht31d.SHT31D(i2c)
        time.sleep(3.0) #para dar tempo de inicializar
        print("\033[1mSensor\033[0m = SHT31-D")
        print("\033[1mSerial Number\033[0m = ", sensor.serial_number, "\n")
        #sensor.repeatability = adafruit_sht31d.REP_LOW
        sensor.repeatability = adafruit_sht31d.REP_MED
        #sensor.repeatability = adafruit_sht31d.REP_HIGH
        #sensor.clock_stretching = True
        # (SEGUNDA FORMA) - PARA ACESSAR O SHT31 SEM O ADAFRUIT
        # Start the i2c bus and label as 'bus'
        #bus = smbus.SMBus(1)
        # Endereço
        #bus.write_i2c_block_data(0x44, 0x2C, [0x06])
        # Read the data from the SHT31 containing
        # the temperature (16-bits + CRC) and humidity (16bits + crc)
        #dataSHT = bus.read_i2c_block_data(0x44, 0x00, 6)
        return sensor
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print('Sensor umidade erro26', error.args[0])
        set_display_umid('er26')
        time.sleep(2)
        capture_message('erro sensor sht 26')
        return False
    except Exception as error:
        print('Sensor umidade erro2', error)
        capture_message('erro sensor sht 2')
        set_display_umid('err2')
        return False


def aciona_flap(comando, tempo):
    print('acionando flap', comando, tempo)
    try:
        tempo = tempo * 2
        if comando == 'fechar':
            GPIO.output(7, True)
            GPIO.output(20, True)
            GPIO.output(18, False)
            print('fechando')
            time.sleep(tempo)
            GPIO.output(7, False)
            GPIO.output(20, False)
            print('fechou')
        elif comando == 'abrir':
            GPIO.output(18, True)
            GPIO.output(20, True)
            GPIO.output(7, False)
            print('abrindo')
            time.sleep(tempo)
            GPIO.output(18, False)
            GPIO.output(20, False)
            print('abriu')
    except Exception as error:
        capture_exception(error)
        print('erro no acionamento do flap status')


global flap_status #0 quer dizer no meio -10 aberto e +10 fechad0
flap_status = 6

global pid
pid = PID(0.1, 0.1, 0.1, setpoint=50) 
pid.output_limits = (0, 6) 

def controleFlap(umid, setpoint):

    global pid
    pid.setpoint = setpoint #valor que deseja alcançar configGeral.temp
    controle = pid(umid) 
    #Umidade baixa (6) (fechado)
    #umidade alta (0) (aberto)
    global flap_status

    correcao = flap_status-int(controle)

    flap_status = int(controle)

    print('controle pid:', controle, 'flap status:', flap_status, 'correção', correcao)

    if correcao < 0: #retorno menor que zero é para fechar
        if flap_status == 0:
            aciona_flap('fechar', -(correcao-2))
        else:
            aciona_flap('fechar', -correcao)
    elif correcao > 0: #retorno maior que zero é para abrir
        if flap_status == 6:
            aciona_flap('abrir', correcao+2)
        else:
            aciona_flap('abrir', correcao)
     

def main():
    global DS18B20status
    device_file = iniciaSensorTemp()

    global SHTstatus
    time.sleep(3)
    try:
        sensor = iniciaSHT()
        SHTstatus = True
    except Exception as error:
        print('err25', error)
        SHTstatus = False

    global configFaixa
    global configGeral
    global contadorTemp
    global contador_mudo_speak
    global contador_click
    try:
        configGeral = service.getLocalConfigGeral(bd_conf)
        configFaixa = service.getLocalConfigFaixa(bd_conf)
        print('print geral', configGeral.speaker)
        verificaLedEtapa(configFaixa.etapa)
        contadorTemp = configGeral.intervalo_seconds/2

        print(str(SHTstatus))
        speaker_alerta(True, configGeral.speaker, contador_mudo_speak)
        time.sleep(0.2)
        speaker_alerta(False, configGeral.speaker, contador_mudo_speak)
        time.sleep(0.7)
        speaker_alerta(True, configGeral.speaker, contador_mudo_speak)
        time.sleep(0.3)
        speaker_alerta(False, configGeral.speaker, contador_mudo_speak)
        time.sleep(1.0)
    except Exception as error :
        capture_exception(error)
        print('erro 501', error)
        contadorTemp = 200

    global humidade
    humidade = 0
    global temperatura_fahrenheit
    temperatura_fahrenheit = 0
    global temperaturaSHT_fahrenheit
    temperaturaSHT_fahrenheit = 0

    #dhtDevice = adafruit_dht.DHT22(board.D13)

    #variavel utilizada para veirficar como esta setado a configuração
    global vr
    vr = 0
    global vr_flap
    vr_flap = 6
    global oculto
    oculto = 0
    global temperatura_celcius

    global medicoes
    medicoes = []

    humidade = 0
    global alerta_sonoro
    global alerta_vr
    global alerta_sonoro_contador
    alerta_sonoro_contador = 0
    global temperature_DS18B20
    global motor_fornalha_cont
    motor_fornalha_cont = 0
    global motor_fornalha_status
    motor_fornalha_status = False
    # Proporcional, 
    # integral: tempo para alcançar o valor de set point, 
    # Derivativa

    try:
        print('carregando sensor de temperatura', DS18B20status)
        if DS18B20status:
            temperature_DS18B20 = read_temp(device_file)
            print('depois de carregado')
            temperatura_celcius = temperature_DS18B20[0]
            temperatura_fahrenheit = temperature_DS18B20[1]
            set_display_temp(temperature_DS18B20[1], configGeral.escala_temp)
    except RuntimeError as error:
        print('Sensor temperatura erro4', error.args[0])
        capture_exception(error)
        set_display_temp('err4', 'T')
        time.sleep(2)
        temperatura_fahrenheit = 0
        temperatura_celcius = 0
    except Exception as error:
        print('Sensor temperatura erro3', error)
        capture_exception(error)
        set_display_temp('err3', 'T')
        time.sleep(5)
        temperatura_fahrenheit = 0
        temperatura_celcius = 0
        #raise error

    aciona_flap('fechar', 6) #para flap iniciar fechado

    while True:
        hora = datetime.now()

        #print(hora.hour, hora.minute)
        if desligar == 1:
            display_temp.write([0, 0, 0, 0])
            display_humid.write([0, 0, 0, 0])
            break
        alerta_sonoro = 0
        alerta_vr = 0

        #SENSOR DE TEMPERATURA DS18B20
        #https://labprototipando.com.br/2020/06/22/como-utilizar-o-sensor-de-temperatura-ds18b20-no-raspberry-pi/
        if DS18B20status:
            try:
                temperature_DS18B20 = read_temp(device_file)
                print(
                    "DS18B20: Temp: {:.1f} F / {:.1f} C".format(
                        temperature_DS18B20[1],
                        temperature_DS18B20[0],
                    )
                )
                temperatura_celcius = round(temperature_DS18B20[0],1)
                temperatura_fahrenheit = round(temperature_DS18B20[1],1)
                set_display_temp(temperature_DS18B20[1], configGeral.escala_temp)
            except RuntimeError as error:
                capture_message('erro sensor DS18B20 5')
                print('Sensor temperatura erro5', error.args[0])
                set_display_temp('err5', 'T')
                time.sleep(2)
                temperatura_fahrenheit = 0
                temperatura_celcius = 0
            except Exception as error:
                capture_message('erro sensor DS18B20 6')
                print('Sensor temperatura erro6', error)
                set_display_temp('err6', 'T')
                time.sleep(5)
                temperatura_fahrenheit = 0
                temperatura_celcius = 0
                DS18B20status = False
        print('707 valor de alerta vr', alerta_vr)
        if sensor:
            #SENSOR SHT31
            try:
                # https://github.com/adafruit/Adafruit_CircuitPython_SHT31D/blob/master/examples/sht31d_periodic_mode.py
                #print("\033[1mHumidity:\033[0m ", sensor.relative_humidity, "\n")
                #print("\033[1mTemperature:\033[0m ", sensor.temperature)
                #para utilizar sem o adafruit
                #tempSHT = dataSHT[0] * 256 + dataSHT[1]
                #tempSHT_c = round(float(-45 + (175 * tempSHT / 65535.0)),2)
                #humiditySHT = round(float(100 * (dataSHT[3] * 256 + dataSHT[4]) / 65535.0),2)

                print(
                    "SHT31:    Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                        round(float(sensor.temperature * (9 / 5) + 32),2),
                        sensor.temperature,
                        sensor.relative_humidity
                    )
                )
                temperaturaSHT_fahrenheit = round(float(sensor.temperature * (9 / 5) + 32),2)
                humidade = round(sensor.relative_humidity,1)
                #display_humid.show(str('U '+str(int(sensor.relative_humidity))))
                set_display_umid(int(sensor.relative_humidity))
            except RuntimeError as error:
                capture_message('erro sensor sht 5')
                print('erro5', error.args[0])
                set_display_umid('err5')
                humidade = 0
                time.sleep(5)
            except Exception as error:
                capture_message('erro sensor sht 6')
                print('erro6', error)
                set_display_umid('err6')
                time.sleep(5)
                humidade = 0

        if configFaixa.etapa != 'Padrão': 
            alerta_vr = service.verificarAlerta(temperatura_fahrenheit, humidade, configFaixa, bd_umid, configGeral)#ok = 0, TA =11, TB=12, HA=33, HB=36, TA+HA=44, TA+HB=47, TB+HA=45, TB+HB=48
        else:
            alerta_vr = 0
        print('746 valor de alerta vr', alerta_vr)

        #calculando média
        m = Medicao(float(temperatura_fahrenheit), float(humidade), float(temperaturaSHT_fahrenheit))
        medicoes = calc.array_medicoes(medicoes, m )


        # pid
        # FALTA DENSEVOLER, PENDENTE
        # DESENVOLVER UM SISTEMA PARA ALTERAR O FLAP PARA MANUAL
        vr_flap += 1
        if vr_flap > 9:
            vr_flap = 0
            if int(humidade) > 0:
                controleFlap(float(humidade), configFaixa.umid_max )



        #armazenando no BD
        try:
            if contadorTemp > configGeral.intervalo_seconds :
                contadorTemp = 0
                if humidade != 0 or temperatura_celcius != 0:
                    try:
                        med = calc.get_media(medicoes)
                        service.add_medicao(med.temperatura,
                                    med.temperatura2,
                                    med.umidade,
                                    oculto,
                                    alerta_vr,
                                    0,
                                    motor_fornalha_status,
                                    bd)

                        #regra para utilizar na consulta de muitas medicoes
                        oculto = oculto+1
                        if oculto > 8 :
                            oculto = 0
                    except RuntimeError as error:
                        capture_exception(error)
                        print('erro12', error.args[0])
                        time.sleep(5)
                    except Exception as error:
                        capture_exception(error)
                        print('erro23', error)
                        time.sleep(5)
            else:
                contadorTemp += 4
        except Exception as error:
            capture_exception(error)
            print('erro no vr para armazenar no bd', error)
            time.sleep(1)
        #uma regra para não precisar verificar se a configuração foi alterada toda vez

   
        #Atualizando tabela de tempo real
        service.updt_medicao(temperatura_fahrenheit, temperaturaSHT_fahrenheit,
                    humidade,
                    alerta_vr,
                    0,
                    motor_fornalha_status,
                    bd)
        print('valor de alerta vr', alerta_vr)
        try:
            sio.emit('medicao', {'motor_status': motor_fornalha_status, 'temperatura': temperatura_fahrenheit, 'temperatura2': temperaturaSHT_fahrenheit, 'umidade': humidade, 'alerta': alerta_vr, 'updated': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})
        except Exception as error:
            capture_exception(error)
            print('erro socket:', e)

        #verificador de inicialização dos sensores
        try:
            if vr % 2 == 0:
                if not DS18B20status:
                    device_file = iniciaSensorTemp()
                #if not SHTstatus:
                if not sensor:
                    try:
                        sensor = iniciaSHT()
                        SHTstatus = True
                    except Exception as error:
                        capture_message('sensor umidade não iniciado')
                        SHTstatus = False
                        set_display_temp('er27', 'T')
        except Exception as error:
            capture_exception(error)
            print('erro no  if vr % 2 == 0:', error)
        #if configFaixa.expiration < str(datetime.now()) :
        #    print('implementar lógica para pular etapa pq expirou')

        if not vr % 2: #para verificar o motor a cada 12s
            alerta_vr = service.verificarAlerta(temperatura_fahrenheit, humidade, configFaixa, bd_umid, configGeral)#ok = 0, TA =11, TB=12, HA=33, HB=36, TA+HA=44, TA+HB=47, TB+HA=45, TB+HB=48
            if temperatura_fahrenheit > 0:
                if temperatura_fahrenheit < configFaixa.temp_min - 1:
                    motor_fornalha_cont += 1
                    if motor_fornalha_cont > 3: #almentar para 3
                        if motor_fornalha_status == False:
                            motor_fornalha_status = True
                            print('-----------------ligar motor ventoinha')
                            motor_fornalha_acionamento(motor_fornalha_status, 1)
                else:
                    motor_fornalha_cont = 0
                    motor_fornalha_status = False
                    print('desligar motor ventoinha')
                    motor_fornalha_acionamento(motor_fornalha_status, 1)

        #em produção trocar para 10min
        if contador_mudo_speak > 0:
            contador_mudo_speak -= 1
        if alerta_vr > 0 and configFaixa.updated < str(datetime.now() - timedelta(minutes=1)):
            if alerta_sonoro_contador > 3:
                contador = 0
                while (contador < 3):
                    contador += 1
                    speaker_alerta(True, configGeral.speaker, contador_mudo_speak)
                    time.sleep(1.4)
                    if alerta_vr == 11 or alerta_vr == 44 or alerta_vr == 47: #temp alta
                        set_display_temp(str('----'), 'T')
                        speaker_alerta(False, configGeral.speaker, contador_mudo_speak)
                    elif alerta_vr == 12 or alerta_vr == 45 or alerta_vr == 48: #temp baixa
                        set_display_temp(str('-   '), 'T')
                        speaker_alerta(False, configGeral.speaker, contador_mudo_speak)
                    if alerta_vr == 33 or alerta_vr == 44 or alerta_vr == 45: #umid alta
                        set_display_umid(str('----'))
                        #speaker_alerta(False, configGeral.speaker, contador_mudo_speak)
                    elif alerta_vr == 36 or alerta_vr == 47 or alerta_vr == 48:  # umid baixa
                        set_display_umid(str('-   '))
                        #speaker_alerta(False, configGeral.speaker, contador_mudo_speak)
                    time.sleep(0.6)
                    if sensor:
                        set_display_umid(int(sensor.relative_humidity))
                    if DS18B20status:    
                        set_display_temp(temperature_DS18B20[1], configGeral.escala_temp)

            else:
                time.sleep(4)
            alerta_sonoro_contador += 1
            configGeral = service.getLocalConfigGeral(bd_conf)
            configFaixa = service.getLocalConfigFaixa(bd_conf)
            vr = vr+1
            if vr > 5 :
                vr = 0
        else:
            alerta_sonoro_contador = 0
            vr = vr+1
            if vr % 2:
                configGeral = service.getLocalConfigGeral(bd_conf)
                configFaixa = service.getLocalConfigFaixa(bd_conf)

            if vr > 5 :
                vr = 0
            time.sleep(4)

        contador_click = 0
        set_led_run(vr % 2)






##sensor de temperatura ds18b20
def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return round(temp_c,1), round(temp_f,1)




if __name__ == '__main__':
    try:
        main()   
        display_temp.write([0, 0, 0, 0])
        display_humid.write([0, 0, 0, 0])
        GPIO.output(26, False)
    except RuntimeError as error:
        capture_exception(error)
        print('erro66', error.args[0])
        print('atribuindo')
        time.sleep(5)
        GPIO.output(7, False)  # flap comando
        GPIO.output(18, False)  # flap comando
    except Exception as error:
        capture_exception(error)
        print('erro67', error)
        GPIO.output(26, False)
        GPIO.output(28, False)
        GPIO.cleanup() #testar melhor
        time.sleep(2)
        main()



# https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
