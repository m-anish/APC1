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

### Reading Data from All Sensors

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
```

This example initializes the APC1 sensor with the default I2C pins (`SCL=1`, `SDA=0`, `id=0`), fetches data for all sensors, and prints the name, value, unit, and description of each sensor.

### Reading a Single Sensor Value (e.g., PM2.5)

```python
import APC1

# Initialize the APC1 instance with default pin values (scl=1, sda=0, id=0)
apc1 = APC1.APC1()

# Get and print data for PM2.5 sensor
pm25_value, unit, description = apc1.get_sensor_data('PM2.5')

# Print the PM2.5 data
print(f"PM2.5: {pm25_value} {unit} - {description}")
```

In this example, the code reads and prints the value of the **PM2.5** sensor (Mass Concentration of Particulate Matter with a diameter of less than 2.5 micrometers). It also prints the unit and description for the PM2.5 sensor.

## Library Functions

- **`get_reg_map()`**: Returns the register map for the APC1 sensor.
- **`read_sensor_data(register, num_bytes)`**: Reads raw data from a specific register.
- **`get_sensor_data(register_name)`**: Retrieves and parses sensor data from a specified register.
- **`get_all_sensor_data()`**: Retrieves and parses data from all registers and returns a dictionary with the sensor name, value, unit, and description.

## Installation

To use this library, simply place the `APC1.py` file in your MicroPython project directory.

```bash
# Example installation on your device
cp APC1.py /flash/lib
```

## License

This library is licensed under the **GNU General Public License v3.0 (GPLv3)**.

See [LICENSE](LICENSE) for more details.

## Credits

- **APC1 Weather Sensor**: Manufacturer's documentation and specifications.
- **MicroPython**: For providing an excellent platform for embedded programming.
- **ChatGPT**: For assisting with code and documentation snippets.

## Contact

For any issues, feel free to open an issue on this repository.
