#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sakshat import SAKSHAT
import time
import os
import socket, fcntl, struct

SAKS = SAKSHAT()


#另一种方法, 只需要指定网卡接口, 我更倾向于这个方法
def get_ip2(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
t = 0
if __name__ == '__main__':
    ip = str(get_ip2('wlan0')).split('.')
    while True:
        t = ip[3] if t == ip[2] else ip[2]
        SAKS.digital_display.show(int(t))
        if t > 50:
            pass
            # SAKS.buzzer.beepAction(0.02,0.02,30)
        time.sleep(2)

    input("Enter any keys to exit...")
