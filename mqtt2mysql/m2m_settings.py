#(@)settings.py
# Note: this must be valid Python!

logfile  = 'mqtt2sql.log'

# Broker

mqtt_broker = 'localhost'       # default: 'localhost'
mqtt_port = 1883                # default: 1883
mqtt_clientid = 'mqtt2sql'      # MUST be set
mqtt_username = 'fongshek'
mqtt_password = 'Fm12345'

# List of topics we should subscribe to
topics = [
        'fongshek/test',
    ]


# Storage

dbengine =  'mysql'
dbhost = 'localhost'
dbname = 'mqtt_log'          # default: "mqtt_log"
dbuser = 'root'
dbpasswd = 'password'
dbport = 3306                 # default: 3306

# Plugins

