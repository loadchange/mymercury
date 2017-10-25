# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

DS = 6
SHCP = 19
STCP = 13

def init():
    GPIO.setup(DS, GPIO.OUT)
    GPIO.setup(SHCP, GPIO.OUT)
    GPIO.setup(STCP, GPIO.OUT)

    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.LOW)

def writeBit(data):
    GPIO.output(DS, data)

    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(SHCP, GPIO.HIGH)

#写入8位LED的状态
def writeByte(data):
    for i in range (0, 8):
        writeBit((data >> i) & 0x01)
    #状态刷新信号
    GPIO.output(STCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.HIGH)

count = 30

try:
    GPIO.cleanup()
    init()
    while not count:
        count -= 1
        #以下一组8个编码由一组二进制转换而成：
        #00000001,00000010,00000100,00001000,00010000,00100000,01000000,10000000
        #分别对应8个LED点亮状态
        for i in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
            writeByte(i)
            time.sleep(0.1)
        #LED组全开
        #writeByte(0xff)
        #time.sleep(0.1)

except KeyboardInterrupt:
    print "except"
    #LED组全关
    writeByte(0x00)
    GPIO.cleanup()
