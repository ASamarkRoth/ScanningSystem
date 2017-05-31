# End-stops linear units # 


In the second round after assistance of Mikael Elfman these were purchased:

5 st (OPB990T51Z): <https://www.elfa.se/sv/laesgaffel-18-mm-40-ma-30-ma-40-70-optek-opb990t51z/p/30009110?channel=b2b&price_afd=48.2&gclid=CjwKEAjwja_JBRD8idHpxaz0t3wSJAB4rXW5Xf4yJTT7-mz6sqe7KDXiuYXHgO5Zg-5TWpgMcBwXPRoCjnLw_wcB>
_Documentation_: <https://www.elfa.se/Web/Downloads/_t/ds/OPB960-990-series_eng_tds.pdf?mime=application%2Fpdf>
Code OPB9...: 

* 9 — Open (apertures visible), Wires 
* 0 — Buffer  Totem-Pole 
* T — Both (two mounting tabs) 
* 51 - aperture width
* Z = Wires only,  None for PCB leads 

Page 3: wire colour code. 
Page 4: Connection diagram
Page 5: Supply voltages

* Maximum diode current = 40 mA
* 4.5 V < V_CC < 16 V

** 330 Ohms ** resistor -> Diode current ~ 24 mA







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

