# ipv6-probe

ipv6活跃探测

张怡桢 大三 南开大学软件工程在读

# ipv6-probe-baseline
Run Method

AddrMiner

su：nohup /home/chengdaguo/anaconda3/envs/AddrMiner/bin/python /home/chengdaguo/ipv6/Baseline/AddrMiner/DynamicScan.py &
No: nohup /home/chengdaguo/anaconda3/envs/AddrMiner/bin/python /home/chengdaguo/ipv6/Baseline/AddrMiner/AddrMiner-N.py &

6Hit
nohup /home/chengdaguo/anaconda3/envs/6Hit/bin/python /home/chengdaguo/ipv6/Baseline/6Hit/main.py &
 Main.py 
M = 种子数量
input——seeds = 种子文件
beta = 预算
B = 每轮迭代多少
￼

6Tree
直接给预算和输入文件夹
nohup python Baseline/6Tree/DynamicScan.py &
Baseline/6Tree/DynamicScan.py
￼

6Forest
 Main.py
nohup /home/chengdaguo/anaconda3/envs/6Forest/bin/python /home/chengdaguo/ipv6/Baseline/6Forest/main.py &

No: nohup /home/chengdaguo/anaconda3/envs/Alias/bin/python /home/chengdaguo/ipv6/Baseline/6Forest/main_no.py &
nohup /home/chengdaguo/anaconda3/envs/6GAN/bin/python /home/chengdaguo/ipv6/Baseline/6Forest/main_no.py &

6Graph 
Main.py
nohup /home/chengdaguo/anaconda3/envs/6Graph/bin/python /home/chengdaguo/ipv6/Baseline/6Graph/main_v3.py &

DET
main_v2.py
nohup /home/chengdaguo/anaconda3/envs/DET/bin/python /home/chengdaguo/ipv6/Baseline/DET/main.py &

Entropy-ip
1. nohup ./2.ALL.sh data/dataset1.txt dataset1 &
2. nohup /home/chengdaguo/anaconda3/envs/entropy-ip/bin/python /home/chengdaguo/ipv6/Baseline/Entropy-ip/c.py &
￼

6GAN
nohup /home/chengdaguo/anaconda3/envs/6GAN/bin/python /home/chengdaguo/ipv6/Baseline/6GAN/train.py &
nohup /home/chengdaguo/anaconda3/envs/6GAN/bin/python /home/chengdaguo/ipv6/Baseline/6GAN/run.py &
nohup /home/chengdaguo/anaconda3/envs/6GAN/bin/python /home/chengdaguo/ipv6/Baseline/6GAN/hit.py &


6GEN

bash ./all-old.sh dataset1/test.txt dataset1/result dataset1/no_prefix.txt dataset1/alias_prefix.txt 2402:f000:6:1401:46a8:42ff:fe43:6d00 1

nohup /home/chengdaguo/anaconda3/envs/6Gen/bin/python /home/chengdaguo/ipv6/Baseline/6Gen/My6Gen/patternMining.py &




export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
