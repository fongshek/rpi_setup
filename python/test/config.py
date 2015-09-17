
import os

CONFIG=os.getenv('M2SCONFIG', 'm2m_settings.py')

class cConfig(object):
    def __init__(self, filename=CONFIG):
        self.config = {}
        execfile(filename, self.config)
        
    def get(self, key, default=None):
        return self.config.get(key, default)

if __name__ == '__main__':
    cf = Config()
    print cf.get('mqtt_broker', 'xx')
