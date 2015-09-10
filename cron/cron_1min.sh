# echo $(date +"%y%m%d-%H%M%S")  "> execute > cron_1min.sh" | wall -n

# save mosquitto system info to mysql
python /home/mosquitto/bin/mqtt2mysql.py -c /home/mosquitto/bin/m2m_syslog.conf 
