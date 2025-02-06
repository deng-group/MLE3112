import h5py
import csv
import numpy as np
import pandas as pd

"""
Author: Zeyu Deng
Email: dengzeyu@gmail.com
"""

class Data:
    """
    A class to handle data loading, processing, and saving for measurement data.

    Attributes:
        file_path (str): Path to the data file.
        measurement_key (str): Key prefix for measurements in the data file. Default is 'measurement_'.
        position_key (str): Key for position data in the measurements. Default is 'position'.
        wavelength_key (str): Key for wavelength data in the measurements. Default is 'wavelength'.
        intensity_key (str): Key for intensity data in the measurements. Default is 'intensity'.
    """

    def __init__(self, file_path: str, 
                 measurement_key: str = 'measurement_', 
                 position_key: str = 'position', 
                 wavelength_key: str = 'wavelength', 
                 intensity_key: str = 'intensity') -> None:
        self.file_path = file_path
        self.measurement_key = measurement_key
        self.position_key = position_key
        self.wavelength_key = wavelength_key
        self.intensity_key = intensity_key

    def _load_hdf_data(self, f) -> dict:
        data = {}
        for key in f.keys():
            if key.startswith(self.measurement_key):
                data[key] = {
                    self.position_key: f[key][self.position_key][()] if np.isscalar(f[key][self.position_key][()]) else f[key][self.position_key][:],
                    self.wavelength_key: f[key][self.wavelength_key][()] if np.isscalar(f[key][self.wavelength_key][()]) else f[key][self.wavelength_key][:],
                    self.intensity_key: f[key][self.intensity_key][()] if np.isscalar(f[key][self.intensity_key][()]) else f[key][self.intensity_key][:]
                }
        return data

    def _load_csv_data(self) -> dict:
        data = pd.read_csv(self.file_path)
        result = {}
        for _, row in data.iterrows():
            key = row['measurement_id']
            result[key] = {
                self.position_key: np.array(eval(row[self.position_key])),
                self.wavelength_key: np.array(eval(row[self.wavelength_key])),
                self.intensity_key: np.array(eval(row[self.intensity_key]))
            }
        return result

    def _load_data(self) -> dict:
        if self.file_path.endswith(('.h5', '.hdf5', 'hdf')):
            with h5py.File(self.file_path, 'r') as f:
                return self._load_hdf_data(f)
        elif self.file_path.endswith('.csv'):
            return self._load_csv_data()
        else:
            raise ValueError('Unsupported file format. Please use .h5, .hdf5, or .csv files.')

    def _get_hdf_measurement(self, f, key) -> dict:
        if key in f:
            return {
                self.position_key: f[key][self.position_key][:],
                self.wavelength_key: f[key][self.wavelength_key][:],
                self.intensity_key: f[key][self.intensity_key][:]
            }
        else:
            raise KeyError(f'Measurement ID {key} not found.')

    def _get_csv_measurement(self, key) -> dict:
        data = pd.read_csv(self.file_path)
        row = data[data['measurement_id'] == key]
        if not row.empty:
            row = row.iloc[0]
            return {
                self.position_key: np.array(eval(row[self.position_key])),
                self.wavelength_key: np.array(eval(row[self.wavelength_key])),
                self.intensity_key: np.array(eval(row[self.intensity_key]))
            }
        raise KeyError(f'Measurement ID {key} not found.')

    def get_measurement(self, measurement_id: int) -> dict:
        key = f'{self.measurement_key}{measurement_id}'
        if self.file_path.endswith(('.h5', '.hdf5', 'hdf')):
            with h5py.File(self.file_path, 'r') as f:
                return self._get_hdf_measurement(f, key)
        elif self.file_path.endswith('.csv'):
            return self._get_csv_measurement(key)
        else:
            raise ValueError('Unsupported file format. Please use .h5, .hdf5, or .csv files.')

    # def get_data_by_position(self, position) -> dict:
    #     data = self._load_data()
    #     result = {self.wavelength_key: [], self.intensity_key: []}
        
    #     if isinstance(position, (float, int)):
    #         position = np.array([position])
    #     elif isinstance(position, list):
    #         position = np.array(position)
    #     position = position.flatten()
        
    #     for measurement in data.values():
    #         indices = np.isin(measurement[self.position_key], position)
    #         if np.any(indices):
    #             result[self.wavelength_key].extend(measurement[self.wavelength_key][indices])
    #             result[self.intensity_key].extend(measurement[self.intensity_key][indices])
        
    #     if not result[self.wavelength_key] and not result[self.intensity_key]:
    #         return None
        
    #     return result

    def add_measurement(self, measurement_id: int, 
                        position: np.ndarray, 
                        wavelength: np.ndarray, 
                        intensity: np.ndarray) -> None:
        key = f'{self.measurement_key}{measurement_id}'
        if self.file_path.endswith(('.h5', '.hdf5', 'hdf')):
            with h5py.File(self.file_path, 'a') as f:
                if key in f:
                    del f[key]
                grp = f.create_group(key)
                grp.create_dataset(self.position_key, data=position)
                grp.create_dataset(self.wavelength_key, data=wavelength)
                grp.create_dataset(self.intensity_key, data=intensity)
        elif self.file_path.endswith('.csv'):
            data = {
                'measurement_id': [key],
                self.position_key: [position.tolist()],
                self.wavelength_key: [wavelength.tolist()],
                self.intensity_key: [intensity.tolist()]
            }
            df = pd.DataFrame(data)
            df.to_csv(self.file_path, mode='a', header=not pd.io.common.file_exists(self.file_path), index=False)
        else:
            raise ValueError('Unsupported file format. Please use .h5, .hdf5, hdf, or .csv files.')
