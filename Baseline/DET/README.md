# DET
Efficient IPv6 address discovery algorithm DET which combines density, information entropy and space tree.  DET is short for detective, which means that  discovery new active IPv6 addresses  in the IPv6 address space.



## zmapv6 installation (ask in IPv4 network)

###  Building from Source

```
git clone https://github.com/tumi8/zmap.git
cd zmap
```
### Installing ZMap Dependencies

On Debian-based systems (including Ubuntu):
```
sudo apt-get install build-essential cmake libgmp3-dev gengetopt libpcap-dev flex byacc libjson-c-dev pkg-config libunistring-dev
```

On RHEL- and Fedora-based systems (including CentOS):
```
sudo yum install cmake gmp-devel gengetopt libpcap-devel flex byacc json-c-devel libunistring-devel
```

On macOS systems (using Homebrew):
```
brew install pkg-config cmake gmp gengetopt json-c byacc libdnet libunistring
```

### Building and Installing ZMap

```
cmake .
make -j4
sudo make install
```

## Usage
Parameter meaning introduction：
* input:  type=str, input IPv6 addresses
* output: type=str,output directory name
* budget: type=int,the upperbound of scan times
* IPv6:   type=str,local IPv6 address
* delta:  type=int, default =16, the base of address
* beta:   type=int, default=16,the max of node

running example
```
sudo python3 DynamicScan.py --input=DataDir/yourdata --output=StoreDir --budget=500  --IPv6=local Ipv6 address --delta=16 --beta=16
```

```
sudo python3 DynamicScan.py --input=/home/chengdaguo/baseline/DET/testData.txt --output=/home/chengdaguo/baseline/DET/output --budget=500  --IPv6=2001:da8:ff:212::10:3 --delta=16 --beta=16
```


```
sudo python3 DET/DynamicScan.py --input=/home/chengdaguo/baseline/scan_output_responsive.txt --output=/home/chengdaguo/baseline/DET/ --budget=500  --IPv6=2001:da8:ff:212::10:3 --delta=16 --beta=16
```




nohup /home/chengdaguo/anaconda3/envs/DET/bin/python /home/chengdaguo/ipv6/Baseline/DET/main_v2.py &