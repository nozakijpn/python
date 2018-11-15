<<comment
command line argv
1 : timeonly
2 : time and iv
3 : background noise
4 : background noise and time
comment

python prob_method.py $1
rm -r /home/nozaki/speaker_clustering/news_i-vector/data/sph 
mkdir /home/nozaki/speaker_clustering/news_i-vector/data/sph
cd /home/nozaki/newsdata
#sh connect.sh
mv connect.sh /home/nozaki/github/python/M2/tooltxt/connect.txt
python /home/nozaki/github/python/M2/mk_connect_wav.py
cp rename.sh /home/nozaki/github/python/M2/tooltxt/rename.txt

cd /home/nozaki/speaker_clustering/news_i-vector
sh delete_nozaki.sh
sh make_i-vector_nozaki.sh

cd iv/raw
mv /home/nozaki/newsdata/rename.sh ./
sh rename.sh
rm soxed* rename.sh
#mv rename.sh /home/nozaki/github/python/M2/rename.txt