from datetime import datetime
import time, smbus2, bme280, os
# Fetch hostname
host = os.uname()[1]

# Initialize with current date/time, hostname, paths, and build logger filename
now = datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
filename = "/bme280/data/sd_" + host + "_" + now.strftime("%Y-%m-%d_%Hh%Mm%Ss") + ".csv"

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(2)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Create data file with column headers
f = open(filename, 'a+')
f.write('ts, temp, humidity, pressure\n');
f.close

while True:
    try:
        now = datetime.now()
        ts = now.strftime("%Y-%m-%d %H:%M:%S")
        # Read sensor data
        data = bme280.sample(bus, address, calibration_params)
        # Extract temperature, pressure, and humidity
        temperature = round(data.temperature,1)
        temperature = str(temperature)
        pressure = round(data.pressure,1)
        pressure = str(pressure)
        humidity = round(data.humidity,1)

        # Build output data string
        data = ts, temperature, humidity, pressure
        output = str(data)
        # Remove extraneous parentheses
        output = output.replace("(","")
        output = output.replace(")","")

        # Write data to sensor_data.csv
        f = open(filename, 'a+')
        f.write(output + "\n")
        f.close()
        del now, ts
        # Wait for a few seconds before the next reading
        time.sleep(60)

    except KeyboardInterrupt:
        print('Program stopped')
        break
    except Exception as e:
        print('An unexpected error occurred:', str(e))
        break
