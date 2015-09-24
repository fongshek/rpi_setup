
import smbus                    #sudo apt-get install python-smbus
import time
from random import randint

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
        

class at24c32:
    WRITE_CYCLE_TIME = 0.005    # 5mS
    def __init__(self, addr, port):
        self.i2c = i2c_device(addr, port)
        self.addr = addr 
        
    def read_byte(self):
        return self.i2c.read_byte()        
        
    def random_read_byte(self, add):
        self.i2c.write_reg_data((add>>8), add & 0xff)   # write address pointer
        return self.i2c.read_byte()
        
    def random_read_bytes(self, add,len):
        self.i2c.write_reg_data((add>>8), add & 0xff)   # write address pointer
        vals = []
        for x in range (0,len):
            vals = vals + [self.i2c.read_byte()]
        return vals

    def random_write_byte(self, add, data):
        vals = [add&0xff,data]
        self.i2c.bus.write_i2c_block_data(self.addr,add>>8,vals)  
        time.sleep(self.WRITE_CYCLE_TIME)
        
    def random_write_bytes(self, add, bytes):
        if (len(bytes) <= 31) :
            vals = [add>>8] + [add&0xff] + bytes
            self.i2c.bus.write_i2c_block_data(self.addr,vals[0],vals[1:])  
            time.sleep(self.WRITE_CYCLE_TIME)
        else :
            vals = [add>>8] + [add&0xff] + bytes
            self.i2c.bus.write_i2c_block_data(self.addr,vals[0],vals[1:33])  
            time.sleep(self.WRITE_CYCLE_TIME)
            vals = [(add+31)>>8] + [(add+31)&0xff] + bytes[31:]
            self.i2c.bus.write_i2c_block_data(self.addr,vals[0],vals[1:])  
            time.sleep(self.WRITE_CYCLE_TIME)
    
    def fill_all(self,val):
        vals=[]
        for x in range (0,32):
            vals = vals + [val]
        
        for x in range (0,128):
            self.random_write_bytes(x*32,vals)
    
    def dump_all(self):
        str = ""
        for x in range(0,128):
            str = str + self.dump_page(x) + "\r\n"
        return (str)
        
    def dump_page(self, page):
        vals = self.random_read_bytes(page * 32,32)
        return (format(page*32,'04X') + " : " + self.hex2str(vals))
        
    def hex2str(self,vals):
        a =""
        for data in vals:
            b = format(data,'02X') + " "
            a = a + b
        return a
    
    def test(self):
        print "AT24c32 Test"
        add = 0x0000;
        vals=[]
        for x in range (0,32):
            vals = vals + [randint(0,255)]
        print "Writting " + self.hex2str(vals)
        self.random_write_bytes(add,vals)
        vals = self.random_read_bytes(0x00,32)
        print "Reading  " + self.hex2str(vals)      


def main():
    DEVICE_ADDRESS = 0x50      #7 bit address (will be left shifted to add the read write bit)
    my24c32 = at24c32(DEVICE_ADDRESS,1)
    my24c32.fill_all(0xFF);
    my24c32.test();
    print "Dump all"
    print my24c32.dump_all();


if __name__ == "__main__":
    main();
    

