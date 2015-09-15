echo $(date +"%y%m%d-%H%M%S")  "> execute > cron_5min.sh" | wall -n

iot_bin="/home/iot/bin"
# save mosquitto system info to mysql
# python $iot_bin/mqtt2mysql.py -c $iot_bin/m2m_syslog.conf 

# run duckdns update
myscript=$iot_bin/duckdns.sh

sh $myscript
