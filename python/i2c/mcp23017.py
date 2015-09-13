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

class mcp23017:

    def __init__(self, addr, port):
        self.i2c = i2c_device(addr, port)

    def read_reg(self, reg):
        return self.i2c.read_reg_data(reg)
        
    def write_reg(self, reg, data):
        return self.i2c.write_reg_data(reg,data)

    def set_reg_bit(self,reg,bit):
        reg_val = self.read_reg(reg)
        mask = 1<<bit
        reg_val = reg_val & (mask ^0xff)
        reg_val = reg_val | mask
        self.write_reg(reg,reg_val)
        
    def clear_reg_bit(self,reg,bit):
        reg_val = self.read_reg(reg)
        mask = 1<<bit
        reg_val = reg_val & (mask ^0xff)
        self.write_reg(reg,reg_val)        
        
    def print_all_reg(self):
        a =""
        for x in range(0,0x15+1):
            data = self.read_reg(x)
            b = format(data,'02X') + " "
            a = a + b
            if ((x==15) or (x==7)):
                a = a + ":"
        print a          
        
    def test(self):
        print "MCP23017 Test"
        self.IODIRA = 0x00;
        self.IODIRB = 0x00;
        self.write_reg(0x00, self.IODIRA)
        self.write_reg(0x01, self.IODIRB)
        self.write_reg(0x0C, self.IODIRA)
        self.write_reg(0x0D, self.IODIRB)
        self.write_reg(0x15, 0xff)
        self.write_reg(0x15, 0x00)

        self.set_reg_bit(0x15,7)
        time.sleep(0.01)
        self.clear_reg_bit(0x15,7)
        time.sleep(1)
        
        self.set_reg_bit(0x15,6)
        time.sleep(0.01)
        self.clear_reg_bit(0x15,6)
        time.sleep(1)
    
        self.set_reg_bit(0x15,5)
        time.sleep(0.01)
        self.clear_reg_bit(0x15,5)
        self.write_reg(0x15, 0x00)


if (1) : 

    DEVICE_ADDRESS = 0x20      #7 bit address (will be left shifted to add the read write bit)
    print "init mcp23017 "
    myDevice = mcp23017(DEVICE_ADDRESS,0)
    myDevice.test();