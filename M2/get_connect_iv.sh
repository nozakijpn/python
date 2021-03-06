<<comment
command line argv
1 : timeonly
2 : time and iv
3 : background noise
4 : background noise and time
comment

<<comment
$1 : prob_method number
$2 : th_time
$3 : th_iv
引数入れなくてもprob_method.pyでエラーが出ないようになっているので、引数入れるのが面倒だったら、プログラム内のパラメータの数値を変更推奨
comment

#ROOT_PATH=$(cd $(dirname $0); pwd)

python prob_method.py $1 $2 $3
echo "python prob_method.py $1 $2 $3"
rm -r /home/nozaki/speaker_clustering/news_i-vector/data/sph 
mkdir /home/nozaki/speaker_clustering/news_i-vector/data/sph
cd /home/nozaki/newsdata

cp connect.sh /home/nozaki/tooltxt/connect.txt
cp rename.sh /home/nozaki/tooltxt/rename.txt

#cd $ROOT_PATH
#python acc_sox.py

sh connect.sh

cd /home/nozaki/speaker_clustering/news_i-vector
sh delete_nozaki.sh
sh make_i-vector_nozaki.sh

cd iv/raw
mv /home/nozaki/newsdata/rename.sh ./
sh rename.sh
rm soxed* rename.sh
#mv rename.sh /home/nozaki/github/python/M2/rename.txt