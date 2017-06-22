# Development and and instructions of the Lund HPGe Scanning System #

This repository holds all the information regarding the development and instructions of the Lund HPGe Scanning System. 

The _How to_ set up the system description is presented in `setting_up.pdf`. 

The software to run the scanning system can be found in `atlundiumberry/`. 
The program should be run through the ScanningComputer which comprise the Raspberry Pi and Gertbot and is able to control the movement of the collimator. 

Other than that, the folder names should be rather explanatory. 

## TO DO ##

* Test the swipe-scan procedure. 
* Configure Data AQuisition with the xy-scanning. I.e.
  * Do we get proper data?
  * How much data is sufficient for each point? 
  * How fine should the scanning grid be?
  * How do we maintain the data?
* Bias detector with the ISEG-control (set ramp speed).
* Perform a full surface scan of the detector. 
