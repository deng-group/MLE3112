# How to drive the motor
"""
Author: Zeyu Deng (dengzeyu@gmail.com)
"""
import numpy as np
import pandas as pd
from mle3112.motor import drive_motor
from mle3112.spectrometer import drive_spectrometer
from mle3112.utils import Progress
import os

def measurement_single_filter(serial_number:str,
                              start:float, end:float, step:float,
                              data_file:str='data.csv',
                              max_num_failure:int=10,
                              tol:float=1e-2,
                              integration_time:float=100.0,
                              kinesis_path:str='C:/Program Files/Thorlabs/Kinesis',
                              avaspecx64_dll_path:str = 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll',
                              dry_run:bool=False,
                              overwrite_datafile:bool=False)->None:
    """
    Perform measurements using single filter by driving motor to specified positions and recording data.
    Data is saved to a CSV file after every measurement step.

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
    overwrite_datafile (bool, optional): If True, overwrite the existing data file. Default is False.

    Raises:
    ValueError: If the start angle is not within the range of 0 to 360 degrees.

    Returns:
    None
    """
    if not (0 <= start <= 360) or not (0 <= end <= 360) or not (0 <= step <= 360):
        raise ValueError('Start, end, and step, angles should be within 0 to 360 degrees!')
    measured_data = []

    total_steps = len(np.unique(np.arange(start, end + step, step) % 360))
    progress = Progress(total_steps)

    progress.show_msg(message=f'Starting measurements.. Data will be saved to: {data_file}' )
    
    position = start
    step_count = 0
    if not dry_run:
        progress.update(step_count, message=f"Move motor to start positions: {position}")
        drive_motor(start, serial_number, tol, max_num_failure, kinesis_path)

    for position in np.unique(np.arange(start, end + step, step) % 360):
        step_count += 1
        progress.update(step_count, message=f"Measuring at position: {position}")
        if not dry_run:
            drive_motor(position, serial_number, tol, max_num_failure, kinesis_path)
            wavelength, intensity = drive_spectrometer(integration_time, avaspecx64_dll_path)
        else:
            wavelength, intensity = ['NA'], ['NA']
        measured_data.append([position, wavelength, intensity])
        
        # Save data every step
        if overwrite_datafile:
            df_all = pd.DataFrame(measured_data, columns=['position1', 'wavelength', 'intensity'])
            df_all.to_csv(data_file, index=False, mode='w', header=True)
        elif not os.path.exists(data_file):
            new_entry = pd.DataFrame([measured_data[-1]], columns=['position1', 'wavelength', 'intensity'])
            new_entry.to_csv(data_file, index=False, mode='w', header=True)
        else:
            progress.show_msg(f"Warning: {data_file} exists; new data will be appended.")
            new_entry = pd.DataFrame([measured_data[-1]], columns=['position1', 'wavelength', 'intensity'])
            new_entry.to_csv(data_file, index=False, mode='a', header=False)
    progress.complete()


def measurement_three_filters(ser1:str, ser2:str, ser3:str, 
                              start:float, end:float, step:float,
                              data_file:str='data_three_filters.csv',
                              max_num_failure:int=10,
                              tol:float=1e-2,
                              integration_time:float=100.0,
                              kinesis_path:str='C:/Program Files/Thorlabs/Kinesis',
                              avaspecx64_dll_path:str = 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll',
                              dry_run:bool=False,
                              overwrite_datafile:bool=False)->None:
    """
    Perform measurements using three filters by driving motors to specified positions and recording data.
    Data is saved to a CSV file after every measurement step.

    Parameters:
    ser1 (str): The serial number of the first motor.
    ser2 (str): The serial number of the second motor.
    ser3 (str): The serial number of the third motor.
    start (float): The starting angle for the motors, should be within 0 to 360 degrees.
    end (float): The ending angle for the motors.
    step (float): The step size for incrementing the motor positions.
    data_file (str, optional): The name of the CSV file to save the measured data. Default is 'data_three_filters.csv'.
    max_num_failure (int, optional): The maximum number of allowed failures for driving the motors. Default is 10.
    tol (float, optional): The tolerance for motor position errors. Default is 1e-2.
    integration_time (float, optional): The integration time in milliseconds for the spectrometer. Default is 100.0 ms.
    kinesis_path (str, optional): The path to the Kinesis software. Default is 'C:/Program Files/Thorlabs/Kinesis'.
    avaspecx64_dll_path (str, optional): The path to the avaspecx64.dll file. Default is 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll'.
    dry_run (bool, optional): If True, perform a dry run without actually driving the motors and spectrometer. Default is False.
    overwrite_datafile (bool, optional): If True, overwrite the existing data file. Default is False.

    Raises:
    ValueError: If the start angle is not within the range of 0 to 360 degrees.

    Returns:
    None
    """
    if not (0 <= start <= 360) or not (0 <= end <= 360) or not (0 <= step <= 360):
        raise ValueError('Start, end, and step, angles should be within 0 to 360 degrees!')
    measured_data = []

    total_steps = len(np.unique(np.arange(start, end + step, step) % 360)) ** 3
    progress = Progress(total_steps)

    progress.show_msg(message=f'Starting measurements.. Data will be saved to: {data_file}' )
    step_count = 0
    if not dry_run:
        progress.update(step_count, message=f"Move motor to start positions: {pos1}, {pos2}, {pos3}")
        drive_motor(start, ser1, tol, max_num_failure, kinesis_path)
        drive_motor(start, ser2, tol, max_num_failure, kinesis_path)
        drive_motor(start, ser3, tol, max_num_failure, kinesis_path)
    pos1, pos2, pos3 = start, start, start
    
    for pos1 in np.unique(np.arange(start, end + step, step) % 360):
        if not dry_run:
            drive_motor(pos1, ser1, tol, max_num_failure, kinesis_path)
        for pos2 in np.unique(np.arange(start, end + step, step) % 360):
            if not dry_run:
                drive_motor(pos2, ser2, tol, max_num_failure, kinesis_path)
            for pos3 in np.unique(np.arange(start, end + step, step) % 360):
                
                step_count += 1
                progress.update(step_count, message=f"Measuring at positions: {pos1}, {pos2}, {pos3}")
                if not dry_run:
                    drive_motor(pos3, ser3, tol, max_num_failure, kinesis_path)
                    wavelength, intensity = drive_spectrometer(integration_time, avaspecx64_dll_path)
                else:
                    wavelength, intensity = ['NA'], ['NA']
                measured_data.append([pos1, pos2, pos3, wavelength, intensity])
                # Save data every step
                if overwrite_datafile:
                    df_all = pd.DataFrame(measured_data, columns=['position1', 'position2', 'position3', 'wavelength', 'intensity'])
                    df_all.to_csv(data_file, index=False, mode='w', header=True)
                elif not os.path.exists(data_file):
                    new_entry = pd.DataFrame([measured_data[-1]], columns=['position1', 'position2', 'position3', 'wavelength', 'intensity'])
                    new_entry.to_csv(data_file, index=False, mode='w', header=True)
                else:
                    progress.show_msg(f"Warning: {data_file} exists; new data will be appended.")
                    new_entry = pd.DataFrame([measured_data[-1]], columns=['position1', 'position2', 'position3', 'wavelength', 'intensity'])
                    new_entry.to_csv(data_file, index=False, mode='a', header=False)
    progress.complete()
