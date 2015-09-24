
import smbus                    #sudo apt-get install python-smbus
import time
from random import randint
from datetime import datetime

# General i2c device class so that other devices can be added easily
class i2c_device:
    def __init__(self, addr, port):
        self.addr = addr
        self.bus = smbus.SMBus(port)

    def write_byte(self, byte):
        self.bus.write_byte(self.addr, byte)

    def read_byte(self):
        return self.bus.read_byte(self.addr)
        
    def write_word_data(self,cmd,val):
        return self.bus.write_word_data(self.addr,cmd,val)        

    def write_reg_data(self,reg,data):
        self.bus.write_byte_data(self.addr,reg,data)
        
    def read_reg_data(self,reg):
        return(self.bus.read_byte_data(self.addr,reg))
        

class ds1307:

    #define DS1307_ADDRESS              0x68 // this device only has one address
    #define DS1307_DEFAULT_ADDRESS      0x68

    #define DS1307_RA_SECONDS           0x00
    #define DS1307_RA_MINUTES           0x01
    #define DS1307_RA_HOURS             0x02
    #define DS1307_RA_DAY               0x03
    #define DS1307_RA_DATE              0x04
    #define DS1307_RA_MONTH             0x05
    #define DS1307_RA_YEAR              0x06
    #define DS1307_RA_CONTROL           0x07
    #define DS1307_RA_RAM               0x08

    #define DS1307_SECONDS_CH_BIT       7
    #define DS1307_SECONDS_10_BIT       6
    #define DS1307_SECONDS_10_LENGTH    3
    #define DS1307_SECONDS_1_BIT        3
    #define DS1307_SECONDS_1_LENGTH     4

    #define DS1307_MINUTES_10_BIT       6
    #define DS1307_MINUTES_10_LENGTH    3
    #define DS1307_MINUTES_1_BIT        3
    #define DS1307_MINUTES_1_LENGTH     4

    #define DS1307_HOURS_MODE_BIT       6 // 0 = 24-hour mode, 1 = 12-hour mode
    #define DS1307_HOURS_AMPM_BIT       5 // 2nd HOURS_10 bit if in 24-hour mode
    #define DS1307_HOURS_10_BIT         4
    #define DS1307_HOURS_1_BIT          3
    #define DS1307_HOURS_1_LENGTH       4

    #define DS1307_DAY_BIT              2
    #define DS1307_DAY_LENGTH           3

    #define DS1307_DATE_10_BIT          5
    #define DS1307_DATE_10_LENGTH       2
    #define DS1307_DATE_1_BIT           3
    #define DS1307_DATE_1_LENGTH        4

    #define DS1307_MONTH_10_BIT         4
    #define DS1307_MONTH_1_BIT          3
    #define DS1307_MONTH_1_LENGTH       4

    #define DS1307_YEAR_10H_BIT         7
    #define DS1307_YEAR_10H_LENGTH      4
    #define DS1307_YEAR_1H_BIT          3
    #define DS1307_YEAR_1H_LENGTH       4

    #define DS1307_CONTROL_OUT_BIT      7
    #define DS1307_CONTROL_SQWE_BIT     4
    #define DS1307_CONTROL_RS_BIT       1
    #define DS1307_CONTROL_RS_LENGTH    2

    #define DS1307_SQW_RATE_1           0x0
    #define DS1307_SQW_RATE_4096        0x1
    #define DS1307_SQW_RATE_8192        0x2
    #define DS1307_SQW_RATE_32768       0x3

    RTC_SEC = 0;
    RTC_MIN = 0;
    RTC_HRS = 0;
    RTC_DAY = 0;
    RTC_DATE = 0;
    RTC_MONTH = 0;
    RTC_YEAR = 0;
    
    def __init__(self, addr, port):
        self.i2c = i2c_device(addr, port)
        
    def prepare_rtc_vals(self,mytime):
        myRTC = mytime.strftime('%y:%m:%d:%H:%M:%S:%w').split(":")
