import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import sqlite3
import os

cur_dir = os.path.dirname(__file__)
db = os.path.join(cur_dir, 'weather.sqlite')
account = os.path.join(cur_dir,'users.sqlite')

def extract_temp_limit(data):
	conn = sqlite3.connect(data)
	c = conn.cursor()
	c.execute("SELECT temperature FROM weather_db WHERE id='1'")
	for row in c.fetchall():
		temp = row[0]
	return temp

def extract_humid_limit(data):
	conn = sqlite3.connect(data)
	c = conn.cursor()
	c.execute("SELECT humidity FROM weather_db WHERE id='1'")
	for row in c.fetchall():
		humid = row[0]
	return humid

sensor = Adafruit_DHT.DHT11

pin = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)

temperature_limit = extract_temp_limit(db)
humidity_limit = extract_humid_limit(db)

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    if (temperature > temperature_limit and humidity > humidity_limit):
        GPIO.output(27,True)
    else:
        GPIO.output(27,False)
else:
    print('Failed to get reading. Try again!')
