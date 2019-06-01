#!/usr/bin/python3
import os
import configparser
from time import sleep

import serial
import serial.tools.list_ports

version = '0.1'

# Set some default values and initialize serial ports lists
ports_list = []
serial_ports = []
# Following values will normally be read from the configuration file,
# these exists in the case no config file is found.
serial_port_str = 'com[0-9]'
port_timeout = 0.02
data_collection = True
tx_interval = 10

config = configparser.ConfigParser()

# Read in values from the configuration file (see config.ini for details)
if os.path.isfile('config.ini'):
    config.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'config.ini'))
    serial_port_str = config['mode']['serial_ports_pattern']
    tx_interval = config.getint('mode', 'tx_interval')
    data_collection = config.getboolean('mode', 'data_collection')


def start_up():
    """Start up Serial Simulator"""
    print('\r\n' + "Starting Serial Sim v" + str(version) + "......")
    serial_sim_setup = SerialSimSetup()
    serial_sim_setup.serial_port_handler()


class SerialSimSetup:

    def __init__(self):
        """Setup the available system serial ports using parameters specified
        in the config file (if available)"""
        print("\r\n" + "Setting up system serial ports..." + "\r\n")

        # Find all ports available matching regex search criteria. Note that
        # on the raspberry pi this search criteria will probably
        # be /dev/ttyUSB[0-9]+
        self.serial_port_str = config['mode']['serial_ports_pattern']
        self.serial_ports = [d for d, p, i in
                             serial.tools.list_ports.grep(
                                 self.serial_port_str)]
        self.serial_ports.sort()

        print("Available system serial ports matching config file pattern:")
        print(self.serial_ports)

        # Setup up to 4 serial ports A,B,C & D with desired parameters
        try:
            if len(self.serial_ports) > 0:
                self.port_A = serial.Serial(self.serial_ports[0],
                                            config.getint('port_A', 'baud'),
                                            config.getint('port_A', 'bytesize'),
                                            config['port_A']['parity'],
                                            config.getint('port_A', 'stopbits'),
                                            port_timeout)
                self.port_A.name = 'port_A'
                ports_list.append(self.port_A)

            if len(self.serial_ports) > 1:
                self.port_B = serial.Serial(self.serial_ports[1],
                                            config.getint('port_B', 'baud'),
                                            config.getint('port_B', 'bytesize'),
                                            config['port_B']['parity'],
                                            config.getint('port_B', 'stopbits'),
                                            port_timeout)
                self.port_B.name = 'port_B'
                ports_list.append(self.port_B)

            if len(self.serial_ports) > 2:
                self.port_C = serial.Serial(self.serial_ports[2],
                                            config.getint('port_C', 'baud'),
                                            config.getint('port_C', 'bytesize'),
                                            config['port_C']['parity'],
                                            config.getint('port_C', 'stopbits'),
                                            port_timeout)
                self.port_C.name = 'port_C'
                ports_list.append(self.port_C)

            if len(self.serial_ports) > 3:
                self.port_D = serial.Serial(self.serial_ports[3],
                                            config.getint('port_D', 'baud'),
                                            config.getint('port_D', 'bytesize'),
                                            config['port_D']['parity'],
                                            config.getint('port_D', 'stopbits'),
                                            port_timeout)
                self.port_D.name = 'port_D'
                ports_list.append(self.port_D)

        except serial.SerialException as error:
            print("Serial port setup error: " + error.__str__())

        print('\r\n' + 'Following serial ports setup:' + '\r\n')

        for seriport in ports_list:
            print(seriport.name + ' ' + (seriport.__str__()))

    @staticmethod
    def serial_port_handler():
        """If data collection mode is specified in the config file, loop
        through all the available, setup ports checking for available data
        lines. If data is available this is read and saved into the appropriate
        data file for the port.

        Otherwise in data transmission mode, check the data transmission
        interval and send data from the data files to the same port it was
        collected on at this interval."""

        # Data collection mode
        if data_collection:
            print("\r\n" + "Commencing data read cycle......" + "\r\n")

            while True:
                for seriport in ports_list:
                    try:
                        data_bytes = seriport.readline()
                        if data_bytes is not b'':
                            data_line = str(data_bytes)

                            print(seriport.name + ': ' + data_line)

                            with open(seriport.name + '.txt', 'a') as text_file:
                                print(data_line, file=text_file)

                    except serial.SerialException as error:
                        print("Serial port error: " + str(error))

        # Data transmission mode
        if not data_collection:

            # Line counter used to ensure the next line in the
            # file is transmitted
            n = 0

            print("\r\n" + "Commencing data transmission cycle......" + "\r\n")

            while True:
                for seriport in ports_list:
                    try:
                        if os.path.isfile(seriport.name + '.txt'):
                            with open(seriport.name + '.txt', 'r') as text_file:
                                print(text_file.name)
                                lines = text_file.readlines()
                                if len(lines) > n:
                                    next_line = lines[n]
                                    print(next_line)
                                    seriport.write(next_line.encode())
                    except serial.SerialException as error:
                        print("Serial port error: " + str(error))
                n += 1
                # Delay next transmission to serial ports by the interval
                # specified in the config file
                sleep(tx_interval)


if __name__ == '__main__':
    start_up()
