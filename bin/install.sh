dest_folder="/home/iot/bin"
echo "Install bin  to " $dest_folder
mkdir -p $dest_folder
cp . $dest_folder -r
chmod -Rf +x mycron.py

rm /usr/local/bin/mycron.py
ln -s $dest_folder/mycron.py /usr/local/bin/mycron.py
cp crontab /etc/.