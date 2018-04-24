import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib.request

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

myAPI = "CMQWMRWWCAXM0WLG"
myDelay = 15 #how many seconds between posting data

def main():
    
    print ('starting...')

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print (baseURL)
    
    while (True):
        if(GPIO.input(17)):
            light = 1
        else:
            light = 0

        if(GPIO.input(27)):
            fan = 1
        else:
            fan = 0

        f = urllib.request.urlopen(baseURL + "&field1=%s&field2=%s" % (light, fan))
        print (f.read())
        print (light,fan)
        f.close()
        sleep(int(myDelay))

if __name__ == '__main__':
    main()
