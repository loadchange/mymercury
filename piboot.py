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

if __name__ == '__main__':
    ip = str(get_ip2('wlan0')).split('.')
    t = 0
    index = 0
    while True:
        if index > len(ip) - 1:
            index = 0
        t = ip[index]
        index++
        t1 = ''
        if len(str(t)) < 4:
            for i in range(4 - len(str(t))):
                t1 += '0'
        t1 += str(t)
        SAKS.digital_display.show(t1)
        if t > 50:
            pass
            # SAKS.buzzer.beepAction(0.02,0.02,30)
        time.sleep(2)

    input("Enter any keys to exit...")
