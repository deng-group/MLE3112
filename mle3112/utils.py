import time
import sys
import time
import logging

"""
Author: Zeyu Deng (dengzeyu@gmail.com)
"""

class Progress:
    """
    A class to track and display the progress of a task using logger.

    Attributes:
    -----------
    total : int
        The total number of steps or units of work to be completed.
    start_time : float
        The time when the progress tracking started.
    current : int
        The current progress in terms of steps or units of work completed.

    Methods:
    --------
    __init__(total):
        Initializes the Progress object with the total number of steps.
    update(progress, message=''):
        Updates the current progress and logs the progress status.
    _log_progress(elapsed_time, remaining_time, message):
        Logs the progress status including elapsed time and remaining time.
    complete():
        Marks the progress as complete and logs the final status.
    """
    def __init__(self, total, save_log=True, log_filename="measurement.log"):
        self.total = total
        self.start_time = time.time()
        self.current = 0
        self.logger = logging.getLogger('Progress')
        # Only add handlers if they haven't been added before.
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            consol_formatter = logging.Formatter('%(message)s')
            file_formatter = logging.Formatter('[%(asctime)s] %(message)s')
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(consol_formatter)
            self.logger.addHandler(ch)
            if save_log:
                fh = logging.FileHandler(log_filename, mode="a")
                fh.setFormatter(file_formatter)
                self.logger.addHandler(fh)
        
    def update(self, progress, message=''):
        self.current = progress
        elapsed_time = time.time() - self.start_time
        estimated_total_time = (elapsed_time / self.current) * self.total if self.current > 0 else 0
        remaining_time = estimated_total_time - elapsed_time
        self._log_progress(elapsed_time, remaining_time, message)

    def _log_progress(self, elapsed_time, remaining_time, message):
        progress_percentage = (self.current / self.total) * 100
        log_message = (
            f"{progress_percentage:.2f}% | {elapsed_time:.2f}s elapsed, "
            f"{remaining_time:.2f}s remaining | {message}"
        )
        self.logger.info(log_message)
    
    def show_msg(self, message):
        self.logger.info(message)

    def complete(self):
        elapsed_time = time.time() - self.start_time
        log_message = f"100.00% | {elapsed_time:.2f}s elapsed | 0.00s remaining | Task completed!"
        self.logger.info(log_message)