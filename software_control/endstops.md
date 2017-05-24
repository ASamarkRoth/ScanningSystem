# End-stops linear units # 

Purchased this: <https://cdn.sos.sk/productdata/dc/80/51538cd9/ktir-0621-ds.pdf>

Instructions on how to connect it:

* <https://bennthomsen.wordpress.com/engineering-toolbox/ti-msp430-launchpad/interfacing-a-photo-interrupter/>
* <http://www.utopiamechanicus.com/article/arduino-photo-interruptor-slotted-optical-switch/>

Not what is presented below!!!




Purchased: Photomicrosensor, transmissive sensing method, termination type - terminal type and mounting type - through hole

* Photomicrosensor (Transmissive) - EE-SX1018 from _Omron_.

* One LED (emitter) and one phototransistor on each side of the fork. 

* Need a limiting resistor (forward impedance of LED is "limitless")!
* Lower limit of Forward voltage LED: 1.2 V (specification sheet)
* Optimal forward current: 20 mA.
* R = (V_CC - V_F) /I_F, V_CC = supply voltage, V_F = forward voltage and I_F = forward current
* V_CC = 8V -> R = 8-1.2 / 20e-3 = 340 Ohm

Page 17 for circuit design: 

* Unclear what supply voltage needed for the phototransistor. 
* Seems proper to have an output resistor for the voltage to "lie over". There exists one at each pin of the gertbot EXT pins. 
* ...

## Questions ## 

* What ON/OFF currents?/voltages does the Gertbot react to? And what voltages should we supply? Different to the diode and the phototransistor?
* How do we deal with the leakage current in the phototransistor? Is it going to pose a problem?

