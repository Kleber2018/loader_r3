import sqlite3
from views import service
from views import bdnew
import time

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

def getLocalConfigFaixa(bd):
    try:
        #global configFaixa
        con = sqlite3.connect(bd)
        cursor = con.cursor()
        cursor.execute(
            "SELECT  temp_min, temp_max, umid_ajuste, etapa, updated, expiration, umid_min, umid_max FROM etapa WHERE status = 1")

        rows = cursor.fetchall()
        if len(rows) > 0:
            con.close()
            return ConfigFaixa(float(rows[0][0]), float(rows[0][1]), int(rows[0][2]), rows[0][3], rows[0][4], rows[0][5], rows[0][6], rows[0][7])
        else:
            cursor.execute(
                "SELECT  temp_min, temp_max, umid_ajuste, etapa, updated, expiration, umid_min, umid_max FROM etapa WHERE id_config = 5;")
            rows = cursor.fetchall()   
            cursor.execute("UPDATE config SET status = 1 WHERE id_config = 5;") 
            con.close()
            return ConfigFaixa(float(rows[0][0]), float(rows[0][1]), int(rows[0][2]), rows[0][3], rows[0][4], rows[0][5], rows[0][6], rows[0][7])
    except Exception as e:
        print('Erro consultar BD getLocalConfigFaixa', e)
        time.sleep(2)
        return False


#criandoSQLiteTabUmidade(bd_umid)

def getLocalConfigGeral(bd):
    try:
        con = sqlite3.connect(bd)
        cursor = con.cursor()
        cursor.execute(
            "SELECT  intervalo_seconds, umid_ajuste, escala_temp, alerta_desat, speaker, etapa FROM config WHERE id_config = '1'")
        rows = cursor.fetchall()
        if len(rows) > 0:
            con.close()
            return ConfigGeral(int(rows[0][0]), int(rows[0][1]), rows[0][2], rows[0][3], rows[0][4], rows[0][5])
        else:
            bdnew.criandoSQLiteConf(bd)
            return False
    except Exception as e:
        print('Erro consultar BD getLocalConfigGeral', e)
        bdnew.criandoSQLiteConf(bd)
        time.sleep(2)
        return False

#habilitar depois de trocar a central da estufa de triunfo
def add_medicao2(temperatura, temperatura_sht, umidade, numoculto, alerta, flap_status, motor_status, bd):
    try:
        motor = 0
        if motor_status:
            motor = 1        
    except Exception as error:
        motor = 0

    """Adds the given contact to the contacts table"""
    try:
        con = sqlite3.connect(bd)
        print('adicionando medição')
        cursor = con.cursor()
        cursor.execute("INSERT INTO medicoes (temperatura, temperatura2, umidade, oculto, alerta, status, flap_status, motor_status) VALUES (?, ?, ?, ?, ?, 0, ?, ?);", (temperatura, temperatura_sht, umidade, numoculto, alerta, flap_status, motor))
        con.commit()
        con.close()
    except Exception as error:
        print(f"erro ao adicionar medicao em medições: {error}")
        bdnew.criandoSQLiteMedicao(bd)

def add_medicao(temperatura, temperatura_sht, umidade, numoculto, alerta, flap_status, motor_status, bd):
    try:
        motor = 0
        if motor_status:
            motor = 1        
    except Exception as error:
        motor = 0

    """Adds the given contact to the contacts table"""
    try:
        con = sqlite3.connect(bd)
        print('adicionando medição')
        cursor = con.cursor()
        cursor.execute("INSERT INTO medicoes (temperatura, temperatura2, umidade, oculto, alerta, status) VALUES (?, ?, ?, ?, ?, 0);", (temperatura, temperatura_sht, umidade, numoculto, alerta))
        con.commit()
        con.close()
    except Exception as error:
        print(f"erro ao adicionar medicao em medições: {error}")
        bdnew.criandoSQLiteMedicao(bd)

