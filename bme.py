from datetime import datetime
import time
import smbus2
import bme280

# Initialize with current date/time and build logger filename
now = datetime.now()
year = str(now.year)
month = str(now.month)
day = str(now.day)
hour = str(now.hour)
minute = str(now.minute)
seconds = str(now.second)
ts = year + "/" + month + "/" + day + " " + hour + ":" + minute + ":" + seconds
filename1 = "/data/Sensor_Data_"+ year + "_" + month + "_" + day + "_" + hour + "_" + minute + "_" + seconds  + ".csv"

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(2)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Create data file with headers
f = open(filename1, 'a+')
f.write('ts, temp, humidity, pressure\n');
f.close

while True:
    try:
        now = datetime.now()
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        hour = str(now.hour)
        minute = str(now.minute)
        seconds = str(now.second)
        ts = year + "/" + month + "/" + day + " " + hour + ":" + minute + ":" + seconds
        # Read sensor data
        data = bme280.sample(bus, address, calibration_params)
        # Extract temperature, pressure, and humidity
        temperature = round(data.temperature,1)
        temperature = str(temperature)
        pressure = round(data.pressure,1)
        pressure = str(pressure)
        humidity = round(data.humidity,1)

        # Build output data
        data = ts, temperature, humidity, pressure
        output = str(data)
        output = output.replace("(","")
        output = output.replace(")","")

        # Write data to sensor_data.csv
        f = open(filename1, 'a+')
        f.write(output + "\n")
        f.close()

        # Wait for a few seconds before the next reading
        time.sleep(60)

    except KeyboardInterrupt:
        print('Program stopped')
        break
    except Exception as e:
        print('An unexpected error occurred:', str(e))
        break
