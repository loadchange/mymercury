#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sakshat import SAKSHAT
import time
import urllib2
import json
import pygame
import os
from concurrent.futures import ThreadPoolExecutor
from tornado.gen import coroutine, Task
from tornado.web import asynchronous
from tornado.util import raise_exc_info


class RasPi():
    executor = ThreadPoolExecutor(2)

    SAKS = None
    __ldp = True
    __dp = True
    __alarm_beep_status = False
    __alarm_beep_times = 0
    __alarm_time = "07:10:00"  # 在这里设定闹钟定时时间

    tellTime = -1

    def init(self):
        self.SAKS = SAKSHAT()

        # 在检测到轻触开关触发时自动执行此函数
        def tact_event_handler(pin, status):
            print pin, status
            # 停止闹钟响铃（按下任何轻触开关均可触发）
            self.__alarm_beep_status = False
            self.__alarm_beep_times = 0
            self.SAKS.buzzer.off()
            self.SAKS.ledrow.off_for_index(6)

        self.SAKS.tact_event_handler = tact_event_handler
        self.SAKS.buzzer.off()
        self.SAKS.ledrow.off_for_index(6)

    def getWeatherData(self):
        weather_url = 'https://free-api.heweather.com/x3/weather?cityid=CN101010400&key=e2dfc339a09c4e09b1e389e9578af294'
        req = urllib2.Request(weather_url)
        resp = urllib2.urlopen(req)
        content = resp.read()
        if content:
            weatherJSON = json.JSONDecoder().decode(content)
            print(content)
            try:
                if weatherJSON['HeWeather data service 3.0'][0]['status'] == "ok":
                    res = weatherJSON['HeWeather data service 3.0'][0]
                    pm10 = str(res['aqi']['city']['pm10'])  # 67
                    pm25 = str(res['aqi']['city']['pm25'])  # 5
                    qlty = res['aqi']['city']['qlty']  # 良
                    suggestion = ''
                    for key in ['air', 'comf', 'cw', 'drsg', 'flu', 'sport', 'trav', 'uv']:
                        suggestion += res['suggestion'][key]['txt']
                    return "空气指数%s,PM10 %s,PM2.5 %s,%s" % (qlty, pm10, pm25, suggestion)
                else:
                    return None
            except Exception as e:
                print e.message
                return None

    def showLed(self, sec):
        global __ldp
        ledIndex = sec % 8
        if __ldp:
            self.SAKS.ledrow.on_for_index(ledIndex)
            __ldp = not ledIndex
        if not __ldp:
            self.SAKS.ledrow.off()

    def showTime(self):
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec
        w = time.strftime('%w', t)
        # print h,m,s,w
        # print "%02d:%02d:%02d" % (h, m, s)
        if self.__dp:
            self.SAKS.digital_display.show(("%02d%02d." % (h, m)))
            if self.__alarm_beep_status:
                self.SAKS.buzzer.on()
                self.__alarm_beep_times += 1
        else:
            self.SAKS.digital_display.show(("%02d%02d" % (h, m)))
            if self.__alarm_beep_status:
                self.SAKS.buzzer.off()
        self.__dp = not self.__dp
        return {'localtime': t, 'hour': h, 'min': m, 'sec': s, 'strftime': w}

    def playTellTime(self, hours):
        path = "%s/rpi/tell-time/%d.mp3" % (os.path.abspath('.'), hours)
        pygame.mixer.init(frequency=15500, size=-16, channels=4)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        self.tellTime = hours

    def run(self):
        time = self.showTime()
        hour = time.get('hour')
        min = time.get('min')
        sec = time.get('sec')
        if 21 >= hour >= 7 and min == 0 and self.tellTime != hour:
            self.playTellTime(hour)
        if self.tellTime == hour and min == 0 and sec >= 4:
            pygame.mixer.quit()

        if ("%02d:%02d:%02d" % (hour, min, sec)) == self.__alarm_time:
            self.__alarm_beep_status = True
            self.__alarm_beep_times = 0

        if self.__alarm_beep_status and self.__alarm_beep_times > 30:
            self.SAKS.buzzer.off()
            self.__alarm_beep_status = False
            self.__alarm_beep_times = 0

        if hour > 21 or (-1 < hour < 7):
            self.SAKS.ledrow.off()
            [self.SAKS.ledrow.on_for_index(leds) for leds in range(sec % 8)]
        else:
            self.SAKS.ledrow.off()

    def _stack_context_handle_exception(self, type, value, traceback):
        try:
            # For historical reasons _handle_request_exception only takes
            # the exception value instead of the full triple,
            # so re-raise the exception to ensure that it's in
            # sys.exc_info()
            raise_exc_info((type, value, traceback))
        except Exception as e:
            print e.message
            return None
        return True
