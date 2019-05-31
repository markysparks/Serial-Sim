# serial_sim
A Python utility application to store (in real time) serial sensor data from up to 4 serial ports and then play the data 
back over the same serial port at a later time. See the notes in the config file.


SETUP:

In the configuration file change the 'data collection' option to 'yes' to collect data over the serial ports or 'no' to
transmit already collected data back over the serial ports.

A PyInstaller generated Windows executable and config file can be found in the zip file.

NOTES:

In the configuration file 'serial ports pattern' option can be used to restrict what serial ports are used. If you 
connect a usb-multi-serial-port adapter you may want to restrict operation to only these ports

The first four serial ports matching the above pattern will be setup using the parameters specified for each port in
the config file and named Port_A, Port_B etc.

Received data will be stored in a text file named after the port it was received on e.g. Port_A.txt . Datalines from
these files will be used when in transmission mode to send data back across the appropriate port. The data files and
the config file must reside in the same directory as the program script/executable.

It is possible to run the whole utility and store the data files on a fast USB memory stick.

IMPORTANT - when in transmission mode a null modem cable or adapter must be used since the transmit source is in effect 
 a DTE device.
 
 
