from datetime import datetime
import time, smbus2, bme280, os

# Fetch hostname
host = os.uname()[1]

# Initialize with current date/time, hostname, paths, and build logger filename
now = datetime.now()
ts = now.strftime("%m/%d/%y %H:%M")
filename = "/bme280/data/" + host + ".csv"
file_path = filename

# Check to see if a pre-existing csv exists, if so skip adding an additional header
if os.path.exists(file_path):
     print('')
else:
     f = open(filename, 'a+')
     f.write('ts,temp,humidity,pressure\n');
     f.close

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
# 1 for Raspberry Pi, 2 for Orange Pi
bus = smbus2.SMBus(2)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

while True:
    try:
    	  # Construct time stamp
        now = datetime.now()
				ts = now.strftime("%m/%d/%y %H:%M")
        
        # Read sensor data
        data = bme280.sample(bus, address, calibration_params)
        
        # Extract temperature, humidity, and pressure from bme280 sensor
        # Convert and round off temperature, humidity, and pressure from integers to strings
        temperature = str(round(data.temperature))
        humidity = str(round(data.humidity))
        pressure = str(round(data.pressure))
        
        #build a  data string that will be output to the csv file
        data = ts + "," + temperature + "," + humidity + "," + pressure 
        
        # Ensure that output data to CSV is a string
        output = str(data)
        
        # Remove extraneous element chars such as open/close parenthesis and single quotes
        output = output.replace("(","")
        output = output.replace(")","")
        output = output.replace("'","")
        
        # Write data to CSV
        # Open csv file as append/create
        f = open(filename, 'a+')
        f.write(output + "\n")
        f.close()
        
        # Clear some variables
        del now, ts
        
        # Wait for a few seconds before the next reading
        time.sleep(300)

    except KeyboardInterrupt:
        print('Program stopped')
        break
    except Exception as e:
        print('An unexpected error occurred:', str(e))
        break
