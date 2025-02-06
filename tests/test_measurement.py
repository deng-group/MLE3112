import unittest
from mle3112.measurement import Measurement
import os

class TestMeasurement(unittest.TestCase):

    def setUp(self):
        self.measurement = Measurement(serial_number="12345", start=0, end=360, step=10)

    def test_single_filter_measurement(self):
        data_file = 'test_data_single.csv'
        self.measurement.measurement_single_filter(data_file=data_file)
        # Check if data file is created
        self.assertTrue(os.path.exists(data_file))
        # Additional checks can be added to verify the contents of the data file

    def test_three_filters_measurement(self):
        data_file = 'test_data_three.csv'
        self.measurement.measurement_three_filters(ser1="123", ser2="456", ser3="789", data_file=data_file)
        # Check if data file is created
        self.assertTrue(os.path.exists(data_file))
        # Additional checks can be added to verify the contents of the data file

    def test_invalid_angle(self):
        with self.assertRaises(ValueError):
            self.measurement.measurement_single_filter(start=370, end=360, step=10)

    def test_continue_from(self):
        data_file = 'test_data_continue.csv'
        self.measurement.measurement_three_filters(ser1="123", ser2="456", ser3="789", data_file=data_file, continue_from=[0, 0, 0])
        # Check if data file is created
        self.assertTrue(os.path.exists(data_file))
        # Additional checks can be added to verify the contents of the data file

    def tearDown(self):
        # Clean up any created test data files
        for file in ['test_data_single.csv', 'test_data_three.csv', 'test_data_continue.csv']:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()