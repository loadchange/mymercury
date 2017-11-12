#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sakshat import SAKSHAT
import time
import urllib2
import json
import pygame
import os

# Declare the SAKS Board
SAKS = SAKSHAT()

__dp = True
__alarm_beep_status = False
__alarm_beep_times = 0
# 在这里设定闹钟定时时间
__alarm_time = "07:10:00"


# 在检测到轻触开关触发时自动执行此函数
def tact_event_handler(pin, status):
    '''
    called while the status of tacts changed
    :param pin: pin number which stauts of tact is changed
    :param status: current status
    :return: void
    '''
    print pin, status
    global __alarm_beep_status
    global __alarm_beep_times
    # 停止闹钟响铃（按下任何轻触开关均可触发）
    __alarm_beep_status = False
    __alarm_beep_times = 0
    SAKS.buzzer.off()
    SAKS.ledrow.off_for_index(6)


def getWeatherData():
    weather_url = 'https://free-api.heweather.com/x3/weather?cityid=CN101010400&key=e2dfc339a09c4e09b1e389e9578af294'
    req = urllib2.Request(weather_url)
    resp = urllib2.urlopen(req)
    content = resp.read()
    if content:
        weatherJSON = json.JSONDecoder().decode(content)
        print(content)
        try:
            if weatherJSON['HeWeather data service 3.0'][0]['status'] == "ok":
                return weatherJSON['HeWeather data service 3.0'][0]
            else:
                return -1
        except Exception as e:
            print e.message
            return -1


if __name__ == "__main__":
    # 设定轻触开关回调函数
    SAKS.tact_event_handler = tact_event_handler
    SAKS.buzzer.off()
    SAKS.ledrow.off_for_index(6)
    mm = 20
    tellTime = False
    while True:
        # 以下代码获取系统时间、时、分、秒、星期的数值
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec
        w = time.strftime('%w', t)
        # print h,m,s,w
        print "%02d:%02d:%02d" % (h, m, s)

        if 21 >= h >= 7 and m == 59 and s >= 58 and not tellTime:
            tellTime = True
            path = "%s/saksha/tell-time/%d.mp3" % (os.path.abspath('.'), m % 10)
            pygame.mixer.init()
            pygame.mixer.music.set_volume(1.0)
            track = pygame.mixer.music.load(path)
            pygame.mixer.music.play()

        if tellTime and not pygame.mixer.music.isplaying():
            tellTime = False
            pygame.mixer.quit()

        if ("%02d:%02d:%02d" % (h, m, s)) == __alarm_time:
            __alarm_beep_status = True
            __alarm_beep_times = 0

        # leds = s % 10
        # if h > 21 or (0 < h < 7):
        #     if leds >= 8:
        #         SAKS.ledrow.off()
        #     else:
        #         SAKS.ledrow.on_for_index(leds)
        # else:
        #     SAKS.ledrow.off()

        # if mm == 20:
        #     mm = 1
        #     weather = getWeatherData()
        #     pm10 = weather['aqi']['city']['pm10']  # 67
        #     pm25 = weather['aqi']['city']['pm25']  # 5
        #     qlty = weather['aqi']['city']['qlty']  # 良
        #     suggestion = ''
        #     for key in ['air', 'comf', 'cw', 'drsg', 'flu', 'sport', 'trav', 'uv']:
        #         suggestion += weather['suggestion'][key]['txt']
        #     print pm10, pm25, qlty, suggestion

        if __dp:
            # 数码管显示小时和分，最后一位的小点每秒闪烁一次
            SAKS.digital_display.show(("%02d%02d." % (h, m)))
            # 判断是否应该响起闹钟
            if __alarm_beep_status:
                SAKS.buzzer.on()
                SAKS.ledrow.on_for_index(6)
                __alarm_beep_times = __alarm_beep_times + 1
                # 30次没按下停止键则自动停止闹铃
                if __alarm_beep_times > 30:
                    SAKS.buzzer.off()
                    __alarm_beep_status = False
                    __alarm_beep_times = 0
        else:
            SAKS.digital_display.show(("%02d%02d" % (h, m)))
            if __alarm_beep_status:
                SAKS.buzzer.off()
                SAKS.ledrow.off_for_index(6)
        __dp = not __dp

        time.sleep(0.5)
    input("Enter any keys to exit...")
