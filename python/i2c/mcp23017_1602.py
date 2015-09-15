#!/usr/bin/python

import smbus                    #sudo apt-get install python-smbus
import time
from lcd_1602 import lcd1602
from mcp23017 import mcp23017

class mcp23017_1602:

    #B0  :   BUT0
    #B1  :   BUT1
    #B2  :   BUT2
    #B3  :   BUT3
    #B4  :   BUT4
    #B5  :   LED-G
    #B6  :   LED-R
    #B7  :   LED-B

    #A0  :   LCD1602-RS
    #A1  :   LCD1602-RW
    #A2  :   LCD1602-E
    #A3  :   LCD1602-D4
    #A4  :   LCD1602-D5
    #A5  :   LCD1602-D6
    #A6  :   LCD1602-D7
    #A7  :   LCD1602-A
    
    PIN_LED_R = 6
    PIN_LED_G = 5
    PIN_LED_B = 7
    
    REG_ADD_IODIRA      = 0x00
    REG_ADD_IODIRB      = 0x01
    REG_ADD_IPOLA       = 0x02
    REG_ADD_IPOLB       = 0x03
    REG_ADD_GPINTENA    = 0x04
    REG_ADD_GPINTENB    = 0x05
    REG_ADD_DEFVALA     = 0x06
    REG_ADD_DEFVALB     = 0x07
    REG_ADD_INTCONA     = 0x08
    REG_ADD_INTCONB     = 0x09
    REG_ADD_IOCON       = 0x0A
    REG_ADD_IOCON_      = 0x0B
    REG_ADD_GPPUA       = 0x0C
    REG_ADD_GPPUB       = 0x0D
    REG_ADD_INTFA       = 0x0E
    REG_ADD_INTFB       = 0x0F
    REG_ADD_INTCAPA     = 0x10
    REG_ADD_INTCAPB     = 0x11
    REG_ADD_GPIOA       = 0x12
    REG_ADD_GPIOB       = 0x13
    REG_ADD_OLATA       = 0x14
    REG_ADD_OLATB       = 0x15
    
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.mc23017 = mcp23017(self.addr,port)
        self.init_mcp23017()
        self.lcd1602 = lcd1602("LCD1602",0);
        self.lcd1602.on_update_io = self.on_update_1602IO
        self.lcd1602.init_4bitmode();

    def init_mcp23017(self):
        self.mc23017.write_reg(self.REG_ADD_IODIRA, 0b00000000)  # PORT_A all output
        self.mc23017.write_reg(self.REG_ADD_IODIRB, 0b00011111)  # PORT_B RGB as output , Button as input
        self.mc23017.write_reg(self.REG_ADD_GPPUA, 0b00000000)   # PORT_A Pull up
        self.mc23017.write_reg(self.REG_ADD_GPPUB, 0b00000000)   # PORT_B Pull up
        

    def on_update_1602IO(self,client,data,cs,rs,rw,bl):
#        print "update 1602IO from " + client.name 
        # Mapping IO PIN
        VAL = (data & 0xf0) >> 1
        if (bl):
            VAL = VAL | 0x80
        if (cs):
            VAL = VAL | 0x04
        if (rw):
            VAL = VAL | 0x02
        if (rs):
            VAL = VAL | 0x01
        self.mc23017.write_reg(self.REG_ADD_OLATA,VAL)       
     
    def led_r(self,val):
        if (val==1):
            self.mc23017.set_reg_bit(self.REG_ADD_OLATB,self.PIN_LED_R)
        else:
            self.mc23017.clear_reg_bit(self.REG_ADD_OLATB,self.PIN_LED_R)

    def led_g(self,val):
        if (val==1):
            self.mc23017.set_reg_bit(self.REG_ADD_OLATB,self.PIN_LED_G)
        else:
            self.mc23017.clear_reg_bit(self.REG_ADD_OLATB,self.PIN_LED_G)
        
    def led_b(self,val):
        if (val==1):
            self.mc23017.set_reg_bit(self.REG_ADD_OLATB,self.PIN_LED_B)
        else:
            self.mc23017.clear_reg_bit(self.REG_ADD_OLATB,self.PIN_LED_B) 
    
    def read_button(self):
        val = self.mc23017.read_reg(self.REG_ADD_GPIOB) & 0b00011111
#        print "read button " + format(val,'05b')
        return val
       
    def display_current_time(self):
        print "Display current time"
       
    def test(self):
        print ("testing mcp23017 + LCD1602 + RGB")

        if (0):
            self.led_r(1)
            time.sleep(0.01)
            self.led_r(0)
            time.sleep(1)
            
            self.led_g(1)
            time.sleep(0.01)
            self.led_g(0)
            time.sleep(1)
        
            self.led_b(1)
            time.sleep(0.01)
            self.led_b(0)
        
        self.lcd1602.backlight(1)
        self.lcd1602.clear_display()
        self.lcd1602.return_home()
        self.lcd1602.write_string(0,0,"MCP23017 - LCD ")
        self.lcd1602.write_string(1,0,"0123456789ABCDEF")
        self.lcd1602.set_cursor(0,100)
        
        print "Reading Buttons"
        while (1):
            val = self.read_button()
            tstr = format(val,'05b')
            self.lcd1602.write_string(1,0,"IN " + tstr + "          ")
            time.sleep(0.1)

if (0) : 

    DEVICE_ADDRESS = 0x20      #7 bit address (will be left shifted to add the read write bit)
    print "init mcp23017 lcd1602"
    myDevice = mcp23017_1602(DEVICE_ADDRESS,0)
#    myDevice.test();

    if (1):
        myDevice.display_current_time();

    if (0):
        myDevice.led_r(1)
        time.sleep(0.01)
        myDevice.led_r(0)
        time.sleep(0.5)
        
        myDevice.led_g(1)
        time.sleep(0.01)
        myDevice.led_g(0)
        time.sleep(0.5)
    
        myDevice.led_b(1)
        time.sleep(0.01)
        myDevice.led_b(0)
        time.sleep(0.5)
    
        myDevice.lcd1602.backlight(1)
        myDevice.lcd1602.clear_display()
        myDevice.lcd1602.return_home()
        myDevice.lcd1602.write_string(0,0,"MCP23017 - LCD ")
        myDevice.lcd1602.write_string(1,0,"0123456789ABCDEF")
        myDevice.lcd1602.set_cursor(0,100)
        
        print "Reading Buttons"
        while (1):
            val = myDevice.read_button()
            tstr = format(val,'05b')
            myDevice.lcd1602.write_string(1,0,"IN " + tstr + "          ")
            time.sleep(0.1)    
