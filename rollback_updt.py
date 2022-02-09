#!/usr/bin/env python3

#deixar uma pasta antes da principal

from datetime import datetime, timedelta
import json

import subprocess

def voltar_backup():
    try:
        now = datetime.now()
        print(now.year)
        subprocess.run(["cp", "-fR", "/etc/loader/loader_bkp/loader_a", "/etc/loader/loader"])
        subprocess.run(["cp", "-fR", "/etc/loader/loader_bkp/loader_m", "/etc/loader/loader"])
        subprocess.run(["cp", "-fR", "/etc/loader/loader_bkp/loader_s", "/etc/loader/loader"])
        return 1
    except Exception as e:
        print('erro backup', e)
        return 0


if __name__ == "__main__":
    voltar_backup()
