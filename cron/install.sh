dest_folder="/usr/local/bin/"
echo "copy all .sh to " + $dest_folder
mkdir -p $dest_folder
cp cron*.sh $dest_folder

dest_folder="/etc/"
echo "copy crontab to " + $dest_folder
mkdir -p $dest_folder
cp crontab $dest_folder

dest_folder="/home/iot"
echo "copy duckdns.sh to " + $dest_folder
mkdir -p $dest_folder
cp duckdns.sh $dest_folder
