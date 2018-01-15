# coding: utf-8
import time
import RPi.GPIO as gpio
import atexit

servopin = 17
atexit.register(gpio.cleanup)
gpio.setmode(gpio.BCM)
gpio.setup(servopin, gpio.OUT, initial=False)
p = gpio.PWM(servopin, 50)
p.start(0)
time.sleep(0.6)

servo_down = 3.8
servo_up = 5


def press(tms):
    p.ChangeDutyCycle(servo_down)
    time.sleep(0.02)
    p.ChangeDutyCycle(0)
    time.sleep(tms)
    p.ChangeDutyCycle(servo_up)
    time.sleep(0.02)
    p.ChangeDutyCycle(0)
    time.sleep(1)


if __name__ == '__main__':
    while True:
        print '>' * 50
        press(float(1200) / 1000)
