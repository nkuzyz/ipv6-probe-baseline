# Entropy/IP

This code implements the Entropy/IP algorithm, as published in:

> P. Foremski, D. Plonka, A. Berger, *Entropy/IP: Uncovering Structure in IPv6 Addresses*, Proceedings of the 2016 Internet Measurement Conference. ACM, 2016.

You can read the paper as PDF at [Akamai website](https://www.akamai.com/us/en/multimedia/documents/technical-publication/entropy-ip-uncovering-structure-in-ipv6-addresses.pdf). This repository supports an Akamai Custom Analytics project.

# License

Entropy/IP is patent pending, submitted as application number 15618303 by Akamai Technologies, Inc.

Akamai releases this code repository as open source, but for *non-commercial, academic research purposes* only. Please read [the LICENSE file](./LICENSE) carefully.

# Quick Start

  1. Install Python 2 packages using `pip`, `apt`, etc.:
  * bnfinder
  * toposort (`apt install python-toposort`)
  * numpy (`apt install python-numpy`)
  * matplotlib (`apt install python-matplotlib`)
  * scikit-learn (`apt install python-scikits-learn`)
  2. Prepare your IPv6 dataset in hex IP format (32 hex characters per line, no colons).
  3. Change working directory to this repository.
  4. Run `./ALL.sh <ips> <target>`, where `<ips>` is your dataset file, and `<target>` is the output directory for storing the results.

# Notes

In this repository, you can find the following files. Read the source code for more details.

* `a{1,2,3,4,5}-*`: scripts for building an Entropy/IP model for a set of IPv6 addresses
* `b1-webreport.sh`: script for building a web report of an Entropy/IP model
* `c{1,2}-*`: scripts for generating target IPv6 addresses for scanning
* `ALL.sh`: shortcut script that does `a*` and `b*` in one shot
* `bin/`: supportive tools for `a*`, `b*`, and `c*` scripts
* `css/`, `js/`: code needed for the web report; some files come from external projects and have different licensing (see headers)

Note that parts of the code might use different names than the paper for referring to various aspects of Entropy/IP. This is because the taxonomy evolved while developing the system.

Also, the code does not directly handle datasets larger than 100K IPs. Whenever appropriate, it will randomly sample from the input dataset if its too large. It is not a significant limitation, as usually we just approximate probabilities from their empirical frequencies in the dataset. From our experiences, 100K is way more than enough to approximate the probabilities properly. On the other hand, we identified that Aggregate Count Ratios are sensitive to sampling, thus for accurate ACR plots for large datasets, one should rather use better tools.

# Author

Pawel Foremski, 2016, pjf@foremski.pl, [@pforemski](https://twitter.com/pforemski).



数据没有冒号，32位16进制的数，且数据数目是16的倍数
1. format
2. ./2.ALL.sh data/su_seed_463.txt result_su
3. 生成并解码
   1. c1-gen ——文件名要改
   2. c2-decode ——文件名要改
  chmod 777 3.generate_ipv6.sh
  ./3.generate_ipv6.sh
4. 别名前缀


./2.ALL.sh data/dataset1.txt dataset1

sudo nohup ./3.generate_ipv6_few.sh &


nohup /home/chengdaguo/anaconda3/envs/Alias/bin/python /home/chengdaguo/ipv6/Baseline/Entropy-ip/4.Alias_Prefix.py &