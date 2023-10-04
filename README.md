# ipv6-probe

ipv6活跃探测

张怡桢 2013747 nku20级本科生

# ipv6-probe-baseline
Run Method

输入的样本：
dataset3：
2001:1291:0000:0106:0000:0000:c930:4751
2001:1291:0000:0106:0000:0000:c930:4753
2001:1291:0000:0106:0000:0000:c930:4758
2001:1291:0000:0106:0000:0000:c930:474f
2001:1291:0000:0106:0000:0000:c930:475f
2001:1291:0000:0106:0000:0000:0000:000a
2001:1291:0000:0106:0000:0000:c930:475d
dataset3_no_colons：
200112910000010600000000c9304751
200112910000010600000000c9304753
200112910000010600000000c9304758
200112910000010600000000c930474f
200112910000010600000000c930475f
2001129100000106000000000000000a
200112910000010600000000c930475d

## 6Forest
输入dataset3

### su
Baseline/6Forest/main.py
### no
Baseline/6Forest/main_no.py

## 6GAN
有很多特殊的预设文件需要载入在dataset3文件夹中
输入的数据集要改名字放到这dataset3/source_data/responsive-addresses.txt
### su
训练得到模型：Baseline/6GAN/train.py
载入模型得到样本：Baseline/6GAN/run.py
### no
100-1000的预算
Baseline/6GAN/main_no_small.py
5000-10000的预算
Baseline/6GAN/main_no_big.py

## 6Gen
输入dataset1_no_colons
输入dataset1
### su 
Baseline/6Gen/patternMining.py
### no
Baseline/6Gen/main_no_small.py
Baseline/6Gen/main_no_big.py

## 6Graph
输入dataset3

### su
Baseline/6Graph/main_v3.py
### no
Baseline/6Graph/main_no_small.py
Baseline/6Graph/main_no_big.py

## 6Hit
输入：dataset3
### su 
Baseline/6Hit/main.py
### no
Baseline/6Hit/main_no_small.py
Baseline/6Hit/main_no_big.py

## 6Tree
输入：dataset3
### su
Baseline/6Tree/DynamicScan.py
### no
Baseline/6Tree/main_no_small.py
Baseline/6Tree/main_no_big.py

## AddrMiner


### su
输入dataset3
Baseline/AddrMiner/DynamicScan_S.py
### no
当然，如果你没有自己提前分好类别只是一堆数据放进去的话，partition.py会给你按照su，few，no三种分类，但是我们自己已经分完了，所以直接开始训练模式
第一步：
根据输入的样本生成pattern library
输入：multi_level = dataloader("./data/dataset2.csv", "./data/ipasn.20230522.dat")
其中：./data/dataset2.csv就是样本变成csv格式
     ./data/ipasn.20230522.dat根据你自己用的
Baseline/AddrMiner-main/generatePD.py
输出：得到模式
第二步：
根据生成的样本模式根据asn号属性进行模式迁移得到no
Baseline/AddrMiner-main/AddrMiner-N_v2.py

## DET
输入dataset3
### su
Baseline/DET/main.py
### no
Baseline/DET/main_no_small.py
Baseline/DET/main_no_big.py


## Ebtropy-ip
### su

1. format_ipv6.py其实就是把地址补全然后去掉冒号也就是得到dataset3_no_colons作为第二部的输入
2. All.sh segment mining
3. Baseline/Entropy-ip/3.c.py 得到结果

### no
Baseline/Entropy-ip/main_no_small.py
Baseline/Entropy-ip/main_no_big.py


