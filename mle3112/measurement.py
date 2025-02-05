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
import itertools
import h5py

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
                              continue_from:list=[])->None:
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
    data_file (str, optional): The name of the CSV/HDF5 file to save the measured data. Default is 'data_three_filters.csv'.
    max_num_failure (int, optional): The maximum number of allowed failures for driving the motors. Default is 10.
    tol (float, optional): The tolerance for motor position errors. Default is 1e-2.
    integration_time (float, optional): The integration time in milliseconds for the spectrometer. Default is 100.0 ms.
    kinesis_path (str, optional): The path to the Kinesis software. Default is 'C:/Program Files/Thorlabs/Kinesis'.
    avaspecx64_dll_path (str, optional): The path to the avaspecx64.dll file. Default is 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll'.
    dry_run (bool, optional): If True, perform a dry run without actually driving the motors and spectrometer. Default is False.
    continue_from (list, optional): The starting positions for the motors. Default is [].

    Raises:
    ValueError: If the start angle is not within the range of 0 to 360 degrees.

    Returns:
    None
    """
    if not (0 <= start <= 360) or not (0 <= end <= 360) or not (0 <= step <= 360):
        raise ValueError('Start, end, and step, angles should be within 0 to 360 degrees!')

    total_steps = len(np.arange(start, end + step, step)) ** 3
    if not continue_from: # Start from the beginning
        progress = Progress(total_steps)
        step_count = 1
        progress.show_msg(message=f'Starting measurements.. Data will be saved to: {data_file}' )

    else:# Continue from a previous run
        positions = np.arange(start, end + step, step)        
        all_runs = list(itertools.product(positions, repeat=3))
        try:
            start_idx = all_runs.index(tuple(continue_from))
        except ValueError:
            raise ValueError("continue_from positions do not match any valid measurement run.")
        progress = Progress.from_current_measurement(start_idx=start_idx, 
                                                     total = len(all_runs),
                                                     save_log=True, 
                                                     log_filename="measurement_three_filters.log")
        step_count = start_idx+1
        progress.show_msg(message=f"Previous run interrupted at position: {continue_from}. Continuing from here..")

    if not continue_from: # drive all position to the initial position if not continue from a previous run
        start1, start2, start3 = start, start, start
    else:
        start1, start2, start3 = continue_from

    progress.show_msg(message=f"Move motor to start positions: {start1}, {start2}, {start3}")
    drive_motor(start1, ser1, tol, max_num_failure, kinesis_path, dry_run)
    drive_motor(start2, ser2, tol, max_num_failure, kinesis_path, dry_run)
    drive_motor(start3, ser3, tol, max_num_failure, kinesis_path, dry_run)

    if os.path.exists(data_file):
        progress.show_msg(message=f"Warning: {data_file} exists; new data will be appended.")

    if data_file.endswith('.csv'):
        save_format = 'csv'
    elif data_file.endswith('.hdf') or data_file.endswith('.h5'):
        save_format = 'hdf'
    else:
        raise ValueError("Invalid data file format. Choose either 'csv' or 'hdf'.")
        
    for pos1 in range(start1, end + step, step):
        drive_motor(pos1, ser1, tol, max_num_failure, kinesis_path, dry_run)
        for pos2 in range(start2 if pos1 == start1 else start, end + step, step):
            drive_motor(pos2, ser2, tol, max_num_failure, kinesis_path,dry_run)
            for pos3 in range(start3 if pos1 == start1 and pos2 == start2 else start, end + step, step):
                
                progress.update(step_count, message=f"Measuring at positions: {pos1}, {pos2}, {pos3}")
                drive_motor(pos3, ser3, tol, max_num_failure, kinesis_path,dry_run)
                wavelength, intensity = drive_spectrometer(integration_time, avaspecx64_dll_path,dry_run)
                current_data = [pos1, pos2, pos3, wavelength, intensity]
                # Save data for the current step without accumulating in a list
                if save_format == 'csv':
                    df_entry = pd.DataFrame([current_data], columns=['position1', 'position2', 'position3', 'wavelength', 'intensity'])
                    df_entry.to_csv(data_file, index=False, mode='a', header=False)

                elif save_format == 'hdf':
                    with h5py.File(data_file, 'a') as f:
                        try:
                            grp = f.create_group(f"measurement_{step_count}")
                            grp.create_dataset("position", data=[pos1, pos2, pos3])
                            grp.create_dataset("wavelength", data=wavelength)
                            grp.create_dataset("intensity", data=intensity)
                        except Exception as e:
                            progress.show_msg(f"Error saving data for step {step_count}: {e}, skip this data saving...")
                            pass

                
                step_count += 1
    progress.complete()
