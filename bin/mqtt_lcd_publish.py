#!/usr/bin/python

# Copyright (c) 2014 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution. 
#
# The Eclipse Distribution License is available at 
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation

# This shows an example of using the publish.single helper function.

import sys, getopt
import paho.mqtt.publish as publish
from urllib2 import urlopen

class cMqtt_lcd_publish:
    def __init__(self, name):
        self.name = name;
        self.host = "fs-server-cb.duckdns.org"
        self.username = "fongshek"
        self.password = "Fm12345"
        self.topic = "sys/lcd_display"
        self.msg = "#Hello World\\nLine 2"
    
    def publish_lcd_msg(self,msg):
        publish.single(self.topic,msg,hostname=self.host,port=1883,auth={'username':self.username, 'password':self.password})        

    def public_myip(self):
        my_ip = urlopen('http://ip.42.pl/raw').read()
        self.publish_lcd_msg("#IP:" + my_ip)
        print my_ip

    def publish_msg(self,msg):
        if (msg[:1]=="#"):
            self.publish_lcd_msg(self.msg)
        elif (msg == "@ip"):
            self.public_myip()
        else :
            print msg
        pass
   
    def test(self):
        self.publish("#Hello World\\nHello 12345")


def parse_argv(argv):
    msg = "#Hello World\\nTest message"
    try:
      opts, args = getopt.getopt(argv,"hc:m:") 
    except getopt.GetoptError:
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         sys.exit()
      elif opt in ("-m"):
         msg = arg
    return (msg)    


def main():
    msg= parse_argv(sys.argv[1:])
    myDevice = cMqtt_lcd_publish("myLCD")
    myDevice.publish_msg(msg);
    

if __name__ == "__main__":
    main();
    

