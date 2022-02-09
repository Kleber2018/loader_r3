import sqlite3
def criandoSQLiteMedicao(b):
     try:
          con = sqlite3.connect(b)
          print('criando o BD')
          cursor = con.cursor()
          cursor.execute('''CREATE TABLE medicoes (id_medicao integer PRIMARY KEY AUTOINCREMENT NOT NULL, motor_status integer, flap_status integer, temperatura real, temperatura2 real, umidade real, oculto integer, alerta integer, status integer, created DATE DEFAULT (datetime('now','localtime')) NOT NULL)''')
          cursor.execute(
               '''CREATE TABLE medicao (id_medicao integer PRIMARY KEY AUTOINCREMENT NOT NULL, motor_status integer, flap_status integer, temperatura real, temperatura2 real, umidade real, alerta integer, updated DATE DEFAULT (datetime('now','localtime')) NOT NULL)''')
          cursor.execute("INSERT INTO medicao (temperatura, temperatura2, umidade, alerta, motor_status, flap_status) VALUES (0, 0, 0, 0, 0, 0)")
          con.commit()
          con.close()
     except Exception as e:
          print('Erro consultar BD getLocalConfigFaixa', e)

def criandoSQLiteConf(b):
     try:
          con = sqlite3.connect(b)
          print('criando o BD')
          cursor = con.cursor()
          cursor.execute('''CREATE TABLE usuario (login text, senha text, nome text, telefone text, email text, privilegios text)''')
          cursor.execute("INSERT INTO usuario VALUES ('montabaco', '4444', 'Montabaco','333333', 't@t.com', 'adm')")

          cursor.execute('''CREATE TABLE config (id_config integer PRIMARY KEY AUTOINCREMENT NOT NULL, flap_auto integer, flap_posicao integer, flap_seconds integer, nome text, etapa text, intervalo_seconds integer , temp_min real , temp_max real, umid_ajuste integer, escala_temp text, obs text, alerta_desat text, speaker integer, status integer, updated DATE DEFAULT (datetime('now','localtime')) NOT NULL, expiration DATE DEFAULT (datetime('now','localtime')) NOT NULL)''')
          cursor.execute("INSERT INTO config (flap_auto, flap_posicao, flap_seconds, nome, etapa, intervalo_seconds, temp_min, temp_max, umid_ajuste, escala_temp, alerta_desat, speaker, status, obs) "
                         "VALUES (1, 6, 2, 'Estufa 1', 'Padrão', 500, 90.0, 100.0, 1, 'F', 0, 0, 0, 'Configuração padrão')")

          cursor.execute(
              '''CREATE TABLE etapa (id_etapa integer PRIMARY KEY AUTOINCREMENT NOT NULL, etapa text, intervalo_seconds integer , temp_min real , temp_max real, umid_min real , umid_max real, umid_ajuste integer, escala_temp text, obs text, alerta_desat text, speaker integer, status integer, updated DATE DEFAULT (datetime('now','localtime')) NOT NULL, expiration DATE DEFAULT (datetime('now','localtime')) NOT NULL)''')
          cursor.execute(
              "INSERT INTO etapa (etapa, intervalo_seconds, temp_min, temp_max, umid_min, umid_max, umid_ajuste, escala_temp, alerta_desat, speaker, status, obs) "
              "VALUES ('Amarelação', 200, 90.0, 100.0, 83, 98, 1, 'F', 0, 0, 0, 'Configuração padrão')")
          cursor.execute(
              "INSERT INTO etapa (etapa, intervalo_seconds, temp_min, temp_max, umid_min, umid_max, umid_ajuste, escala_temp, alerta_desat, speaker, status, obs) "
              "VALUES ('Murchamento', 200, 101.0, 120.0, 45, 81, 1, 'F', 0, 0, 0, 'Configuração padrão')")
          cursor.execute(
              "INSERT INTO etapa (etapa, intervalo_seconds, temp_min, temp_max, umid_min, umid_max, umid_ajuste, escala_temp, alerta_desat, speaker, status, obs) "
              "VALUES ('Secagem da Lâmina', 200, 121.0, 140.0, 25, 44, 1, 'F', 0, 0, 0, 'Configuração padrão')")
          cursor.execute(
              "INSERT INTO etapa (etapa, intervalo_seconds, temp_min, temp_max, umid_min, umid_max, umid_ajuste, escala_temp, alerta_desat, speaker, status, obs) "
              "VALUES ('Secagem do Talo', 200, 141.0, 165.0, 10, 25, 1, 'F', 0, 0, 0, 'Configuração padrão')")
          cursor.execute(
              "INSERT INTO etapa (etapa, intervalo_seconds, temp_min, temp_max, umid_min, umid_max, umid_ajuste, escala_temp, alerta_desat, speaker, status, obs) "
              "VALUES ('Personalizada', 200, 67.2, 90.0, 50, 90, 1, 'F', 0, 0, 1, 'Configuração padrão')")
          
          con.commit()
          con.close()
     except Exception as e:
          print('Erro consultar BD criandoSQLiteConf', e)


