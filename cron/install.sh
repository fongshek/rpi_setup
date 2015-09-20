#chmod +x *.sh -r
chmod -Rf +x ./
dest_folder="/home/iot/bin"
echo "copy current folder to "  $dest_folder
cp -r ./ $dest_folder
rm /usr/local/bin/cron*sh
ln -s $dest_folder/cron_1day.sh /usr/local/bin/cron_1day.sh
ln -s $dest_folder/cron_1hr.sh /usr/local/bin/cron_1hr.sh
ln -s $dest_folder/cron_1min.sh /usr/local/bin/cron_1min.sh
ln -s $dest_folder/cron_5min.sh /usr/local/bin/cron_5min.sh
ln -s $dest_folder/cron_reboot.sh /usr/local/bin/cron_reboot.sh


