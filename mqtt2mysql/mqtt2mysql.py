#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m2m_config import Config
import paho.mqtt.client as paho   # pip install paho-mqtt
import socket
import signal
import logging
import sys, getopt
import json
import datetime
import time

import paho.mqtt.client as mqtt
from cMysql import cMySql

cf = None
db = None
mqtt_topics =''
mqtt_message_cnt=0
mqtt_max_msg_cnt=0
db_table =''

def print_config(config):
    print "logfile        : " ,config.get('logfile')       

    print "mqtt_clientID  : " ,config.get('mqtt_clientid')       
    print "mqtt_broker    : " ,config.get('mqtt_broker')       
    print "mqtt_port      : " ,config.get('mqtt_port')       
    print "mqtt_username  : " ,config.get('mqtt_username')       
    print "mqtt_password  : " ,config.get('mqtt_password')           
    print "mqtt_topics    : " ,config.get('mqtt_topics')       

    print "dbhost         : " ,config.get('dbhost')       
    print "dbport         : " ,config.get('dbport')       
    print "dbname         : " ,config.get('dbname')       
    print "dbtable        : " ,config.get('dbtable')       
    print "dbuser         : " ,config.get('dbuser')       
    print "dbpasswd       : " ,config.get('dbpasswd')       

    print "mqtt_max_msg_cnt       : " ,int(config.get('mqtt_max_msg_cnt'))       


def read_config(argv):
    config_file = 'm2m_default.conf'
    try:
      opts, args = getopt.getopt(argv,"hc:",["cfile="])
    except getopt.GetoptError:
      print 'mqtt2mysql.py -c <configfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'mqtt2mysql.py -c <configfile>'
         sys.exit()
      elif opt in ("-c", "--cfile"):
         config_file = arg

    return (Config(config_file))
#   print 'Config file is "', config_file

def db_insert(idb,topic,msg):
#    print str(mqtt_message_cnt),">" ,topic , str(msg)  
    sql = "INSERT INTO `"+ db_table +"`(`topic`, `message`) VALUES ('"+topic+"','"+msg+"')"
    idb.query(sql)

def app2logfile(filename,msg):
    fh = open(filename, 'a')
    fh.write(msg)    
   
def process_mqtt_msg(topic,msg):
#    print str(mqtt_message_cnt),">" ,topic , str(msg)  
    app2logfile("mqtt.log",topic+" "+str(msg) +"\r\n")
    db_insert(db,topic,msg)    
 
# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_topics)

# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))  
    global mqtt_message_cnt
    process_mqtt_msg(str(msg.topic),str(msg.payload));
    mqtt_message_cnt = mqtt_message_cnt +1
    if (mqtt_max_msg_cnt != -1):
    	if (mqtt_message_cnt >mqtt_max_msg_cnt) :
		print "Exit with Max msg Cnt ", str(mqtt_max_msg_cnt), str(mqtt_message_cnt)
        	client.disconnect()
        
   
def main():
    global cf, db,db_table, mqtt_topics, mqtt_max_msg_cnt
    cf = read_config(sys.argv[1:])    
#    print_config(cf)
    
    db = cMySql(
        host=cf.get('dbhost') ,
        db=cf.get('dbname'),
        user=cf.get('dbuser'),
        passwd=cf.get('dbpasswd'),
        keep_alive=True # try and reconnect timedout mysql connections?
        )
    db_table=cf.get('dbtable')
    ver = db.query("select version()")
    print ver.fetchone() , db_table
    
    mqtt_host=cf.get('mqtt_broker') 
    mqtt_port=cf.get('mqtt_port') 
    mqtt_username=cf.get('mqtt_username') 
    mqtt_password=cf.get('mqtt_password') 
    mqtt_topics=cf.get('mqtt_topics') 
    
    mqtt_max_msg_cnt = int(cf.get('mqtt_max_msg_cnt'))	

    client = mqtt.Client()
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message
    #Set userid and password
    client.username_pw_set(mqtt_username, mqtt_password)
    client.connect(mqtt_host,mqtt_port,60)
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()    
    print "Exiting Main"

if __name__ == "__main__":
    main();
