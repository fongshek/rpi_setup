#!/usr/bin/python

import sys, getopt
from mcp23017_1602 import mcp23017_1602
from pcf8574_1602 import pcf8574_1602
from config import cConfig


def write_message(config):
    print "writting  message to LCD"
#    config = parse_config(config)
#    print config.lcd_module, format(config.lcd_i2c_add,'02X'), config.lcd_i2c_port, " > " + config.lcd_message
    myDevice = None
    if (config.lcd_module == "pcf8574_1602"):
        myDevice = pcf8574_1602(config.lcd_i2c_add,config.lcd_i2c_port)
    elif (config.lcd_module == "mcp23017_1602"):
       myDevice = mcp23017_1602(config.lcd_i2c_add,config.lcd_i2c_port)
    else:
       myDevice = None

    if (myDevice == None):
        sys.exit(0)
    
    myDevice.lcd1602.backlight(1)
    myDevice.lcd1602.clear_display()
    myDevice.lcd1602.return_home()    
    messages = config.lcd_message.split("\\n")
#    print messages
    line = 0
    for msg in messages:
        if (line <2):
            myDevice.lcd1602.write_string(line,0,msg)    
            print msg
        line = line + 1
    myDevice.lcd1602.set_cursor(0,100)
    
def parse_config(config):
#    print "parse config"
    lcd_modules = config.get('lcd_modules') 
    lcd_index = int(config.get('lcd_module_index'))
    lcd_config = lcd_modules[lcd_index].split(",")
    config.lcd_module = lcd_config[0]
    config.lcd_i2c_add = int(lcd_config[1].replace("0x",""),16)
    config.lcd_i2c_port = int(lcd_config[2].replace("0x",""),16)
    if (config.lcd_message==""):
        config.lcd_message = config.get('lcd_message')
    return (config)

    
def print_config(config):
    print "ConfigFile   : " ,config.get('name')       
    print "lcd_index    : " ,config.get('lcd_module_index')    
    print "lcd_modules  : " ,config.get('lcd_modules') 
    print "lcd_message  : " ,config.get('lcd_message')  
    lcd_modules = config.get('lcd_modules') 
    lcd_index = int(config.get('lcd_module_index'))
    print "selected_lcd : " ,lcd_modules[lcd_index]  
    print "lcd_message1 : " ,config.lcd_message 
 
def read_config(argv):
    lcd_config = 'lcd_module.conf'
    lcd_message = ""
    try:
      opts, args = getopt.getopt(argv,"hc:m:")
    except getopt.GetoptError:
      print 'lcd_displayEx.py -c <configfile> -m <message>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'lcd_displayEx.py -c <configfile> -m <message>'
         sys.exit()
      elif opt in ("-c", "--cfile"):
         lcd_config = arg
      elif opt in ("-m"):        
         lcd_message = arg

    lCfg = cConfig(lcd_config)
    lCfg.lcd_message = lcd_message
    return (lCfg)    

def main():
    global cf
    cf = parse_config(read_config(sys.argv[1:]))   
#    print_config(cf) 
    write_message(cf)

if __name__ == "__main__":
    main();
