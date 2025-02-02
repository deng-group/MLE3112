# How to drive the motor
"""
Author: Zeyu Deng (dengzeyu@gmail.com)
"""
import numpy as np
import pandas as pd
from mle3112.motor import drive_motor
from mle3112.spectrometer import drive_spectrometer


def measurement_single_filter(serial_number:str, 
                              start:float, end:float, step:float, 
                              data_file:str='data.csv',
                              max_num_failure:int=10,
                              tol:float=1e-3,
                              integration_time:float=100.0,
                              kinesis_path:str='C:/Program Files/Thorlabs/Kinesis',
                              avaspecx64_dll_path:str = 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll' )->None:
    """
    Perform measurements by driving a motor to specified positions and collecting data from a spectrometer.

    Parameters:
    serial_number (str): The serial number of the motor to be connected.
    start (float): The starting angle in degrees. Must be within 0 to 360 degrees.
    end (float): The ending angle in degrees.
    step (float): The step size in degrees for each measurement.
    data_file (str, optional): The name of the CSV file to save the measured data. Default is 'data.csv'.
    max_num_failure (int, optional): The maximum number of retries allowed for motor driving failures. Default is 10.
    tol (float, optional): The tolerance for motor position errors. Default is 1e-3.
    integration_time (float, optional): The integration time in milliseconds for the spectrometer. Default is 100.0 ms.
    kinesis_path (str, optional): The path to the Kinesis software. Default is 'C:/Program Files/Thorlabs/Kinesis'.
    avaspecx64_dll_path (str, optional): The path to the avaspecx64.dll file. Default is 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll'.

    Raises:
    ValueError: If the start angle is not within the range of 0 to 360 degrees.
    RuntimeError: If the motor driving fails for the specified number of retries.

    Returns:
    None: The function saves the measured data to a CSV file named 'data.csv'.

    Notes:
    - The function assumes the presence of `drive_motor` and `drive_spectrometer` functions.
    - The function also assumes the presence of `ThorlabsError` exception and `ser` serial connection.
    - The measured data is saved in a CSV file with columns: 'position', 'wavelength', and 'data'.
    """
    if not (0 <= start <= 360) or not (0 <= end <= 360) or not (0 <= step <= 360):
        raise ValueError('Start, end, and step, angles should be within 0 to 360 degrees!')
    
    measured_data = []
    print(f'Setting the initial positions to {start}...')
    drive_motor(start, serial_number, tol, max_num_failure, kinesis_path)
    for position in np.unique(np.arange(start, end + step, step) % 360):
        drive_motor(position, serial_number, tol, max_num_failure, kinesis_path)
        wavelength, intensity = drive_spectrometer(integration_time,avaspecx64_dll_path)
        measured_data.append([position, wavelength, intensity])

    df = pd.DataFrame(measured_data, columns=['position', 'wavelength', 'intensity'])
    df.to_csv(data_file)

def measurement_three_filters(ser1:str, ser2:str, ser3:str, 
                              start:float, end:float, step:float,
                              data_file:str='data_three_filters.csv',
                              max_num_failure:int=10,
                              tol:float=1e-3,
                              integration_time:float=100.0,
                              kinesis_path:str='C:/Program Files/Thorlabs/Kinesis',
                              avaspecx64_dll_path:str = 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll')->None:
    """
    Perform measurements using three filters by driving motors to specified positions and recording data.

    Parameters:
    ser1 (str): The serial number of the first motor.
    ser2 (str): The serial number of the second motor.
    ser3 (str): The serial number of the third motor.
    start (float): The starting angle for the motors, should be within 0 to 360 degrees.
    end (float): The ending angle for the motors.
    step (float): The step size for incrementing the motor positions.
    data_file (str, optional): The name of the CSV file to save the measured data. Default is 'data_three_filters.csv'.
    max_num_failure (int, optional): The maximum number of allowed failures for driving the motors. Default is 10.
    tol (float, optional): The tolerance for motor position errors. Default is 1e-3.
    integration_time (float, optional): The integration time in milliseconds for the spectrometer. Default is 100.0 ms.
    kinesis_path (str, optional): The path to the Kinesis software. Default is 'C:/Program Files/Thorlabs/Kinesis'.
    avaspecx64_dll_path (str, optional): The path to the avaspecx64.dll file. Default is 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll'.

    Raises:
    ValueError: If the start angle is not within the range of 0 to 360 degrees.

    Returns:
    None

    Notes:
    - The function drives three motors to various positions within the specified range and step size.
    - It then measures data using a spectrometer at each combination of positions and stores the results in a CSV file.
    """
    if not (0 <= start <= 360) or not (0 <= end <= 360) or not (0 <= step <= 360):
        raise ValueError('Start, end, and step, angles should be within 0 to 360 degrees!')
    measured_data = []

    print(f'Setting the initial positions to {start}...')
    drive_motor(start, ser1, tol, max_num_failure, kinesis_path)
    drive_motor(start, ser2, tol, max_num_failure, kinesis_path)
    drive_motor(start, ser3, tol, max_num_failure, kinesis_path)

    for pos1 in np.unique(np.arange(start, end + step, step) % 360):
        drive_motor(pos1, ser1, tol, max_num_failure, kinesis_path)
        for pos2 in np.unique(np.arange(start, end + step, step) % 360):
            drive_motor(pos2, ser2, tol, max_num_failure, kinesis_path)
            for pos3 in np.unique(np.arange(start, end + step, step) % 360):
                print(f"Setting the positions to: {pos1}, {pos2}, {pos3}")
                drive_motor(pos3, ser3, tol, max_num_failure, kinesis_path)

                wavelength, intensity = drive_spectrometer(integration_time,avaspecx64_dll_path)
                measured_data.append([pos1, pos2, pos3, wavelength, intensity])
                
    df = pd.DataFrame(measured_data, columns=['position1', 'position2', 'position3', 'wavelength', 'intensity'])
    df.to_csv(data_file)
