# How to drive the motor
"""
Author: Zeyu Deng (dengzeyu@gmail.com)
"""
import numpy as np
import pandas as pd
from mle3112.motor import drive_motor
from mle3112.spectrometer import drive_spectrometer
import os

def automated_measurement(serial_number:str,
                         start:float, end:float, step:float,
                         data_file:str='data.csv',
                         max_num_failure:int=10,
                         tol:float=1e-2,
                         integration_time:float=100.0,
                         kinesis_path:str='C:/Program Files/Thorlabs/Kinesis',
                         avaspecx64_dll_path:str = 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll',
                         dry_run:bool=False)->None:
    """
    Perform measurements using single filter by driving motor to specified positions and recording data.
    Data is saved to a CSV file.

    Parameters:
    serial_number (str): The serial number of the motor.
    start (float): The starting angle for the motors, should be within 0 to 360 degrees.
    end (float): The ending angle for the motors.
    step (float): The step size for incrementing the motor positions.
    data_file (str, optional): The name of the CSV file to save the measured data. Default is 'data.csv'.
    max_num_failure (int, optional): The maximum number of allowed failures for driving the motors. Default is 10.
    tol (float, optional): The tolerance for motor position errors. Default is 1e-2.
    integration_time (float, optional): The integration time in milliseconds for the spectrometer. Default is 100.0 ms.
    kinesis_path (str, optional): The path to the Kinesis software. Default is 'C:/Program Files/Thorlabs/Kinesis'.
    avaspecx64_dll_path (str, optional): The path to the avaspecx64.dll file. Default is 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll'.
    dry_run (bool, optional): If True, perform a dry run without actually driving the motors and spectrometer. Default is False.

    Raises:
    ValueError: If the start angle is not within the range of 0 to 360 degrees.

    Returns:
    None
    """
    if not (0 <= start <= 360) or not (0 <= end <= 360) or not (0 <= step <= 360):
        raise ValueError('Start, end, and step, angles should be within 0 to 360 degrees!')
    measured_data = []

    print(f'Starting measurements.. Data will be saved to: {data_file}' )
    if dry_run:
        print("Dry run mode is enabled. No motors will be moved and no spectrometer will be driven.")
    
    position = start

    if not dry_run:
        print(f"Move motor to start positions: {position}")
        drive_motor(start, serial_number, tol, max_num_failure, kinesis_path)

    step_count = 0
    
    for position in np.unique(np.arange(start, end + step, step) % 360):
        step_count += 1
        print(f"Measuring at position: {position}")
        if not dry_run:
            drive_motor(position, serial_number, tol, max_num_failure, kinesis_path)
            wavelength, intensity = drive_spectrometer(integration_time, avaspecx64_dll_path)
        else:
            wavelength, intensity = ['NA'], ['NA']
        measured_data.append([position, wavelength, intensity])
        
    df = pd.DataFrame(measured_data, columns=['position1', 'wavelength', 'intensity'])
    df.to_csv(data_file, index=False, mode='w', header=True)
