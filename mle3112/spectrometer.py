"""
Author: Zeyu Deng
Email: dengzeyu@gmail.com
"""

from devices.Avaspec import Avaspec

def drive_spectrometer(integration_time:float = 100.0, 
                       avaspecx64_dll_path:str = 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll',
                       dry_run = False) -> tuple:
    """
    Drives the spectrometer to measure and return wavelength and data.

    This function initializes the Avaspec device, sets the integration time,
    retrieves raw data and wavelength information from the device, and 
    processes them into lists of floats.

    Args:
        integration_time (float, optional): The integration time in milliseconds. Default is 100 ms.
        avaspecx64_dll_path (str, optional): The path to the avaspecx64.dll file. Default is 'C:/AvaSpecX64-DLL_9.14.0.0/avaspecx64.dll'.
        dry_run (bool, optional): If True, the function will not actually drive the spectrometer. Default is False.

    Returns:
        tuple: A tuple containing two lists:
            - wavelength (list of float): The list of wavelength values.
            - data (list of float): The list of measured data values.
    """
    if dry_run:
        return [],[]
    else:
        device = Avaspec(avaspecx64_dll_path = avaspecx64_dll_path)
        device.set_integration_time(integration_time) # in ms
        data_raw = device.data()
        data = [float(i) for i in data_raw.split(",")]
        wavelength_raw = device.wavelength()
        wavelength = [float(i) for i in wavelength_raw.split(",")]
    return wavelength,data
