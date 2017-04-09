A GPLv3 Python library to communicate with the Canberra/NRC ADM-300 Mutli-fuction Survey Meter.

Files:
- adm300comm.py - Library that communicates via serial with the ADM-300.
- adm300parse.py - Library that just parses output data from the ADM-300.
- \_\_init\_\_.py - Glue file for using this repository as a library.
- commTest.py - Tests communications with an ADM-300 and parses the serial data. This is an example of how to use the library to communicate as well.
- parseTest.py - Parser tests using strings captured from an ADM-300.
- LICENSE - A copy of the GPLv3 license.

Dependencies:
pyserial - A python serial communication library. It can be installed on Ubuntu systems using: sudo apt-get install python-serial, or can be installed from pip.

Limitations:
- Verifying data with the checksum is not yet supported as I'm not sure what sort of checksum the ADM-300 generates. Update the issue at: https://github.com/ThreeSixes/pyadm300/issues/4
- ADM-300 instruments that display readings in Sv will get incorrect readings until I have some data samples from units that read in Sv. Update the issue at: https://github.com/ThreeSixes/pyadm300/issues/2
- The library does not yet support configuring the alarm thresholds for dose rate and accumulated dose. https://github.com/ThreeSixes/pyadm300/issues/1
- The library may not work well with external probes until I can get some data sentences with probes connected. I only have the ADM-300 and no external Smart Probes to experiment with. If someone out there has external probes and wants to help out submit the raw sentences from the ADM-300 with the probe connected and the model of probe. https://github.com/ThreeSixes/pyadm300/issues/3

Providing output for expanding the software and parsing:
- adm300comm.setRawCallback(pprint) method can be used to dump the raw sentences from the ADM-300 for submitting them to me via the issue tracker at https://github.com/ThreeSixes/pyadm300/issues.

Serial connections to the ADM-300:
- The accessory connector for the ADM-300 is a Hirose "SR30-10PE-6P(74)" which can be found on mouser.com. Pin 1 on the connector is marked by the widest key on the connector.
- The target serial port can be specified when instanciating the class using the "dev" parameter in Windows or Linux.
- Pins 2, 3, and 5 of the ADM-300 accessory connector (white with 6 pins) are required for serial communication. Pins 2, 3, and 5 map directly to the pin numbers on a DB-9 connector.
- I attempted to connect a USB UART to the ADM-300 but it didn't work. A USB serial adapter did.
- The ADM-300 operates at 300 baud.
