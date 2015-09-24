#!/usr/bin/python

import sys, getopt
from mcp23017_1602 import mcp23017_1602
from pcf8574_1602 import pcf8574_1602
from config import cConfig
import paho.mqtt.client as paho   # pip install paho-mqtt
import threading
from datetime import datetime
import time
import paho.mqtt.client as mqtt
import Queue

class mqtt_lcd_display:

    def __init__(self, name, config_file):
        self.name = name
        self.cfg = cConfig(config_file)
        self.parse_config();
        self.stop_print_service_flag = False
        self.myLCD = None
        self.mqtt = None
        self.stop_flag = False
        self.mqtt_msg_cnt = 0
        self.mqtt_msg_arr = []
        self.lcd_msg_q = Queue.Queue()
        
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
    
    def start_print_service(self):
        print "Starting lcd print service"
        if (self.lcd_module == "pcf8574_1602"):
            self.myLCD = pcf8574_1602(self.lcd_i2c_add,self.lcd_i2c_port)
        elif (self.lcd_module == "mcp23017_1602"):
            self.myLCD = mcp23017_1602(self.lcd_i2c_add,self.lcd_i2c_port)
        else:
            self.myLCD = None

        if (self.myLCD == None):
            sys.exit(0)
        
        self.myLCD.lcd1602.backlight(1)
        self.myLCD.lcd1602.clear_display()
        self.myLCD.lcd1602.return_home()   
        self.myLCD.lcd1602.write_string(0,0,"Starting") 
        self.myLCD.lcd1602.write_string(1,0,"LCD Service") 
        
        while 1:
            myTime = datetime.now()
            myRTC = myTime.strftime('%y:%m:%d:%H:%M:%S:%w').split(":")
#            print "current time is " + myTime.strftime('%y:%m:%d:%H:%M:%S')
            self.myLCD.lcd1602.write_string(0,0,"Current Time") 
            self.myLCD.lcd1602.write_string(1,0,myTime.strftime('%m:%d %H:%M:%S')) 
            if (self.stop_print_service_flag == True):
                break;
            time.sleep(1)        
        
    # The callback for when the client receives a CONNACK response from the server.
    def mqtt_on_connect(self,client, userdata, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(mqtt_topics)

    # The callback for when a PUBLISH message is received from the server.
    def mqtt_on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))  
        self.on_mqtt_message(str(msg.topic), str(msg.payload))
    #    process_mqtt_msg(str(msg.topic),str(msg.payload));
    
    def on_mqtt_message(self, topic, msg):
        self.mqtt_msg_cnt +=1
        if (topic == "sys/lcd_display"):
            if (msg[:1] == "#"):
                self.lcd_msg_q.put(msg[1:])
#        print "on_mqtt " + str(self.mqtt_msg_cnt) + ">" + topic + msg
#        print len(self.mqtt_msg_arr) , self.mqtt_msg_arr
#        if (len(self.mqtt_msg_arr) >1):
#            print self.mqtt_msg_arr[0]
    
    def start_mqtt_service(self):
        print "Starting mqtt subscribe"
        if (1):
            self.client = mqtt.Client()
            self.client.on_connect = self.mqtt_on_connect
            self.client.on_message = self.mqtt_on_message
            #Set userid and password
            self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
            self.client.connect(self.mqtt_host,self.mqtt_port,60)
            # Blocking call that processes network traffic, dispatches callbacks and
            # handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a
            # manual interface.
            self.client.loop_forever()        
    
    def start(self):
        
        print "Starting " + self.name
