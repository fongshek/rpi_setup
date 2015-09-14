#!/usr/bin/python

import time


class lcd1602:
    LCD_CLEARDISPLAY    = 0x01
    LCD_RETURNHOME      = 0x02
    LCD_ENTRYMODESET    = 0x04
    LCD_DISPLAYCONTROL  = 0x08
    LCD_CURSORSHIFT     = 0x10
    LCD_FUNCTIONSET     = 0x20
    LCD_SETCGRAMADDR    = 0x40
    LCD_SETDDRAMADDR    = 0x80

    def __init__(self,name,mode):
        self.name = name
        self.mode = mode
        self.on_update_io = None
        self.rs=0
        self.rw=0
        self.cs=0
        self.bl=0
        self.data=0x00
        
    def update_io(self,data,cs,rs,rw,bl):
        # call back function
        self.data = data
        self.rs = rs
        self.rw = rw
        self.cs = cs
        self.bl = bl
        self.on_update_io(self,data,cs,rs,rw,bl)        
     
    def init_4bitmode(self):
#        print ("Init 4bit mode")
        self.update_io(0x00,0,0,0,0)
        self.write_nibble(0x03)
        self.write_nibble(0x03)
        self.write_nibble(0x03)
        self.write_nibble(0x02)
        
        self.write_cmd(0b00000001)  # clear display
        self.write_cmd(0b00000010)  # return home
        self.write_cmd(0b00000110)  # set the entry mode 
        self.write_cmd(0b00001110)  # Display On / OFF
        self.write_cmd(0b00011100)  # Cursor / Display Shift
        self.write_cmd(0b00101000)  # Function set
                
    def write_nibble(self,val):
        self.update_io((val << 4) & 0xf0, 0, self.rs, self.rw, self.bl)
        time.sleep(0.001)
        self.update_io((val << 4) & 0xf0, 1, self.rs, self.rw, self.bl)   
        time.sleep(0.001)
        self.update_io((val << 4) & 0xf0, 0, self.rs, self.rw, self.bl)   
        time.sleep(0.001)

    def write_cmd(self,data):
#        print "write cmd"
        self.rs = 0
        self.write_nibble(data>>4)
        self.write_nibble(data&0x0f)

    def write_data(self,data):
#        print "write data"
        self.rs = 1
        self.write_nibble(data>>4)
        self.write_nibble(data&0x0f)
        
    def backlight(self, val):
        self.bl = val
        self.update_io(self.data,self.cs,self.rs,self.rw,val)  
        
    def write_string(self,x,y,istr):
#        print str(x) + "," + str(y) + " " + istr
        self.set_cursor(x,y)
        strArr = map(ord,istr)
        for ch in strArr :
            self.write_data(ch)
    
    def clear_display(self):
        self.write_cmd(0x01)

    def return_home(self):  
        self.write_cmd(0b00000010)
        
    def set_cursor(self,x,y):
#        print "Set Cursor Line " + str(x) + "," + str(y)
        if (x==0):
            AC = y
        else :
            AC = 0x40 + y

        self.write_cmd(0x80+AC)
        
    
    def test(self):
        print "Testing LCD1602"
        self.write_data(0x53)        
        

        
        