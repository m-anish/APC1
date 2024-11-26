from machine import I2C, Pin


class APC1(I2C):
    """
    A class to interface with the APC1 Weather Sensor over I2C.

    This class allows for reading and parsing data from various registers on the APC1 sensor,
    such as PM1.0, PM2.5, PM10, TVOC, eCO2, temperature, and humidity.

    Example usage:
    
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

    This will initialize the APC1 sensor on the default I2C pins, retrieve data for all sensor registers, and print the results.
    """

    # Register map for APC1 weather sensor
    _REG_MAP = [
        ['PM1.0', 0x04, 2, 1, 'ug/m3', 'PM1.0 Mass Concentration'],
        ['PM2.5', 0x06, 2, 1, 'ug/m3', 'PM2.5 Mass Concentration'],
        ['PM10', 0x08, 2, 1, 'ug/m3', 'PM10 Mass Concentration'],
        ['TVOC', 0x1C, 2, 1, 'ppb', 'TVOC output'],
        ['eCO2', 0x1E, 2, 1, 'ppm', 'Output in ppm CO2 equivalents'],
        ['T-comp', 0x22, 2, 0.1, 'C', 'Compensated Temperature'],
        ['RH-comp', 0x24, 2, 0.1, '%', 'Compensated Relative Humidity'],
        ['T-raw', 0x26, 2, 0.1, 'C', 'Raw Temperature'],
        ['RH-raw', 0x28, 2, 0.1, '%', 'Raw Relative Humidity'],
        ['AQI', 0x3A, 1, 1, '', 'AQI according to TVOC value']
    ]

    # Private default device address set to 0x12
    _DEFAULT_DEVICE_ADDR = 0x12

    def __init__(self, id=0, scl=1, sda=0, freq=100000, device_addr=None):
        """
        Initialize the APC1 I2C object.

        :param id: I2C peripheral ID (default: 0)
        :param scl: Pin number for SCL (default: 1)
        :param sda: Pin number for SDA (default: 0)
        :param freq: I2C frequency (default: 100kHz)
        :param device_addr: Optional I2C device address (default: 0x12)
        """
        # Convert the passed integer pin numbers into machine.Pin objects
        scl_pin = Pin(scl)
        sda_pin = Pin(sda)

        super().__init__(id=id, scl=scl_pin, sda=sda_pin, freq=freq)
        self.device_addr = device_addr or self._DEFAULT_DEVICE_ADDR  # Use default if none provided

    @classmethod
    def get_reg_map(cls):
        """
        Get the register map for the APC1 weather sensor.

        :return: List of sensor register details
        """
        return cls._REG_MAP

    def read_sensor_data(self, register, num_bytes):
        """
        Read data from a specified register of the APC1 sensor.

        :param register: The register address to read from.
        :param num_bytes: The number of bytes to read.
        :return: The data read from the register as a bytearray.
        """
        return self.readfrom_mem(self.device_addr, register, num_bytes)

    def get_sensor_data(self, register_name):
        """
        Get and parse sensor data based on the register name.

        :param register_name: The name of the register to read and parse.
        :return: The parsed value, unit, and description of the register.
        """
        # Create a dictionary from the register map for easier look-up
        reg_map_dict = {reg[0]: reg for reg in self._REG_MAP}

        # Check if the register name exists in the dictionary
        if register_name not in reg_map_dict:
            raise ValueError(f"Register '{register_name}' not found.")

        # Extract the register details from the dictionary
        register_info = reg_map_dict[register_name]
        register_address, num_bytes, scale, unit, description = register_info[1], register_info[2], register_info[3], register_info[4], register_info[5]

        # Read raw data from the sensor register
        raw_data = self.read_sensor_data(register_address, num_bytes)

        # Process the raw data based on register information
        if len(raw_data) != num_bytes:
            raise ValueError(f"Expected {num_bytes} bytes of data, but got {len(raw_data)}.")

        # Convert raw data into a numeric value
        value = int.from_bytes(raw_data, 'big') * scale
        return value, unit, description

    def get_all_sensor_data(self):
        """
        Retrieve and parse data for all registers in the register map.

        :return: A dictionary with register names as keys and their parsed values as values.
        """
        all_data = {}
        for reg_info in self._REG_MAP:
            register_name = reg_info[0]
            value, unit, description = self.get_sensor_data(register_name)
            all_data[register_name] = {
                'value': value,
                'unit': unit,
                'description': description
            }
        return all_data
