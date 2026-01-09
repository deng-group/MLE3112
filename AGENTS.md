# AGENTS.md

This file provides guidelines for agentic coding assistants working on the MLE3112 repository.

## Project Overview

MLE3112 is a Python package for automated optical experiments, controlling motorized filters and spectrometers.

## Build, Lint, and Test Commands

### Installation
```bash
pip install -e .
```

### Testing
```bash
# Run all tests
python -m unittest discover -s tests -v

# Run a specific test file
python -m unittest tests.test_measurement -v
python -m unittest tests.test_data -v

# Run a specific test method
python -m unittest tests.test_measurement.TestMeasurement.test_single_filter_measurement -v
```

### Code Quality
This project does not have explicit linting/typechecking configurations. When making changes:
- Follow existing code style patterns
- Ensure tests pass before committing

## Code Style Guidelines

### Imports
Order imports: standard library → third-party → local
```python
import os
import time
import logging

import numpy as np
import pandas as pd
import h5py

from mle3112.motor import drive_motor
from mle3112.spectrometer import drive_spectrometer
```

### Type Hints
Use type hints for function signatures, especially for parameters and return types:
```python
def drive_motor(position: float,
                serial_number: str,
                tol: float = 1e-3,
                max_num_failure: int = 10,
                kinesis_path: str = 'C:/Program Files/Thorlabs/Kinesis',
                dry_run: bool = False) -> None:
```

### Naming Conventions
- **Classes**: PascalCase (`Measurement`, `Data`, `Progress`)
- **Functions/Methods**: snake_case (`drive_motor`, `perform_measurement`, `_move_motors_to_start`)
- **Private Methods**: underscore prefix (`_load_hdf_data`, `_initialize_measurement`)
- **Variables**: snake_case (`integration_time`, `wavelength_col_name`)

### Documentation
Use Google-style docstrings with Parameters, Raises, and Returns sections:
```python
def drive_motor(position: float, serial_number: str, tol: float = 1e-3) -> None:
    """
    Drives the motor to the specified position.

    Parameters:
        position (float): The target position to move the motor to.
        serial_number (str): The serial number of the motor controller.
        tol (float, optional): The tolerance for the motor position. Default is 1e-3.

    Raises:
        RuntimeError: If the motor fails to reach the position after max retries.

    Returns:
        None
    """
```

### Error Handling
- Use `ValueError` for parameter validation (e.g., invalid angle ranges)
- Use `RuntimeError` for operation failures
- Use try/except for retry logic with appropriate error messages
- Example:
```python
if not (0 <= start <= 360):
    raise ValueError('Start angle should be within 0 to 360 degrees!')
```

### Formatting
- Use 4 spaces for indentation
- Limit line length to ~80-100 characters
- Use blank lines between class methods and logical sections
- Don't add trailing whitespace

### Testing Guidelines
- Use `unittest` framework
- Test files: `tests/test_<module>.py`
- Test classes: `Test<ModuleName>`
- Test methods: `test_<specific_behavior>`
- Use `setUp()` for test initialization
- Use `tearDown()` for cleanup (remove temp files, etc.)
- Example:
```python
class TestData(unittest.TestCase):
    def setUp(self):
        self.data_handler = Data('test_data.h5')

    def test_add_measurement(self):
        self.data_handler.add_measurement(1, np.array([1.0]), np.array([400, 500]), np.array([10, 20]))

    def tearDown(self):
        if os.path.exists('test_data.h5'):
            os.remove('test_data.h5')
```

### Data Handling
- Use `h5py` for HDF5 file operations
- Use `pandas` for CSV operations
- Support both `.h5`/`.hdf5`/`.hdf` and `.csv` file formats
- Convert data to numpy arrays when working with numerical data
- Use `np.array()` and `.tolist()` for type conversion between storage and computation

### Progress Tracking
Use the `Progress` class for long-running measurements:
```python
progress = Progress(total_steps)
progress.update(current_step, message=f"Measuring at position {position}")
progress.complete()
```

### Hardware Integration
- Motor control: Use `drive_motor()` with retry logic via `max_num_failure` parameter
- Spectrometer: Use `drive_spectrometer()` for data acquisition
- Support dry_run mode for testing without hardware

## Key Dependencies
- `numpy`: Numerical operations and array handling
- `pandas`: Data manipulation and CSV I/O
- `h5py`: HDF5 file format support
- `matplotlib`: Plotting and visualization

## Project Structure
```
MLE3112/
├── mle3112/
│   ├── __init__.py
│   ├── measurement.py   # Main measurement orchestration
│   ├── motor.py        # Motor control functions
│   ├── spectrometer.py # Spectrometer control functions
│   ├── data.py         # Data handling (HDF5/CSV)
│   ├── plot.py         # Plotting utilities
│   ├── solution.py     # Example solutions
│   └── utils.py        # Progress tracking utilities
├── tests/
│   ├── test_measurement.py
│   └── test_data.py
├── examples/
│   ├── guide.ipynb
│   ├── tasks.ipynb
│   └── test.ipynb
└── pyproject.toml
```
