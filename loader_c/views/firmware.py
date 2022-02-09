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



def atualizar_firmware():
    import subprocess
    try:
        subprocess.run(["sudo", "python3", "/etc/loader/loader/atualiza.py"])
        return 1
    except Exception as e :
        capture_message('atualizar_firmware 89')
        capture_exception(e)
        return 0

def rollback_atualizar(v):
    from datetime import datetime
    import subprocess
    try:
        subprocess.run(["sudo", "python3", "/etc/loader/loader/rollback_updt.py"])
        now = datetime.now()
        arquivo = open('/etc/loader/loader/version.conf', 'w')
        arquivo.write(v - 0.1)
        arquivo.close()
        return 1
    except Exception as e :
        capture_exception(e)
        return 0