def criandoSQLiteMonitorSys(b):
     try:
          con = sqlite3.connect(b)
          print('criando o BD Monitor')
          cursor = con.cursor()
          cursor.execute('''CREATE TABLE monitor (id_monitor integer PRIMARY KEY AUTOINCREMENT NOT NULL, temperatura real, serie string, created DATE DEFAULT (datetime('now','localtime')) NOT NULL)''')
          cursor.execute("INSERT INTO monitor (temperatura, serie) VALUES (0, 'teste')")
          con.commit()
          con.close()
     except Exception as e:
          print('Erro criar monitor', e)

def criandoSQLiteTabUmidade(b):
    try:
        con = sqlite3.connect(b)
        print('criando o BD')
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE umidade (id_umidade integer PRIMARY KEY AUTOINCREMENT NOT NULL, temperatura integer, umidade integer, etapa text)''')
        cursor.execute('''CREATE TABLE umidade (id_umidade integer PRIMARY KEY AUTOINCREMENT NOT NULL, temperatura integer, umidade integer, etapa text)''')
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 55, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 56, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 57, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 58, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 59, 98, 'Teste')")

        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 60, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 61, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 62, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 63, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 64, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 65, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 66, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 67, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 68, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 69, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 70, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 71, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 72, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 73, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 74, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 75, 98, 'Teste')")

        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 76, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 77, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 78, 98, 'Teste')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 79, 98, 'Teste')")

        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 80, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 81, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 82, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 83, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 84, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 85, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 86, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 87, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 88, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 89, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 90, 98, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 91, 96, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 92, 94, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 93, 92, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 94, 91, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 95, 90, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 96, 89, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 97, 88, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 98, 86, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 99, 83, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 100, 81, 'Amarelação')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 101, 79, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 102, 78, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 103, 77, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 104, 75, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 105, 73, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 106, 71, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 107, 69, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 108, 66, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 109, 64, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 110, 63, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 111, 62, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 112, 58, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 113, 56, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 114, 54, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 115, 53, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 116, 51, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 117, 50, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 118, 48, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 119, 46, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 120, 45, 'Murchamento')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 121, 44, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 122, 43, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 123, 41, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 124, 40, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 125, 39, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 126, 37, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 127, 35, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 128, 34, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 129, 33, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 130, 32, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 131, 31, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 132, 31, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 133, 30, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 134, 29, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 135, 28, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 136, 28, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 137, 27, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 138, 26, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 139, 26, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 140, 25, 'Secagem da Lâmina')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 141, 25, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 142, 25, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 143, 24, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 144, 24, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 145, 23, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 146, 23, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 147, 23, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 148, 22, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 149, 22, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 150, 20, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 151, 19, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 152, 18, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 153, 17, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 154, 16, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 155, 15, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 156, 14, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 157, 13, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 158, 12, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 159, 11, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 160, 11, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 161, 11, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 162, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 163, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 164, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 165, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 166, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 167, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 168, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 169, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 170, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 171, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 172, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 173, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 174, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 175, 10, 'Secagem do Talo')")

        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 176, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 177, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 178, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 179, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 180, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 181, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 182, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 183, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 184, 10, 'Secagem do Talo')")
        cursor.execute("INSERT INTO umidade (temperatura, umidade, etapa) VALUES ( 185, 10, 'Secagem do Talo')")
        con.commit()
        con.close()
    except Exception as error:
        print('ERRO NA TABELA DE UMIDADE CRIAÇÃO',error)

# def getLocalConfig():
#     try:
#         #intervalo_seconds, temp_min, temp_max, umid_min, umid_max, escala_temp
#
#         arquivo = open('parametros.conf', 'r')
#         #for linha in arquivo:
#         #    print('if', linha)
#         intervalo_seconds = arquivo.readline()
#         temp_min = arquivo.readline()
#         temp_max = arquivo.readline()
#         umid_min = arquivo.readline()
#         umid_max = arquivo.readline()
#         escala_temp = arquivo.readline()
#         configBusca = Config(int(intervalo_seconds), float(temp_min), float(temp_max), float(umid_min), float(umid_max), escala_temp)
#         arquivo.close()
#         return configBusca
#     except Exception as error:
#         arquivo2 = open('parametros.conf', 'w')
#         arquivo2.write('365')
#         arquivo2.write("\n")
#         arquivo2.write('60')
#         arquivo2.write("\n")
#         arquivo2.write('140')
#         arquivo2.write("\n")
#         arquivo2.write('10')
#         arquivo2.write("\n")
#         arquivo2.write('90')
#         arquivo2.write("\n")
#         arquivo2.write('F')
#         arquivo2.write("\n")
#         arquivo2.close()
#         configPadrao = Config(int(60), float(60), float(140), float(10),
#                              float(90), 'F')
#         return configPadrao
#         print('Erro ao buscar a configuração local', error.args[0])

# #busca configurações de alerta setadas