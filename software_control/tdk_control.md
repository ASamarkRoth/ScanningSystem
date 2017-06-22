# TDK-Lambda power supply remote control #

**Our version: ** Gen 50-30

Remote control via RS232 remote control. Need connector as presented in fig. 7-3 in manual. 

Purchased this: <https://www.elfa.se/en/adaptor-sub-male-to-rj45-9p-mh-connectors-da9-pmj8/p/30036055?q=db9+connector&filter_Termination=plug-in&filter_categoryCodePathROOT%2Fcat-L2D_379527=cat-DNAV_0301&filter_categoryCodePathROOT=cat-L2D_379527&page=2&origPos=40&origPageSize=25&simi=85.76>

Cabled it from this guide: <https://www.usconverters.com/downloads/support/db9_rj45_assembeling_guide.pdf> and the table with colour + the scheme presented in the power supply manual. 

TDK Lambda proposes: 

* RS232 interface cable. <http://www.conrad.com/ce/en/product/515782/TDK-Lambda-ACC-GENZ-232-9-Z-232-9-RS232-Interface-Cable-For-Z-Genesys-Laboratory-Power-Supplies-Compatible-with-Z-Ge>
* USB adapter. <http://www.datatec.de/TDK-Lambda-Digitus-Adapter.htm>

## Working config. ## 

The RJ45 - DB9 adapter was connected with the three cables indicated in the TDK Lambda manual. Correct connection was ensured via buzzing. It turned out that the colour scheme vs. pin was inverted (or somehow the cable was flipped). Thus the following was connected: 

* Orange to DB9 2
* Blue to DB9 3
* White to DB9 5

* OBS: use the left-bottom most usb-connection, otherwise it won't work!

**GUI**:

* <https://www.de.tdk-lambda.com/technical-centre/software-tools.aspx>
* Genesys and then download "Genesys™ Drivers - GEN Control"
* For manual - see unzipped folder. 

## Configuring on Linux ##

(Drivers are useless as they assume LAN communication: <http://www.us.tdk-lambda.com/HP/product_html/Drivers/drivers_8.htm>, should be bookmarked)

_Useful commands_: <https://www.cyberciti.biz/faq/find-out-linux-serial-ports-with-setserial/>

`stty` use this for: "Open and use the specified DEVICE instead of stdin.".

1. Devices are: `/dev/ttyS0` and 0 = COM1, ... For USB-port -> ttyUSB0
2. Nice manual for `stty`: <https://www.esrl.noaa.gov/gmd/dv/hats/cats/stations/qnxman/stty.html>

**Interesting on how to send data (did not manage to get it work though):** <https://unix.stackexchange.com/questions/117037/how-to-send-data-to-a-serial-port-and-see-any-answer>

_Setting baud rate:_ `stty -F /dev/ttyS0 9600`

**Might be of interest (GTKTERM):** <http://elinux.org/Communicate_with_hardware_using_USB_cable_for_Ubuntu>

**USB-interface TDK-Lambda**: <https://www.us.tdk-lambda.com/hp/pdfs/Product_manuals/Genesys%20USB%20User%20Manual.pdf>

##Setting up ##
**Following this:**  <https://unix.stackexchange.com/questions/117037/how-to-send-data-to-a-serial-port-and-see-any-answer>

1. **OBS ensure everything is connected!**
1. `dmesg | grep tty` - checks serial port connection. Here you get `ttyUSB2` @ebbe and seemingly `ttyUSB0` @lundiumberry.
2. `sudo chmod o+rw /dev/ttyUSB2` - change read and writing permissions.
3. `stty -F /dev/ttyUSB2 9600 cs8 -cstopb -parenb -echo` - Setting up TDK-Lambda communication protocol (see below). `-echo` is needed @lundiumberry since otherwise the machine tries to read commands all the time. 
4. Open two terminal tabs and read in one and write in the other:
5. _Read_: `cat < /dev/ttyUSB2`
5. _Write_: `echo -ne 'OUT 1\015' > /dev/ttyUSB2` where `\015` mirrors the user hitting _enter_.

* `stty -a -F /dev/ttyUSB0` outputs current device settings (check for the ones given in point 3). 

_According to manual_:

* Baud rate: 9600
* Data bits: 8
* Parity: None
* Stop bits: 1
* Flow control: None

**-> stty command**: `stty -F /dev/ttyUSB2 9600 cs8 -cstopb`. In order: baud rate, data bits and stop bits. Correct? Don't do anything for parity and flow control?
The following was also tried: `stty -F /dev/ttyUSB2 9600 cs8 -cstopb -parenb`

Tried:

1. Added `-crtscts -ixon` -> still not working. Tried to disable flow control as some pointed out.

### Screen ###

_How to send commands_: <http://www.linuxquestions.org/questions/linux-software-2/how-to-send-a-command-to-a-screen-session-625015/>
<https://pixhawk.ethz.ch/tutorials/serial_terminal>
Setup was tried with: `screen -S tdk /dev/ttyUSB2 9600,cs8,-parentb,-cstopb,-parenb`
`screen -d -m -S tdk /dev/ttyUSB2 9600,cs8,-parentb,-cstopb,-parenb`
It worked with these settings, however not with commands ...

_Minicom_: also tried, real sweet for port settings.

* This worked ... <https://askubuntu.com/questions/805262/cannot-send-at-commands-in-minicom>

Tried _PUTTY_ on windows and that worked. OBS need to force read and echo!

## To-do ##

1. Make a script which can be invoked from an SSH-session. It should:
	
	* Set output voltage to ~8V, and switch output ON/OFF. 
	* Read the current outputs; voltage and current. It should work as a check from the master that everything is fine.
