#!/usr/bin/env python3

from datetime import datetime, timedelta
import os
import time
import subprocess
import git

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

def resetar_fila():
    try:
        print('resetando')
        subprocess.run(["git", "checkout", "--", "."])
        subprocess.run(["git", "clean", "-f", "-d"])
        return 1
    except Exception as e:
        print('erro no git reset', e)
        return 0

def atualizando():
    try:
        capture_message('executou atualização')
        if backup() == 1:
            try:
                subprocess.run(["sudo", "rm", "-f", "/etc/loader/loader/.git/index.lock"])
            except Exception as e:
                capture_exception(e)
            repo = git.Repo('/etc/loader/loader')
            repo.git.reset('--hard')
            repo_heads = repo.heads
            try:
                print(repo_heads)
                repo_heads['master'].checkout()
            except Exception as e:
                capture_exception(e)
            repo.git.reset('--hard')
            repo.git.clean('-xdf')
            repo.remotes.origin.pull()
            print("atualizado")

            time.sleep(10.0)
            subprocess.run(["sudo", "chmod", "-R", "777", "/etc/loader/loader"])
            time.sleep(10.0)
            subprocess.run(["sudo", "reboot"])
        return 1
    except Exception as e:
        capture_exception(e)
        print('erro atualização', e)
        return 0

def clear_bkp():
    try:
        now = datetime.now()
        print(now.year)
        subprocess.run(["sudo", "rm", "-fR", "/etc/loader/loader_bkp"])
        return 1
    except Exception as e:
        print('erro clear_bkp', e)
        return 0

def backup():
    try:
        clear_bkp()
        import time
        time.sleep(5.0)
        now = datetime.now()
        print(now.year)
        subprocess.run(["sudo", "cp", "-fR", "/etc/loader/loader", "/etc/loader/loader_bkp"])
        return 1
    except Exception as e:
        capture_exception(e)
        print('erro backup2', e)
        return 0


if __name__ == "__main__":
    atualizando()
