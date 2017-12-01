# Development and and instructions of the Lund HPGe Scanning System #

This repository holds information regarding the development and instructions of the Lund HPGe Scanning System. Configuring DAQ and movement of the collimator can be found in another repository named _ScannerAnalysis_.

The _How to_ set up the system description is presented in `setting_up.pdf`. It comprises:
- 3D designs.
- Details on how the table and top plate was installed. 
- Screws and plates that were used.
- Details on the positioning system: linear units x2 and linear guide x1 and how those are mounted.
- How to connect the raspberry pi and the gertbot.
- Stepper motors.
- Cable connections from the gertbot to the stepper motors and the photosensors which act as endstops.
- Software documentation on how to move the collimator. 

The software to run the scanning system can be found in `atlundiumberry/`. 
The program should be run through the ScanningComputer which comprise the Raspberry Pi and Gertbot and is able to control the movement of the collimator. 

Other than that, the folder names should be rather explanatory. 

## TO DO ##

* Verify the viability to borrow ESS laser triangulation sensor to measure z-coordinate. 
* 
