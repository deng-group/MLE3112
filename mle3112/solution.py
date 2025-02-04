# How to drive the motor
"""
Author: Zeyu Deng (dengzeyu@gmail.com)

Here is the solution to the tasks in the MLE3112 course.
"""
import numpy as np
import pandas as pd
from mle3112.motor import drive_motor
from mle3112.spectrometer import drive_spectrometer
import matplotlib.pyplot as plt
import ast

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


def plot(data_file: str, positions:list) -> None:
    """
    Plots spectral data from a CSV file.

    This function reads a CSV file specified by the data_file parameter. It expects the CSV to contain columns such as 'intensity', 'wavelength', and 'position'.
    The 'intensity' and 'wavelength' columns are expected to be in string format that can be converted to Python objects using ast.literal_eval.
    For each unique position in the data, the function plots the spectral data, labeling the plot with the position value.
    It configures the plot with axis labels, a title, and a grid, then saves the plot as a pdf file named 'plot_<position>.pdf'.

    Parameters:
        data_file (str): Path to the CSV file containing the spectral data.
        positions (list): List of positions to plot.

    Returns:
        None
    """
    # read data
    df = pd.read_csv(data_file, index_col=0)
    df['intensity'] = df['intensity'].apply(lambda x: ast.literal_eval(x))
    df['wavelength'] = df['wavelength'].apply(lambda x: ast.literal_eval(x))

    # Plot the spectrum for a few positions

    for pos in positions:
        df_pos = df[df['position'] == pos].iloc[0]
        print(pos, df_pos)
        plt.figure(figsize=(5, 5))
        plt.plot(df_pos['wavelength'], df_pos['intensity'], label=f'Position {df_pos["position"]} degrees')

        plt.xlabel('Wavelength (nm)', fontsize=14)
        plt.ylabel('Intensity (a.u.)', fontsize=14)
        plt.title(f'Spectrum at Position {pos} degrees', fontsize=16)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        # Save the plot
        plt.savefig(f'plot_{pos}.pdf')
        plt.close()


def calculate_integrated_intensity(wavelength, intensity) -> None:
    """
    Calculate the integrated intensity from the wavelength and intensity data.
    Parameters:
    wavelength (List[float]): The list of wavelengths.
    intensity (List[float]): The list of intensities.

    Returns:
    float: The integrated intensity.
    """
    return np.trapz(y=intensity, x=wavelength)

def plot_integrated_intensity(data_file: str) -> None:
    """
    Plots integrated intensity and adsorptance from a CSV file containing spectral data.
    Parameters:
    data_file (str): Path to the CSV file containing the data.

    Returns:
    None
    """
    # read data
    df = pd.read_csv(data_file, index_col=0)
    df['intensity'] = df['intensity'].apply(lambda x: ast.literal_eval(x))
    df['wavelength'] = df['wavelength'].apply(lambda x: ast.literal_eval(x))

    # integrate wavelength
    integrated_intensity = [calculate_integrated_intensity(wavelength, intensity) for wavelength, intensity in zip(df['wavelength'], df['intensity'])]
    
    # Create the plot
    plt.figure(figsize=(5, 5))
    plt.plot(df['position'], integrated_intensity, 'o-', markersize=8, linewidth=2, label='Integrated Data')

    # Add legends for both y-axes
    plt.xlabel('Position (degrees)', fontsize=14)
    plt.ylabel('Integrated Data (a.u.)', fontsize=14)
    plt.title('Position vs Integrated Data', fontsize=16)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('integrated.pdf')