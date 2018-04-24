import sqlite3
import os
conn = sqlite3.connect('weather.sqlite')

c = conn.cursor()
c.execute('CREATE TABLE weather_db'' (id TEXT, temperature INTEGER, humidity INTEGER)')

c.execute("INSERT INTO weather_db"" (id, temperature, humidity) VALUES"" (?, ?, ?)", (1, 0, 0))

conn.commit()
conn.close()