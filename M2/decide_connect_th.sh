<<comment
command line argv
1 : timeonly
2 : time and iv
3 : background noise
4 : background noise and time
comment

rm /home/nozaki/github/python/M2/txt_for_decide_th/*

for i in `seq 80 10 300`
do
	echo $i
    python prob_method2.py $1 $i
    rm -r /home/nozaki/speaker_clustering/news_i-vector/data/sph
    mkdir /home/nozaki/speaker_clustering/news_i-vector/data/sph
    cd /home/nozaki/newsdata
    #sh connect.sh
    mv connect.sh /home/nozaki/github/python/M2/txt_for_decide_th/connect_$i.txt
    cp rename.sh /home/nozaki/github/python/M2/txt_for_decide_th/rename_$i.txt
    cd /home/nozaki/github/python/M2/
done


