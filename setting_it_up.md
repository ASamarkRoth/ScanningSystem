# Setting up the scanning system #

###Threaded rods for fixing horisontal absorbers: ###
* 9 st - M4 (4 mm diameter) - length = 10 mm (Al base) + 70 mm (tungsten pieces = 2x19+2x13+3x2 = 70) ~ 80 mm
* <https://tools.se/produkterSe/fastteknik/industriinfastning/helgangad-stang/Gangstang-HGS-4.8-ANS-FZB-1411093-sv-se#v=SE-2605977>
* Malmö!

1. They will acquire the rods from central storage and text me Thursday 23/3 when they are in.
2. They are in our possession. They need to be produced to correct lengths!

### Screws for setting up LYCCA ring: ###

#### 12 cylindrical distance pins for LYCCA ring top <-> bottom - 2x12 M6 screws: ####

* From top: l = 10+10 = 20 mm, no protruding head
* <https://tools.se/produkterSe/fastteknik/industriinfastning/maskingangad-insexskruv/-SchaferPeters-A2-1411468-sv-se?categoryId=1073748027#v=SE-2027270>
* Lund!
* 
* From bottom: Drill small larger "holes" for head? -> l = 10 (Al base) + 10 (Plexi bottom) + 10 (in distance pin) = 30 mm
* <https://tools.se/produkterSe/fastteknik/industriinfastning/maskingangad-insexskruv/Insexskruv-MF6S-10.9-Forsankt-cyl.-huvud-ANS-FZB-1411311-sv-se>
* Lund!

#### 12 M3 screws for fixing each LYCCA module in the bottom plate ####

* Or is it possible with the final module configuration?
* l = 5 mm, head not very important!?
* This length does not exist!!
* WE HAVE IT IN_HOUSE!! This is true!

Dubbelhäftande tape to fix the 4 plastic boxes on the preamplifiers and the preamps to the bottom plate.

* <https://tools.se/produkterSe/fastighet/tejp-och-tatningslist/ovrigt-tejp-och-hallare/Mattejp-Universal-561705617156172-TESA-1405469-sv-se>


### Screws positioning system ###
* KK50-bottom <-> top plate: 6 st; HEAD=8x4, THRU=4.5 (no thread), thickness top plate = 10 mm

	* Final: 6 st, M4x25mm with M4 nut + M4 plate
* KK50-wagon <-> KK60-base: 

	* Wagon: 4 st; M4x0.7
	* KK60-base; 4?=2; HEAD 9.5x4.7, THRU=5.5

		* Final: 2 st M4x10mm. These have been optimised for the usage of the most threads in the KK50 wagon. M4x12mm was protruding! Fix these really tight as they need to sustain a large load. 

* Linear guide base <-> top-plate: 4 st; 7.5(measured~8)x5.3, THRU=4.5x(15-5.3=9.7), thickness top plate = 10 mm
	* Final: 4 st M4x25mm + M4 nut + M4 plate
* Linear guide wagon <-> KK60-base:

	* Wagon: M4 THRU
	* KK60-base; 4?=2; HEAD 9.5x4.7, THRU=5.5

		Final: M5x25mm. Nuts and plates were too tedious to install.

* Collimator arm <-> KK60-wagon:

	* Wagon: 4 st; M5x0.8
	* Thickness collimator arm = 10 mm

		* Final: M5x18 + plate M5. This needs confirmation!!!!
	
Remarks: Sadly no plates matches the space for the screw heads on the base of the linear units, unclear why this construction. 

### Mounting the wagon onto the linear guide ### 

1. First a plastic temporary filler was removed from underneath the oiled up wagon. 
2. The wagon needs to be slowly and carefully slid onto the guide. 
	
	* At first try 2 of the bearing balls were pushed out of their course. 
	* With a forceps (pincett) the cleaned balls were moved back. 
	* At second try it was successful. 
3. It is important that the guide is not fixed when run, as it needs to adapt its path to horisontal with the linear unit.

## Setting up the Raspberry Pi - Gertbot - stepper motors  ## 

1. Before booting the _Lundiumberry_ (Raspberry Pi 3, Model B installed with Raspbian): The Gertbot goes on top of the pins on the raspberry pi (only one way, otherwise it will hit ethernet connector)
2. The 2 phase stepper motors _17H261-02S/D_ are run with 1.2 A per phase. On the specification sheet it is stated that each phase has a resistance of 4 Ohm. According to  <http://compotech.se/blogg/2014/06/sa-valjer-du-ratt-spanning-din-stegmotordrift/> at least 4.8 V should be enough. 6 V was chosen as an objective. 
3. The Gertbot controller requires at least 8 V (8-18 V is recommended, see gertbot.com) to function. This has the consequence that it is necessary to connect a resistor in series with the phase of the stepper motors. A 15 V nominal input voltage was chosen which implies 6 Ohms resistors. 
4. 6.7 Ohms, 5.5 W resistors were connected via a connection board. Assuming a motor current of 1.2 A we need ~ 10 W resistors and these are getting somewhat too hot. 
5. The stepper motors were connected to the Gertbot as illustrated in the figures below!
6. Important convention: Red wire connected to A1 and striped red wire to A2, red wire connected to B1 and striped green wire to B2. Correspondingly for 2nd connected stepper motor. Important since this determines the polarity of rotation.

![Stepper motor connection](/home/anton/Pictures/DocumentationScanningSystem/20170512_161630.jpg)

![Stepper motor connection (close up)](/home/anton/Pictures/DocumentationScanningSystem/20170512_161651.jpg)

Configuring _Lundiumberry_ with Gertbot: 
	1. From <https://www.gertbot.com/download.html> download: 

		* Gertbot debug GUI, executable for Rasbian
		* Drivers for Python 3 (.py) 
		* Executable to enable the uart

	2. Follow: <https://www.isnr.de/images/Tools/low_cost_CT/How-to-set-up-the-Raspberry-Pi-and-Gertbot-as-a-tomography-controller-V2_30-08-2016.pdf>
	3. Execute GUI for debug with: `sudo ./gertbot` 
		
		* Click connect and one board (#3) should be found 
		* For channels 1 and 3 choose `Step gray off` and try it out. 
		* For details of the GUI: <https://www.gertbot.com/gbdownload/man/Gertbot_GUI.pdf>

### Activating end-stops ###



