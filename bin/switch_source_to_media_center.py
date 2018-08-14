#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# switch_source_to_raspi.py

import datetime
import subprocess
import time

CODE_SOURCE_RASPI = 'SA-CD/CD'
CODE_SOURCE_CATV = 'SAT/CATV'
REMOTE_NAME = 'RM-AAU190'


def irsend(remote_code, remote_name=REMOTE_NAME, count=None):
    cmd = ['/usr/bin/irsend', 'SEND_ONCE', remote_name, remote_code]
    if count is not None:
        count_decimal = int(count)
        cmd.insert(1, '--count=%d' % count_decimal)

    print(datetime.datetime.now(), end=" -- ")
    print(cmd)
    subprocess.run(cmd)


def power_on_switch_to_raspi():
    time.sleep(0.01)
    irsend(CODE_SOURCE_CATV)


if __name__ == '__main__':
    power_on_switch_to_raspi()
