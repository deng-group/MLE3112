# How to Use Python to Run Automated Experiments
- Author: Zeyu Deng, with the help of Dmitrii Litvinov, and Sasani Jayawardhana
- Email: msedz@nus.edu.sg

## Pre-requisite
- A computer with Windows OS
- Miniconda or Anaconda installed (https://docs.anaconda.com/miniconda/install/)
- Visual Studio Code installed (https://code.visualstudio.com/Download)
- Git installed (https://git-scm.com/downloads/win)

## Install Thorlabs Kinesis
Install the Kinesis here: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=0
- You should install the x64 version

## Setup Virtal COM Port
This step is needed for using Python to connect to the motor. 

Plug-in the USB cable. Then open `Device Manager`, find the `APT USB Device` under `Universal Serial Bus Controller`, right click and select properties. Then go to `Advanced` tab and tick `Load VCP`. You should then unplug and plug-in the USB cable again to make the change effective.

## Confirm the Motor Is Working
Open `Kinesis`, then click `Move` for your motor, then set any number as position. Make sure it is moving as expected.

## Callibration
You should callibrate positions to zero for your motor. 

Open `Kinesis`, then click `Home` for your motor and make sure you get zero on both the motor and the display. 

## Install the Software to Drive the Spectrometer
You can download the software to drive the spectrometer from the Announcements email.

### Install Avasoft and AvaSpecDLL
- `Avasoft86Setup.exe`: Install Avasoft
- `AvaSpec-DLL/AvaSpecDLLsetup64.exe`: Install AvaSpecDLL

## Confirm the Spectrometer Is Working
Connect your computer to the spectrometer using the USB cable. Then open `Avasoft 8` and check if the spectrometer is working: Click `Start` and tick `Autoscale Y-axis`. You should see a spectrum.

## Install Python Packages
### Create a virtual environment
- Open `Anaconda Prompt`
- Run `conda create -n mle3112 python`
- Run `conda activate mle3112`

### Install the required packages
- Activate the virtual environment that we have created
```shell
conda activate mle3112
```
- Run the command below to install required packages, make sure you have installed [git for windows](#pre-requisite)
```shell
pip install git+https://github.com/deng-group/MLE3112.git
```
## Python Code to Drive Motor and Spectrometer
Please use the supplied code to drive the motor.