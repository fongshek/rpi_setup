#!/usr/bin/python

import time
import os
import sys
from datetime import datetime
from datetime import timedelta

mypath = os.path.abspath(os.path.dirname(__file__))
iotpath = "/home/iot/bin"

class cCron:

    def __init__(self, name):
        self.name = name
        self.uptime = self.get_uptime()
        self.time = self.get_current_time()
        self.cron_1min = 1
        self.cron_2min = 1
        self.cron_5min = 1
        self.cron_1hr  = 1
        self.parse_cron()

    def get_uptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = int(float(f.readline().split()[0]))    
        days, remainder_hour = divmod(uptime_seconds,3600*24)
        hours, remainder_minutes = divmod(remainder_hour, 3600)
        minutes, seconds = divmod(remainder_minutes, 60)
        uptime = [uptime_seconds,days,hours,minutes,seconds]
        return uptime

    def get_current_time(self):
        myTime = datetime.now()
        myRTC = myTime.strftime('%y:%m:%d:%H:%M:%S').split(":")
        return myRTC

    def parse_cron(self):
        self.cron_1min = 0
        self.cron_2min = int(self.time[4]) % 2
        self.cron_5min = int(self.time[4]) % 5
        self.cron_1hr  = int(self.time[4])

    def test(self):
        print self.name, self.uptime , self.time


def cron_test():
#    print mypath
    script = "python " + iotpath + "/mqtt_lcd_publish.py  -m \"@ip\""
    os.system(script)

def cron_boot():
    script = "echo $(date +\"%y%m%d-%H%M%S\")  \"> execute > cron_boot\" | wall -n"
    os.system(script)
#    script = "python " + iotpath + "/mqtt_lcd_display.py  &"
#    os.system(script)
    
#    script = "python " + iotpath + "/mqtt2mysql.py  -c m2m_d2m.conf&"
#    os.system(script)

def cron_1min():
    script = "echo $(date +\"%y%m%d-%H%M%S\")  \"> execute > cron_1min\" | wall -n"
    os.system(script)
#    script = "python " + iotpath + "/mqtt_lcd_publish.py  -m \"@ip\""
#    os.system(script)
   
def cron_2min():
    script = "echo $(date +\"%y%m%d-%H%M%S\")  \"> execute > cron_2min\" | wall -n"
    os.system(script)
    
def cron_5min():
    script = "echo $(date +\"%y%m%d-%H%M%S\")  \"> execute > cron_5min\" | wall -n"
    os.system(script)
#    script = "sh " + iotpath + "/duckdns.sh"
#    os.system(script)

def cron_1hr():
    script = "echo $(date +\"%y%m%d-%H%M%S\")  \"> execute > cron_1hr\" | wall -n"
    os.system(script)

def main():
#    print mypath
    myCron = cCron("myCron")
#    myCron.test();
    par = sys.argv[1:]
    if (len(par)==0):
        if (myCron.cron_1min ==0):
            cron_1min()
        if (myCron.cron_2min ==0):
            cron_2min()
        if (myCron.cron_5min ==0):
            cron_5min()
        if (myCron.cron_1hr ==0):
            cron_1hr()        
    else :
        if (par[0] == "boot"):
            cron_boot()
        if (par[0] == "test"):
            cron_test()
            
            

if __name__ == "__main__":
    main();
