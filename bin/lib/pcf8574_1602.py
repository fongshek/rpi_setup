#!/usr/bin/python

from pcf8574 import pcf8574
from lcd_1602 import lcd1602
import time

        
class pcf8574_1602:
    # PC8574 PORT connected to LCD1602
    #P0  :   LCD1602-RS
    #P1  :   LCD1602-RW
    #P2  :   LCD1602-CS
    #P3  :   LCD1602-nK
    #P4  :   LCD1602-D4
    #P5  :   LCD1602-D5
    #P6  :   LCD1602-D6
    #P7  :   LCD1602-D7
    
    PIN_LCD1602_RS = 0
    PIN_LCD1602_RW = 1
    PIN_LCD1602_CS = 2
    PIN_LCD1602_K  = 3
    PIN_LCD1602_D4 = 4
    PIN_LCD1602_D5 = 5
    PIN_LCD1602_D6 = 6
    PIN_LCD1602_D7 = 7

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.pcf8574 = pcf8574(self.addr,port)
        self.pcf8574.write_port(0x00)
        self.lcd1602 = lcd1602("PCF8574",0);
        self.lcd1602.on_update_io = self.on_update_1602IO
        self.lcd1602.init_4bitmode();
 
    def on_update_1602IO(self,client,data,cs,rs,rw,bl):
    #    print "update 1602IO from " + client.name 
        # Mapping IO PIN
        VAL = data & 0xf0
        if (bl):
            VAL = VAL | 0x08
        if (cs):
            VAL = VAL | 0x04
        if (rw):
            VAL = VAL | 0x02
        if (rs):
            VAL = VAL | 0x01
        self.pcf8574.write_port(VAL)       
 
    def test(self):
        print "testing PCF8574 - LCD 1620"
        self.lcd1602.backlight(1)
        self.lcd1602.clear_display()
        self.lcd1602.return_home()
        self.lcd1602.write_string(0,0,"PCF8574 - LCD 1620")
        self.lcd1602.write_string(1,0,"0123456789ABCDEF")
        self.lcd1602.set_cursor(0,100)


def main():
    DEVICE_ADDRESS = 0x27      #7 bit address (will be left shifted to add the read write bit)
#   print "init pcf8574_1602 ....."
    myDevice = pcf8574_1602(DEVICE_ADDRESS,1)
    myDevice.lcd1602.backlight(1)
        
    myDevice.test()
    time.sleep(1)

    myDevice.lcd1602.clear_display()
    myDevice.lcd1602.return_home()
    myDevice.lcd1602.write_string(0,0,"Hello 111")
    for x in range (0,20):
        myDevice.lcd1602.write_string(1,0,"Hello " + str(x))
        myDevice.lcd1602.set_cursor(0,100)

if __name__ == "__main__":
    main();

