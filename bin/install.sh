dest_folder="/home/iot/bin"
echo "Install bin  to " $dest_folder
mkdir -p $dest_folder
chmod -Rf +x *.py
chmod -Rf +x *.sh
cp . $dest_folder -rf

rm /usr/local/bin/mycron.py
ln -s $dest_folder/mycron.py /usr/local/bin/mycron.py
cp crontab /etc/.
