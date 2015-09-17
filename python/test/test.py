
import threading

class myClass:
    def __init__(self):
        self.on_message = None
        print "Init myClass"
        
    def _handle_on_message(self, message):
        self.on_message(self, message)
        
            
        
    def test(self):
        self.on_message(self,"Hello")

def on_message(client, msg):
    print "On message received " + msg

print "Test start"
        
myClass1 = myClass()
myClass1.on_message = on_message
myClass1.test();