#        t1 = threading.Thread(target=self.start_print_service())
#        t2 = threading.Thread(target=self.start_mqtt_service())
#        t1.start()
#        t2.start()
        print "Exiting Main"
        
    def thread_1(self):
        print "Starting lcd print service"
        if (self.lcd_module == "pcf8574_1602"):
            self.myLCD = pcf8574_1602(self.lcd_i2c_add,self.lcd_i2c_port)
        elif (self.lcd_module == "mcp23017_1602"):
            self.myLCD = mcp23017_1602(self.lcd_i2c_add,self.lcd_i2c_port)
        else:
            self.myLCD = None

        if (self.myLCD == None):
            sys.exit(0)
        
        self.myLCD.lcd1602.backlight(1)
        self.myLCD.lcd1602.clear_display()
        self.myLCD.lcd1602.return_home()   
        self.myLCD.lcd1602.write_string(0,0,"Starting") 
        self.myLCD.lcd1602.write_string(1,0,"LCD Service") 
        while 1:
            myTime = datetime.now()
            myRTC = myTime.strftime('%y:%m:%d:%H:%M:%S:%w').split(":")
#            print myTime.strftime('%m:%d %H:%M:%S')
            while not self.lcd_msg_q.empty():
                lcd_msg = self.lcd_msg_q.get()
                lcd_msg += "\\n\\n"
                lcd_msgs = lcd_msg.split("\\n")
#               print "lcd display "  , lcd_msg , lcd_msgs
                self.myLCD.lcd1602.write_string(0,0,lcd_msgs[0]+"              ") 
                self.myLCD.lcd1602.write_string(1,0,lcd_msgs[1]+"              ")
                time.sleep(5)
                
            self.myLCD.lcd1602.write_string(0,0,"Current Time " + str(self.mqtt_msg_cnt)) 
            self.myLCD.lcd1602.write_string(1,0,myTime.strftime('%m:%d %H:%M:%S'))             
            if (self.stop_flag == True):
                break;
            time.sleep(1)
        print "Exiting thread_1"
        
    def get_key(self):
        response = raw_input("Press enter to stop")
        self.stop_flag = True        

    def run(self):
        print "Running " + self.name
        t1 = threading.Thread(target=self.thread_1)
#        t2 = threading.Thread(target=self.get_key)
        t1.start()
#        t2.start()
        print "Exiting Run"

            
    def test(self):
        print ("Test")
#        self.print_config();
        pass

# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(mqtt, userdata, rc):
    global myDevice, msg_cnt
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    topics = [ ("$SYS/#", 0),]
    msg_cnt += 1 
    topics = myDevice.mqtt_topics
#    print topics
    mqtt.subscribe(topics)
    myDevice.lcd_msg_q.put("MQTT Connected")

# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
    global myDevice, msg_cnt
#    print(str(msg_cnt) + ":" + msg.topic+" "+str(msg.payload))  
    msg_cnt += 1 
    myDevice.on_mqtt_message(msg.topic,str(msg.payload))  
    #    process_mqtt_msg(str(msg.topic),str(msg.payload));


 
def parse_argv(argv):
    lcd_config = 'mqtt_lcd_display.conf'
    lcd_message = ""
    try:
      opts, args = getopt.getopt(argv,"hc:m:") 
    except getopt.GetoptError:
      print 'mqtt_lcd_display.py -c <configfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'mqtt_lcd_display.py -c <configfile> '
         sys.exit()
      elif opt in ("-c", "--cfile"):
         lcd_config = arg
      elif opt in ("-m"):
         lcd_config = arg
    return (lcd_config)    

def main():
    global myDevice, client, msg_cnt
    config_file = parse_argv(sys.argv[1:])
    myDevice = mqtt_lcd_display("rpi-lcd",config_file,) 
    myDevice.print_config();
#    myDevice.start();
    myDevice.run();
    msg_cnt = 0
    if (1):
        print "Starting mqtt subscribe"
        client = mqtt.Client()
        client.on_connect = mqtt_on_connect
        client.on_message = mqtt_on_message
        #Set userid and password
        client.username_pw_set(myDevice.mqtt_username, myDevice.mqtt_password)
        client.connect(myDevice.mqtt_host,myDevice.mqtt_port,60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()            
    
    

if __name__ == "__main__":
    main();
