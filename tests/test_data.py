import unittest
import numpy as np
import os
import h5py
import pandas as pd
from mle3112.data import Data

class TestData(unittest.TestCase):

    def setUp(self):
        # Create a temporary HDF5 file for testing
        self.h5_file_path = 'test_data.h5'
        with h5py.File(self.h5_file_path, 'w') as f:
            grp = f.create_group('measurement_1')
            grp.create_dataset('position', data=np.array([1.0, 2.0, 3.0]))
            grp.create_dataset('wavelength', data=np.linspace(400, 500, 100))
            grp.create_dataset('intensity', data=np.linspace(10, 20, 100))

        # Create a temporary CSV file for testing
        self.csv_file_path = 'test_data.csv'
        data = {
            'measurement_id': ['measurement_1'],
            'position': ['[1.0, 2.0, 3.0]'],
            'wavelength': [np.linspace(400, 500, 100).tolist()],
            'intensity': [np.linspace(10, 20, 100).tolist()]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_file_path, index=False)

    def tearDown(self):
        # Remove the temporary files after tests
        if os.path.exists(self.h5_file_path):
            os.remove(self.h5_file_path)
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)

    def test_load_data_h5(self):
        data = Data(self.h5_file_path)
        loaded_data = data._load_data()
        self.assertIn('measurement_1', loaded_data)
        self.assertTrue(np.array_equal(loaded_data['measurement_1']['position'], np.array([1.0, 2.0, 3.0])))
        self.assertTrue(np.array_equal(loaded_data['measurement_1']['wavelength'], np.array([400, 500, 600])))
        self.assertTrue(np.array_equal(loaded_data['measurement_1']['intensity'], np.array([10, 20, 30])))

    def test_load_data_csv(self):
        data = Data(self.csv_file_path)
        loaded_data = data._load_data()
        self.assertIn('measurement_1', loaded_data)
        self.assertTrue(np.array_equal(loaded_data['measurement_1']['position'], np.array([1.0, 2.0, 3.0])))
        self.assertTrue(np.array_equal(loaded_data['measurement_1']['wavelength'], np.array([400, 500, 600])))
        self.assertTrue(np.array_equal(loaded_data['measurement_1']['intensity'], np.array([10, 20, 30])))

    def test_get_measurement(self):
        data = Data(self.h5_file_path)
        measurement = data.get_measurement(1)
        self.assertIsNotNone(measurement)
        self.assertTrue(np.array_equal(measurement['position'], np.array([1.0, 2.0, 3.0])))
        self.assertTrue(np.array_equal(measurement['wavelength'], np.array([400, 500, 600])))
        self.assertTrue(np.array_equal(measurement['intensity'], np.array([10, 20, 30])))

    def test_get_data_by_position(self):
        data = Data(self.h5_file_path)
        result = data.get_data_by_position(2.0)
        self.assertIsNotNone(result)
        self.assertEqual(result['wavelength'], 500)
        self.assertEqual(result['intensity'], 20)

    def test_save_data(self):
        data = Data(self.h5_file_path)
        new_file_path = 'saved_data.h5'
        data.save_data(new_file_path)
        with h5py.File(new_file_path, 'r') as f:
            self.assertIn('measurement_1', f)
            self.assertTrue(np.array_equal(f['measurement_1']['position'][:], np.array([1.0, 2.0, 3.0])))
            self.assertTrue(np.array_equal(f['measurement_1']['wavelength'][:], np.array([400, 500, 600])))
            self.assertTrue(np.array_equal(f['measurement_1']['intensity'][:], np.array([10, 20, 30])))
        os.remove(new_file_path)

    def test_add_measurement(self):
        data = Data(self.h5_file_path)
        data.add_measurement(2, np.array([4.0, 5.0, 6.0]), np.array([700, 800, 900]), np.array([40, 50, 60]))
        with h5py.File(self.h5_file_path, 'r') as f:
            self.assertIn('measurement_2', f)
            self.assertTrue(np.array_equal(f['measurement_2']['position'][:], np.array([4.0, 5.0, 6.0])))
            self.assertTrue(np.array_equal(f['measurement_2']['wavelength'][:], np.array([700, 800, 900])))
            self.assertTrue(np.array_equal(f['measurement_2']['intensity'][:], np.array([40, 50, 60])))

if __name__ == '__main__':
    unittest.main()