# End-stops linear units # 

Purchased: Photomicrosensor, transmissive sensing method, termination type - terminal type and mounting type - through hole

* Photomicrosensor (Transmissive) - EE-SX1018 from _Omron_.

* One LED (emitter) and one phototransistor on each side of the fork. 

* Need a limiting resistor (forward impedance of LED is "limitless")!
* Lower limit of Forward voltage LED: 1.2 V (specification sheet)
* Optimal forward current: 20 mA.
* R = (V_CC - V_F) /I_F, V_CC = supply voltage, V_F = forward voltage and I_F = forward current

Page 17 for circuit design: 

## Questions ## 

* What ON/OFF currents?/voltages does the Gertbot react to? And what voltages should we supply? Different to the diode and the phototransistor?
* How do we deal with the leakage current in the phototransistor? Is it going to pose a problem?
