import threading
import time

class DomainOperations:
    def __init__(self, domain):
        self.domain = domain
        self.domain_ip = ''
        self.website_thumbnail = ''
        self.stop_flag = False

    def resolve_domain(self):
        #resolve domain to ipv4 and save to self.domain_ip
        self.domain_ip="127.0.0.1"
        while 1:
            print "resolving domain ..."
            if (self.stop_flag == True):
                break;
            time.sleep(1)
        print "Exiting resolving domain"

    def generate_website_thumbnail(self):
        #generate website thumbnail and save the url to self.website_thumbnail
        self.website_thumbnail = "Hall"    
        while 1:
            print "generate website thumbnail  ..."
            time.sleep(1.5)
            if (self.stop_flag == True):
                break;            
        print "Exiting generate website thumbnail"
        
    def get_key(self):
        response = raw_input("Press any key to stop")
        self.stop_flag = True

    def run(self):
        t1 = threading.Thread(target=self.resolve_domain)
        t2 = threading.Thread(target=self.generate_website_thumbnail)
        t3 = threading.Thread(target=self.get_key)
        t3.start()
        t1.start()
        t2.start()

#        t1.join()
#        t2.join()
#        t3.join()
        print "Ending ", self.domain_ip, self.website_thumbnail

a=DomainOperations("www.google.com")
a.run();
#a.get_key()