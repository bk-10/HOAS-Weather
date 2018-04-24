from flask import Flask, render_template, request, session, abort, redirect, flash
from wtforms import Form, TextAreaField, validators
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import sqlite3
import os
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

cur_dir = os.path.dirname(__file__)
db = os.path.join(cur_dir, 'weather.sqlite')
account = os.path.join(cur_dir,'users.sqlite')

def get_cur_temp(sensor, pin):
	c_humidity, c_temperature = Adafruit_DHT.read_retry(sensor, pin)
	return c_temperature

def get_cur_humid(sensor, pin):
	c_humidity, c_temperature = Adafruit_DHT.read_retry(sensor, pin)
	return c_humidity

def weather_update(data,temp, humid):
	conn = sqlite3.connect(data)
	c = conn.cursor()
	c.execute("UPDATE weather_db SET temperature = ?, humidity  = ? WHERE id = '1'", (temp, humid))
	conn.commit()
	conn.close()

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

def activate_light_system(option):
	p=subprocess.Popen(['python3', 'lighting.py'])
	if(option):
		pj=1
	else:
		p.kill()

def activate_weather_system(option):
	p=subprocess.Popen(['python3', 'weather.py'])
	if(option):
		pj=1
	else:
		p.kill()

def activate_status_update(option):
	p=subprocess.Popen(['python3','home_status.py'])
	if(option):
		pj=1
	else:
		p.kill()

app = Flask(__name__)

class ac_holders(Form):
	username = TextAreaField('',[validators.DataRequired()])
	password = TextAreaField('',[validators.DataRequired()])

class weatherForm(Form):
	temperature = TextAreaField('',[validators.DataRequired()])
	humidity = TextAreaField('',[validators.DataRequired()])

@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('weather.html')

@app.route('/login', methods=['POST'])
def verify():
	form = ac_holders(request.form)
	if request.form['password'] == 'projectiot' and request.form['username'] == 'iot':
		session['logged_in'] = True
		GPIO.output(22,True)
		activate_light_system(True)
		activate_weather_system(True)
		activate_status_update(True)
	else:
		flash('wrong password!')
		return index()
	return home()

@app.route('/home')
def home():
	sensor = Adafruit_DHT.DHT11
	pin = 11
	form = weatherForm(request.form)
	temperature = extract_temp_limit(db)
	humidity = extract_humid_limit(db)
	c_temperature = get_cur_temp(sensor, pin)
	c_humidity = get_cur_humid(sensor, pin)
	return render_template('weather.html', form=form, temperature=temperature, humidity=humidity, c_temperature=c_temperature, c_humidity=c_humidity)

@app.route('/weather', methods=['POST'])
def weather():
	form = weatherForm(request.form)
	sensor = Adafruit_DHT.DHT11
	pin = 11
	if request.method == 'POST' and form.validate():
		temperature = request.form['temperature']
		humidity = request.form['humidity']
		weather_update(db,temperature,humidity)
		activate_weather_system(True)
		c_temperature = get_cur_temp(sensor, pin)
		c_humidity = get_cur_humid(sensor, pin)
		return render_template('weather.html', temperature=temperature, humidity=humidity, c_temperature=c_temperature, c_humidity=c_humidity)

@app.route('/cweather', methods=['POST'])
def c_weather():
	form = weatherForm(request.form)
	sensor = Adafruit_DHT.DHT11
	pin = 11
	if request.method == 'POST':
		c_temperature = get_cur_temp(sensor, pin)
		c_humidity = get_cur_humid(sensor, pin)
		temperature = extract_temp_limit(db)
		humidity = extract_humid_limit(db)
		activate_weather_system(True)
		return render_template('weather.html', temperature=temperature, humidity=humidity, c_temperature=c_temperature, c_humidity=c_humidity)

@app.route('/logout', methods=['POST'])
def logout():
	session.pop('logged_in', None)
	flash('You were logged out.')
	activate_light_system(False)
	GPIO.output(27,False)
	GPIO.output(22,False)
	GPIO.output(17,False)
	return render_template('login.html')

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0')
