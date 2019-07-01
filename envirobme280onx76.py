# this script will up load your gy-bme280 temp/press/humidi/alti to adafruit io  
# you must create feeds  with names temperature2,pressure2,humidity2,altitude2 
#once the feeds are created you can create your own dash to display those readings

import time
import board
import busio
import adafruit_bme280

from Adafruit_IO import Client, Feed, RequestError
LOOP_DELAY = 10
ADAFRUIT_IO_KEY = '0d23b4cab7a04da284d43dc5f90185a'
ADAFRUIT_IO_USERNAME = 'YourUsername'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we already have the feeds, assign them.
    temperature_feed = aio.feeds('temperature2')
    humidity_feed = aio.feeds('humidity2')
    pressure_feed = aio.feeds('pressure2')
    altitude_feed = aio.feeds('altitude2')
except RequestError: # if we don't, create and assign them.
    temperature_feed = aio.create_feed(Feed(name='temperature2'))
    humidity_feed = aio.create_feed(Feed(name='humidity2'))
    pressure_feed = aio.create_feed(Feed(name='pressure2'))
    altitude_feed = aio.create_feed(Feed(name='altitude2'))

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

while True:
    print('Reading sensors...')
    temp_data = bme280.temperature
    # convert temperature (C->F)
    temp_data = int(temp_data) * 1.8 + 32
    humid_data = bme280.humidity
    pressure_data = bme280.pressure
    alt_data = bme280.altitude

    print('sending data to adafruit io...')
    # Send BME280 Data to Adafruit IO.
    print('Temperature: %0.1f C' % temp_data)
    aio.send(temperature_feed.key, temp_data)
    print("Humidity: %0.1f %%" % humid_data)
    aio.send(humidity_feed.key, int(humid_data))
    time.sleep(2)
    print("Pressure: %0.1f hPa" % pressure_data)
    aio.send(pressure_feed.key, int(pressure_data))
    print("Altitude = %0.2f meters" % alt_data)
    aio.send(altitude_feed.key, int(alt_data))

    time.sleep(LOOP_DELAY * 60)

