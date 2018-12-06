echo "input backup name"
read filename

mkdir /mnt/disk2/backup/$filename
cp /home/nozaki/github/python/M2 /mnt/disk2/backup/$filename/ -r

mkdir /home/nozaki/backup/$filename
cp /home/nozaki/github/python/M2 /home/nozaki/backup/$filename/ -r