#        print mytime.strftime('%y:%m:%d:%H:%M:%S:%w')
        
        self.RTC_SEC = (int(myRTC[5]) / 10) * 0x10 +  (int(myRTC[5]) % 10)
        self.RTC_MIN = (int(myRTC[4]) / 10) * 0x10 +  (int(myRTC[4]) % 10)
        self.RTC_HRS = (int(myRTC[3]) / 10) * 0x10 +  (int(myRTC[3]) % 10)
        self.RTC_DAY = int(myRTC[6]) + 1
        self.RTC_DATE = (int(myRTC[2]) / 10) * 0x10 +  (int(myRTC[2]) % 10)
        self.RTC_MONTH = (int(myRTC[1]) / 10) * 0x10 +  (int(myRTC[1]) % 10)
        self.RTC_YEAR = (int(myRTC[0]) / 10) * 0x10 +  (int(myRTC[0]) % 10)
#        print format(self.RTC_YEAR,'02x'),format(self.RTC_MONTH,'02x'),format(self.RTC_DATE,'02x'),format(self.RTC_HRS,'02x'),format(self.RTC_MIN,'02x'),format(self.RTC_SEC,'02x'),format(self.RTC_DAY,'02x')
        
        RTC_VALS=[self.RTC_SEC,self.RTC_MIN,self.RTC_HRS,self.RTC_DAY,self.RTC_DATE,self.RTC_MONTH,self.RTC_YEAR,0x00]
        return (RTC_VALS)
   
    def read_rtc(self):
#        print "reading rtc"
        vals=[]
        for x in range(0,8):
            vals = vals + [self.i2c.read_reg_data(x)]
        return vals        
    
    def write_rtc(self,RTC_VALS):
#        print "writing rtc"
#        print self.hex2str(RTC_VALS);
        i =0
        for val in RTC_VALS:
            self.i2c.write_reg_data(i,val)
            i = i+1

    def sync_rtc(self):
        RTC_VALS = self.prepare_rtc_vals(datetime.now())
        self.write_rtc(RTC_VALS)
        return (RTC_VALS)
 
    def hex2str(self,vals):
        a =""
        for data in vals:
            b = format(data,'02X') + " "
            a = a + b
        return a
        
    def format_rtc(self,vals):
#        print "format rtc " + self.hex2str(vals)
        myYear  = 10*(vals[6] >>4) + (vals[6] & 0x0f) 
        myMonth = 10*(vals[5] >>4) + (vals[5] & 0x0f) 
        myDate  = 10*(vals[4] >>4) + (vals[4] & 0x0f) 
        myHours = 10*(vals[2] >>4) + (vals[2] & 0x0f) 
        myMin   = 10*(vals[1] >>4) + (vals[1] & 0x0f) 
        mySec   = 10*(vals[0] >>4) + (vals[0] & 0x0f) 
        myDay   =  (vals[3] & 0x0f) 
        myStr   = format(myYear,'02d') + ":" + format(myMonth,'02d') + ":" +  format(myDate,'02d')
        myStr   = myStr + ":" +  format(myHours,'02d') + ":" +  format(myMin,'02d') + ":" +  format(mySec,'02d')
        myStr   = myStr + ":" +  format(myDay-1,'01d')
        return myStr
    
    def test(self):
        print "DS1307 Test"
        myTime = datetime.now()
        print "RTC PC     " + myTime.strftime('%y:%m:%d:%H:%M:%S:%w')
        RTC_VALS = self.prepare_rtc_vals(myTime)
        myRTC = self.read_rtc()
        print "RTC DS1307 " + self.format_rtc(myRTC);
       
def main():
    DEVICE_ADDRESS = 0x68      #7 bit address (will be left shifted to add the read write bit)
    myds1307 = ds1307(DEVICE_ADDRESS,1)
    if (0):
        RTC_SYNC = myds1307.sync_rtc();
        print "Sync PC RTC to DS1307" 
        print "RTC Sync   " + myds1307.format_rtc(RTC_SYNC)
    print "Compare PC / DS1307 RTC"
    myTime = datetime.now()
    print "RTC PC     " + myTime.strftime('%y:%m:%d:%H:%M:%S:%w')
    RTC_VALS = myds1307.prepare_rtc_vals(myTime)
    myRTC = myds1307.read_rtc()
    print "RTC DS1307 " + myds1307.format_rtc(myRTC);


if __name__ == "__main__":
    main();
 







