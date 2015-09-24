
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
        

class max9611:
    CSA_DATA_BYTE_MSB_ADRR= 0x00
    CSA_DATA_BYTE_LSB_ADRR= 0x01
    RS_DATA_BYTE_MSB_ADRR= 0x02
    RS_DATA_BYTE_LSB_ADRR= 0x03
    OUT_DATA_BYTE_MSB_ADRR= 0x04
    OUT_DATA_BYTE_LSB_ADRR= 0x05
    SET_DATA_BYTE_MSB_ADRR= 0x06
    SET_DATA_BYTE_LSB_ADRR= 0x07
    TEMP_DATA_BYTE_MSB_ADRR= 0x08
    TEMP_DATA_BYTE_LSB_ADRR= 0x09
    CONTROL_REGISTER_1_ADRR= 0x0A
    CONTROL_REGISTER_2_ADRR= 0x0B   
   
    CSA     = 0
    RS      = 0
    OUT     = 0
    SET     = 0
    TEMP    = 0
    CTR     = 0
    
    def __init__(self, addr, port):
        self.i2c = i2c_device(addr, port)

    def hex2str(self,vals):
        a =""
        for data in vals:
            b = format(data,'02X') + " "
            a = a + b
        return a

    def read_all_reg(self):
        vals=[]
        for x in range(0,12):
            vals = vals + [self.i2c.read_reg_data(x)]
            
        self.CSA  = ((vals[0] << 8) + vals[1])>>4
        self.RS   = ((vals[2] << 8) + vals[3])>>4
        self.OUT  = ((vals[4] << 8) + vals[5])>>4
        self.SET  = ((vals[6] << 8) + vals[7])>>4
        self.TEMP = ((vals[8] << 8) + vals[9])>>4
        self.CTR  = (vals[10] << 8) + vals[11]        
        return vals  

    def set_mux_channel(self,ch):
        vals = self.read_all_reg();
        val = vals[10] & (0b11111000)
        val = val + (ch & 0x07)
        self.i2c.write_reg_data(self.CONTROL_REGISTER_1_ADRR,val)

    def test(self):
        print "max9611 Test"
        GAIN = [1,4,8]
        GAIN_SET = 0x00                     # 0 = 1x , 1=4x, 2 = 8x
        self.set_mux_channel(GAIN_SET)      # Set CS Gain to 1
        self.set_mux_channel(0x07)      # Auto Refresh all channel in 2mS
        vals = self.read_all_reg();
        print self.hex2str(vals)
        print "CSA = " + format(self.CSA,'04x') + " : " +format(float(self.CSA) / GAIN[GAIN_SET] * 13 /1000 ,'2.3f') + "mA"
        print "RS  = " + format(self.RS,'04x') + " : " + format(float(self.RS) *  57.3 /(2**12) ,'2.2f') + "v"
        print "OUT = " + format(self.OUT,'04x')
        print "SET = " + format(self.SET,'04x')
        print "TEMP= " + format(self.TEMP,'04x')+ " : " +format(float(self.TEMP) * 0.48 /8 ,'2.1f') + "c"
        print "CTR = " + format(self.CTR,'04x')
        

def main():
    DEVICE_ADDRESS = 0x70      #7 bit address (will be left shifted to add the read write bit)
    myDevice = max9611(DEVICE_ADDRESS,1)
    myDevice.test()


if __name__ == "__main__":
    main();
    







