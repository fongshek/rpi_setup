#!/usr/bin/python

import smbus                    #sudo apt-get install python-smbus
import time

# General i2c device class so that other devices can be added easily
class i2c_device:
    def __init__(self, addr, port):
        self.addr = addr
        self.bus = smbus.SMBus(port)

    def write_byte(self, byte):
        self.bus.write_byte(self.addr, byte)

    def read_byte(self):
        return self.bus.read_byte(self.addr)

    def write_reg_data(self,reg,data):
        self.bus.write_byte_data(self.addr,reg,data)
        
    def read_reg_data(self,reg):
        return(self.bus.read_byte_data(self.addr,reg))

    def read_nbytes_data(self, data, n): # For sequential reads > 1 byte
        return self.bus.read_i2c_block_data(self.addr, data, n)

class pcf8574:

    PORT_VAL = 0x00
    DEBUG = 0

    def __init__(self, addr, port):
        self.i2c = i2c_device(addr, port)

    def read_port(self):
#        return self.i2c.read_byte()
        return (self.PORT_VAL)
        
    def write_port(self, data):
        self.PORT_VAL = data
        if (self.DEBUG):
            print "PORT VAL = " + format(self.PORT_VAL,'02X') + " " + format(self.PORT_VAL,'08b')
        return self.i2c.write_byte(data)

    def output_bit(self,pos,val):
        if (val ==0):
            self.clear_bit(pos)
        else:
            self.set_bit(pos)
    
    def set_bit(self,bit):
        reg_val = self.read_port()
        mask = 1<<bit
        reg_val = reg_val & (mask ^0xff)
        reg_val = reg_val | mask
        self.write_port(reg_val)
        
    def clear_bit(self,bit):
        reg_val = self.read_port()
        mask = 1<<bit
        reg_val = reg_val & (mask ^0xff)
        self.write_port(reg_val)        
        
    def test(self):
        print "test pcf8574"
        self.clear_bit(3);
        time.sleep(1)
        self.set_bit(3);


if (0) : 

    DEVICE_ADDRESS = 0x27      #7 bit address (will be left shifted to add the read write bit)
    print "init pcf8574 "
    myDevice = pcf8574(DEVICE_ADDRESS,1)
    myDevice.test();