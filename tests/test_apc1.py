import unittest
from unittest.mock import MagicMock
from apc1 import APC1  # Importing the APC1 class from the apc1 package

class TestAPC1(unittest.TestCase):

    def setUp(self):
        """
        Set up a mock APC1 instance for testing.
        """
        self.apc1 = APC1.APC1(id=0, scl=1, sda=0)
        
        # Mock I2C interface
        self.apc1.i2c = MagicMock()
        
    def test_get_reg_map(self):
        """
        Test the reg map of the sensor.
        """
        reg_map = self.apc1.get_reg_map()
        self.assertIsInstance(reg_map, list)  # The reg map should be a list
        self.assertGreater(len(reg_map), 0)   # It should not be empty

    def test_get_sensor_data_valid(self):
        """
        Test retrieving valid sensor data (e.g., PM2.5).
        """
        self.apc1.read_sensor_data = MagicMock(return_value=[0x00, 0x01])  # Mock the I2C data
        sensor_name = 'PM2.5'
        value, unit, description = self.apc1.get_sensor_data(sensor_name)
        
        self.assertIsInstance(value, float)  # The value should be a float
        self.assertEqual(unit, 'ug/m3')  # Unit for PM2.5 should be ug/m3
        self.assertIsInstance(description, str)  # Description should be a string
        self.assertEqual(description, 'PM2.5 Mass Concentration')  # Check that the description is correct

    def test_get_sensor_data_invalid(self):
        """
        Test retrieving sensor data for an invalid register.
        """
        invalid_sensor_name = 'INVALID_SENSOR'
        with self.assertRaises(ValueError):
            self.apc1.get_sensor_data(invalid_sensor_name)
        
    def test_get_all_sensor_data(self):
        """
        Test retrieving data for all sensors.
        """
        # Mock the reading function for multiple sensors
        self.apc1.read_sensor_data = MagicMock(return_value=[0x00, 0x01])
        
        all_data = self.apc1.get_all_sensor_data()
        
        self.assertIsInstance(all_data, dict)  # The result should be a dictionary
        self.assertIn('PM2.5', all_data)  # The PM2.5 sensor should be included
        self.assertIn('PM10', all_data)  # The PM10 sensor should be included

    def test_get_sensor_data_edge_case(self):
        """
        Test edge case for getting sensor data (e.g., empty response).
        """
        self.apc1.read_sensor_data = MagicMock(return_value=[])
        
        # Test with a valid sensor that should return an empty list
        value, unit, description = self.apc1.get_sensor_data('PM2.5')
        
        self.assertEqual(value, 0.0)  # Empty response should return 0 value
        self.assertEqual(unit, 'ug/m3')  # Unit should remain the same
        self.assertEqual(description, 'PM2.5 Mass Concentration')  # Description should remain the same

if __name__ == '__main__':
    unittest.main()