#habilitar depois de trocar a central da estufa de triunfo
def updt_medicao(temperatura, temperatura_sht, umidade, alerta, flap_status, motor_status, bd):
    try:
        motor = 0
        if motor_status:
            motor = 1        
    except Exception as error:
        motor = 0
    """Adds the given contact to the contacts table"""
    try:
        con = sqlite3.connect(bd)
        cursor = con.cursor()
        cursor.execute("UPDATE medicao SET temperatura = ?, temperatura2 = ?, umidade = ?, alerta = ?, flap_status = ?, motor_status = ?, updated = datetime('now', 'localtime') WHERE id_medicao = 1;",
                       (temperatura, temperatura_sht, umidade, alerta, flap_status, motor))
        con.commit()
        con.close()
    except Exception as error:
        print(f"erro ao atualizar medicao: {error}")
        bdnew.criandoSQLiteMedicao(bd)

def updt_medicao2(temperatura, temperatura_sht, umidade, alerta, flap_status, motor_status, bd):
    try:
        motor = 0
        if motor_status:
            motor = 1        
    except Exception as error:
        motor = 0
    """Adds the given contact to the contacts table"""
    try:
        con = sqlite3.connect(bd)
        cursor = con.cursor()
        cursor.execute("UPDATE medicao SET temperatura = ?, temperatura2 = ?, umidade = ?, alerta = ?, updated = datetime('now', 'localtime') WHERE id_medicao = 1;",
                       (temperatura, temperatura_sht, umidade, alerta))
        con.commit()
        con.close()
    except Exception as error:
        print(f"erro ao atualizar medicao: {error}")
        bdnew.criandoSQLiteMedicao(bd)

def verificarAlerta(temperatura, umidade, config, bd_umid, configGeral):
    #ok = 0, TA =11, TB=12, HA=33, HB=36, TA+HA=44, TA+HB=47, TB+HA=45, TB+HB=48
    global r
    r = 0
    if temperatura > 0:
        if temperatura < config.temp_max + 3:
            r = 12 #TB
        elif temperatura > config.temp_min - 3:
            r = 11 #TA
    if umidade > 0:
        if umidade < config.umid_max + 2:
            r = r + 36 #HB
        elif umidade > config.umid_min - 2:
            r = r + 33 #HA
    return r


#para verificar se a temperatura e umidade que está dentro do setpointer de alerta:#ok = 0, temp = 1, umid=3, ambos = 4
def verificarAlerta2(temperatura, umidade, config, bd_umid, configGeral):
    global r
    r = 0
    if temperatura > 0:
        if temperatura > config.temp_max:
            r = 11
        elif temperatura < config.temp_min:
            r = 12
    try:
        con = sqlite3.connect(bd_umid)
        cursor = con.cursor()
        cursor.execute("SELECT umidade FROM umidade WHERE temperatura = ?", (int(temperatura),))
        rows = cursor.fetchall()
        con.close()
        if len(rows) > 0:
            if umidade < rows[0][0] - 2 + configGeral.umid_ajuste:
                #umidade baixa
                r = r + 36
            elif umidade > rows[0][0] + 2 + configGeral.umid_ajuste:
                # umidade alta
                r = r + 33
        else:
            print('nenhum alerta umidade')
    except Exception as error:
        print('ERRO NA TABELA DE UMIDADE busca',error)
    return r


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

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def add_system_monitor(bd_m):
    """Adds the given contact to the contacts table"""
    try:
        con = sqlite3.connect(bd_m)
        print('adicionando medição monitor')
        cursor = con.cursor()
        t_cpu = get_cpu_temp()
        ns = getserial()
        cursor.execute("INSERT INTO monitor (temperatura, serie) VALUES (?, ?);", (t_cpu, ns))
        con.commit()
        con.close()
    except Exception as error:
        print(f"erro ao adicionar monitor: {error}")
        bdnew.criandoSQLiteMonitorSys(bd_m)