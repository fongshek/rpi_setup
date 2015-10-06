#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

class cMySql:
    conn = None
    cur = None
    conf = None
    
    def __init__(self, **kwargs):
		self.conf = kwargs
		self.conf["keep_alive"] = kwargs.get("keep_alive", False)
		self.conf["charset"] = kwargs.get("charset", "utf8")
		self.conf["host"] = kwargs.get("host", "localhost")
		self.conf["port"] = kwargs.get("port", 3306)
		self.conf["autocommit"] = kwargs.get("autocommit", False)
		self.connect()
            
    def connect(self):
	"""Connect to the mysql server"""
        try:
            self.conn = MySQLdb.connect(db=self.conf['db'], host=self.conf['host'],
                                        port=self.conf['port'], user=self.conf['user'],
                                        passwd=self.conf['passwd'],
                                        charset=self.conf['charset'])
            self.cur = self.conn.cursor()
            self.conn.autocommit(self.conf["autocommit"])
    #        print "connected to ", self.conf['host'], self.conf['db']
        except:
            print ("MySQL connection failed")
            raise

    def is_open(self):
		"""Check if the connection is open"""
		return self.conn.open

    def end(self):
		"""Kill the connection"""
		self.cur.close()
		self.conn.close()

    def query(self, sql, params = None):
    
        try:
            with self.conn:
                self.cur.execute(sql)
        except:
			print("Query failed")
			raise
        return self.cur

if (0):
    db = cMySql(
        host="localhost",
        db="mqtt_log",
        user="root",
        passwd="password",
        keep_alive=True # try and reconnect timedout mysql connections?
    )

    db.query("INSERT INTO `test`(`topic`, `message`) VALUES ('abc','123')");
