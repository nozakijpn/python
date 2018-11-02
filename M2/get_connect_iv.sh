python prob_method.py 2
rm -r /home/nozaki/speaker_clustering/news_i-vector/data/sph 
mkdir /home/nozaki/speaker_clustering/news_i-vector/data/sph
cd /home/nozaki/newsdata
sh connect.sh
rm connect.sh

cd /home/nozaki/speaker_clustering/news_i-vector
sh delete_nozaki.sh
sh make_i-vector_nozaki.sh

cd iv/raw
mv /home/nozaki/newsdata/rename.sh ./
sh rename.sh
rm soxed* rename.sh
cd /home/nozaki/speaker_clustering/news_i-vector/data/sph
rm soxed*