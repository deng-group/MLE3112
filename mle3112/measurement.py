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
                              max_num_failure:int=10)->None:
    """
    Perform measurements by driving a motor to specified positions and collecting data from a spectrometer.
    Parameters:
    serial_number (str): The serial number of the motor to be connected.
    start (float): The starting angle in degrees. Must be within 0 to 360 degrees.
    end (float): The ending angle in degrees.
    step (float): The step size in degrees for each measurement.
    data_file (str, optional): The name of the CSV file to save the measured data. Default is 'data.csv'.
    max_num_failure (int, optional): The maximum number of retries allowed for motor driving failures. Default is 10.
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
    drive_motor(position=start, serial_number=serial_number, tol=1e-3, max_num_failure=max_num_failure)
    for position in np.arange(start, end + step, step):
        print(f"Setting the position to: {position}")
        drive_motor(position=position, serial_number=serial_number)
        wavelength, intensity = drive_spectrometer()
        measured_data.append([position, wavelength, intensity])

    df = pd.DataFrame(measured_data, columns=['position', 'wavelength', 'intensity'])
    df.to_csv(data_file)

def measurement_three_filters(ser1:str, ser2:str, ser3:str, 
                              start:float, end:float, step:float,
                              data_file:str='data_three_filters.csv',
                              max_num_failure:int=10)->None:
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
    Raises:
    ValueError: If the start angle is not within the range of 0 to 360 degrees.
    Returns:
    None
    The function drives three motors to various positions within the specified range and step size.
    It then measures data using a spectrometer at each combination of positions and stores the results in a CSV file named 'data_three_filters.csv'.
    """
    if not (0 <= start <= 360) or not (0 <= end <= 360) or not (0 <= step <= 360):
        raise ValueError('Start, end, and step, angles should be within 0 to 360 degrees!')
    measured_data = []

    print(f'Setting the initial positions to {start}...')
    drive_motor(position=start, ser=ser1, tol=1e-3, max_num_failure=max_num_failure)
    drive_motor(position=start, ser=ser2, tol=1e-3, max_num_failure=max_num_failure)
    drive_motor(position=start, ser=ser3, tol=1e-3, max_num_failure=max_num_failure)

    for pos1 in np.arange(start, end + step, step):
        drive_motor(position=pos1, ser=ser1, tol=1e-3, max_num_failure=max_num_failure)
        for pos2 in np.arange(start, end + step, step):
            drive_motor(position=pos2, ser=ser2, tol=1e-3, max_num_failure=max_num_failure)
            for pos3 in np.arange(start, end + step, step):
                print(f"Setting the positions to: {pos1}, {pos2}, {pos3}")
                drive_motor(position=pos3, ser=ser3, tol=1e-3, max_num_failure=max_num_failure)

                wavelength, intensity = drive_spectrometer()
                measured_data.append([pos1, pos2, pos3, wavelength, intensity])
                measured_data.append([pos1, pos2, pos3, wavelength, intensity])
    df = pd.DataFrame(measured_data, columns=['position1', 'position2', 'position3', 'wavelength', 'intensity'])
    df.to_csv(data_file)
