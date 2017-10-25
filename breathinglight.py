# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(0, GPIO.OUT)
pwm = GPIO.PWM(0, 50)
pwm.start(0)
pause_time = 0.01

try:
    while True:
        for i in xrange(0, 101, 1):
            pwm.ChangeDutyCycle(i)
            # off
            time.sleep(pause_time)

        time.sleep(1)

        for i in xrange(100, -1, -1):
            pwm.ChangeDutyCycle(i)
            # on
            time.sleep(pause_time)

except KeyboardInterrupt:
    # stop the white PWM output
    pwm.stop()
    # clean up GPIO on CTRL+C exit
    GPIO.cleanup()
