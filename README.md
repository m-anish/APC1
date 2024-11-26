# APC1 Weather Sensor Library for MicroPython

This repository contains a MicroPython library to interface with the APC1 weather sensor over I2C. The `APC1` class provides an easy way to read and parse data from various sensors such as particulate matter (PM1.0, PM2.5, PM10), TVOC, eCO2, temperature, and humidity.

## Features

- Supports communication with the APC1 weather sensor via I2C.
- Retrieves and parses sensor data from the APC1 registers (PM1.0, PM2.5, PM10, TVOC, eCO2, etc.).
- Provides a method to fetch all sensor data in a structured format.
- Configurable I2C communication parameters (SDA, SCL pins, and I2C frequency).
- Option to use a custom I2C device address (defaults to `0x12`).
- Provides detailed sensor information (name, value, unit, description).

## Example Usage

```python
import APC1

# Initialize the APC1 instance with default pin values (scl=1, sda=0, id=0)
# Default values:
#   id = 0 (I2C peripheral ID)
#   scl = 1 (SCL pin number)
#   sda = 0 (SDA pin number)
apc1 = APC1.APC1()

# Get and print data for all sensors
all_sensor_data = apc1.get_all_sensor_data()

# Print all the sensor data in a readable format
for sensor_name, data in all_sensor_data.items():
    print(f"{sensor_name}: {data['value']} {data['unit']} - {data['description']}")
