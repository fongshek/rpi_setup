dest_folder="/home/iot/bin"
echo "copy all .py to " + $dest_folder
echo "copy all .conf to " + $dest_folder
echo "copy all .sql to " + $dest_folder
mkdir -p $dest_folder
cp *.py $dest_folder
cp *.conf $dest_folder
cp *.sql $dest_folder

