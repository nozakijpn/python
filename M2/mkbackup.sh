echo "input backup name"
read filename

echo "input backup date"
read nowdate

mkdir /mnt/disk2/backup/$filename/$nowdate
cp /home/nozaki/github/python/M2 /mnt/disk2/backup/$filename/$nowdate/ -r

mkdir /home/nozaki/backup/$filename/$nowdate
cp /home/nozaki/github/python/M2 /home/nozaki/backup/$filename/$nowdate/ -r
