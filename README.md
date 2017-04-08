A python library to communicate with the Canberra/NRC ADM-300 Mutli-fuction Survey Meter.

Files:
- adm300comm.py - Library that communicates via serial with the ADM-300.
- adm300parse.py - Library that just parses output data from the ADM-300.
- __init__.py - Glue file for using this repository as a library.
- parseTest.py - Parser tests using strings captured from an ADM-300.

Dependencies:
pyserial - A python serial communication library. It can be istalled on Ubuntu systems using: sudo apt-get install python-serial
