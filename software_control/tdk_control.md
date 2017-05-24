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

