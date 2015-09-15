#!/usr/bin/python

import time
import datetime
from mcp23017_1602 import mcp23017_1602

if (1) : 

    DEVICE_ADDRESS = 0x20      #7 bit address (will be left shifted to add the read write bit)
    print "init mcp23017 lcd1602"
    myDevice = mcp23017_1602(DEVICE_ADDRESS,0)
#    myDevice.test();

    if (1):
        myTime = datetime.datetime.now()
        myRTC = myTime.strftime('%y:%m:%d:%H:%M:%S:%w').split(":")
        
        myDevice.lcd1602.backlight(1)
        myDevice.lcd1602.clear_display()
        myDevice.lcd1602.return_home()
        myDevice.lcd1602.write_string(0,0,"Current time :")
        myTimeStr = myTime.strftime('%m%d %H:%M:%S')
        myDevice.lcd1602.write_string(1,0,myTimeStr)        

