import sys, getopt,os
from config import cConfig

def parse_config():
    print "parse config"

def parse_argv(argv):
    myConfigFile = 'cron.conf'
    myMessage = ""
    myScript = os.path.basename(__file__)
    myConfig = None
    try:
      opts, args = getopt.getopt(argv,"hc:m:") 
    except getopt.GetoptError:
      print myScript , ' -c <configfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print myScript , ' -c <configfile> '
         sys.exit()
      elif opt in ("-c", "--cfile"):
         # config_file
         myConfigFile = arg
      elif opt in ("-m"):
         # message
         myMessage = arg

    myConfig = cConfig(myConfigFile)
    myConfig.message = myMessage
    myConfig.filename = myConfigFile
    return (myConfig)    
    
def main():
    myConfig = parse_argv(sys.argv[1:])
#    print myConfigFile
    print myConfig.filename , myConfig.message

if __name__ == "__main__":
    main();