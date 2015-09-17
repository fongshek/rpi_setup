#!/usr/bin/python

import sys, getopt
from mcp23017_1602 import mcp23017_1602
from pcf8574_1602 import pcf8574_1602
from config import cConfig
import paho.mqtt.client as paho   # pip install paho-mqtt
from threading import Thread

class mqtt_lcd_display:

    def __init__(self, name, config_file):
        self.name = name
        self.cfg = cConfig(config_file)
        self.parse_config();
        
    def parse_config(self):
    #    print "parse config"
        lcd_modules = self.cfg.get('lcd_modules')
        lcd_index = int(self.cfg.get('lcd_module_index'))
        lcd_config = lcd_modules[lcd_index].split(",")

        self.lcd_module = lcd_config[0]
        self.lcd_i2c_add = int(lcd_config[1].replace("0x",""),16)
        self.lcd_i2c_port = int(lcd_config[2].replace("0x",""),16)
        
        self.mqtt_host=self.cfg.get('mqtt_broker') 
        self.mqtt_port=self.cfg.get('mqtt_port') 
        self.mqtt_username=self.cfg.get('mqtt_username') 
        self.mqtt_password=self.cfg.get('mqtt_password') 
        self.mqtt_topics=self.cfg.get('mqtt_topics') 
    
    def print_config(self):
        print self.lcd_module, self.lcd_i2c_add, self.lcd_i2c_port
        print self.mqtt_host, self.mqtt_port, self.mqtt_username, self.mqtt_password, self.mqtt_topics
    
    def start(self):
        print "Starting " + self.name
    
    def test(self):
#        self.print_config();
        pass

 
def parse_argv(argv):
    lcd_config = 'mqtt_lcd_display.conf'
    lcd_message = ""
    try:
      opts, args = getopt.getopt(argv,"hc:")
    except getopt.GetoptError:
      print 'mqtt_lcd_display.py -c <configfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'mqtt_lcd_display.py -c <configfile> '
         sys.exit()
      elif opt in ("-c", "--cfile"):
         lcd_config = arg
    return (lcd_config)    

def main():
    config_file = parse_argv(sys.argv[1:])
    myDevice = mqtt_lcd_display("rpi-lcd",config_file,) 
    myDevice.print_config();
    myDevice.start();

if __name__ == "__main__":
    main();
