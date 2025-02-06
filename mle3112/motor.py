"""
Author: Zeyu Deng
Email: dengzeyu@gmail.com
"""

from devices.KDC101 import KDC101
import time

def drive_motor(position: float, serial_number: str, tol: float = 1e-3,
                max_num_failure:int=10, 
                kinesis_path:str = 'C:/Program Files/Thorlabs/Kinesis',
                dry_run = False)->None:
    """
    Drives the motor to the specified position.

    Parameters:
    position (float): The target position to move the motor to.
    serial_number (str): The serial number of the motor controller.
    tol (float, optional): The tolerance for the motor position. Default is 1e-3.
    max_num_failure (int, optional): The maximum number of allowed failures before giving up. Default is 10.
    kinesis_path (str, optional): The path to the Kinesis folder. Default is 'C:/Program Files/Thorlabs/Kinesis'.
    dry_run (bool, optional): For testing, if True, the motor will not be moved. Default is False.

    Raises:
    RuntimeError: If the motor fails to reach the position after the maximum number of retries.

    Returns:
    None
    """
    failed_counter = 0
    for attempt in range(max_num_failure):
        try:
            if not dry_run:
                _drive_motor(position=position, serial_number=serial_number, tol=tol, kinesis_path=kinesis_path)
            break
        except Exception as e:
            failed_counter += 1
            print(f'Error: {str(e)}. Failed {failed_counter}/{max_num_failure} times. Trying again ...')
            if failed_counter >= max_num_failure:
                raise RuntimeError(f"Cannot fix this error by rerunning the program for {failed_counter} times! I want to give up!")
            continue

def _drive_motor(position: float, 
                 serial_number: str, 
                 tol: float = 1e-3, 
                 kinesis_path = 'C:/Program Files/Thorlabs/Kinesis')->None:
    """
    Drives the motor to the specified position and waits until it reaches the desired tolerance.

    Args:
        position (float): The target position to move the motor to.
        serial_number (str): The serial number or identifier for the motor.
        tol (float, optional): The tolerance within which the motor should reach the target position. Defaults to 1e-3.
        kinesis_path (str, optional): The path to the Kinesis folder. Defaults to 'C:/Program Files/Thorlabs/Kinesis'.

    Returns:
        None

    Raises:
        Exception: If there is an issue with the motor or communication.
        
    Notes:
        This function uses the KDC101 device from the Kinesis library to control the motor.
        It continuously checks the motor's position and waits until it is within the specified tolerance.
        The function prints the motor's current position during the process and a final message once the target position is reached.
    """
    
    device = KDC101(serial_number, kinesis_path)
    device.set_position(position)

    while abs((position - device.position() + 180) % 360 - 180) > tol: # The motor position is in the range of 0 to 360 degrees
        time.sleep(0.5) # wait for 0.5 seconds
        print(f"Waiting for the motor ({serial_number}) to go to position: {position}, current position {device.position()}")
    time.sleep(1) # wait for 1 second
    print(f'Final motor: {serial_number} at position: {device.position()}')
    device.close()
