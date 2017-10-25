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
    print get_ip2('wlan0')
    print get_ip2('lo')
    while True:
        t = 80
        SAKS.digital_display.show("%.2f" % t)
        if t > 50:
            SAKS.buzzer.beepAction(0.02,0.02,30)
        time.sleep(1)

    input("Enter any keys to exit...")
