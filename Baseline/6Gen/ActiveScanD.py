#!/usr/bin/python3.6
# encoding:utf-8
import subprocess, os,json, time,re

def getIPv6Address():
    output = os.popen("ifconfig").read()
    # print(output)
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]

def Scan(addr_set, source_ip, output_file, tid=0):
    """
    运用扫描工具检测addr_set地址集中的活跃地址

    Args：
        addr_set：待扫描的地址集合
        source_ip
        output_file
        tid:扫描的线程id

    Return：
        active_addrs：活跃地址集合
    """
    
    scan_input = output_file + '/zmap/scan_input_{}.txt'.format(tid)
    scan_output = output_file + '/zmap/scan_output_{}.txt'.format(tid)
    os.makedirs(os.path.dirname(scan_input), exist_ok=True)
    os.makedirs(os.path.dirname(scan_output), exist_ok=True)
    
    with open(scan_input, 'w', encoding = 'utf-8') as f:
        for addr in addr_set:
            f.write(addr + '\n')

    active_addrs = set()
    command = 'sudo zmap --ipv6-source-ip={} --ipv6-target-file={} -M icmp6_echoscan -p 80 -q -o {}'\
    .format(source_ip, scan_input, scan_output)
    print('[+]Scanning {} addresses...'.format(len(addr_set)))
    t_start = time.time()
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # ret = p.poll()
    while p.poll() == None:
        pass

    if p.poll() == 0:
        # with open(output_file, 'a', encoding='utf-8') as f:
        # time.sleep(1)
        for line in open(scan_output):
            if line != '':
                active_addrs.add(line[0:len(line) - 1])
                    # f.write(line)
            
    print('[+]Over! Scanning duration:{} s'.format(time.time() - t_start))
    print('[+]{} active addresses detected!'
        .format(len(active_addrs)))
    # return active_addrs
    if len(addr_set) > 0:
        hit_rate = len(active_addrs)/len(addr_set)
    else:
        hit_rate = 0
    return len(addr_set),len(active_addrs),hit_rate

def scan_addr(output_file,datafile,tid=0):
    source_ip = getIPv6Address()
    output_file = output_file
    addr_set = set()
    with  open(datafile,  "r")  as  fileHandler:
    # Read next line
        line  =  fileHandler.readline()
    # check line is not empty
        while  line:
            addr_set.add(line.strip())
            line  =  fileHandler.readline()
    return Scan(addr_set,source_ip,output_file,tid)


def scan_addr_list(output_file,addr_set,tid=0):
    source_ip = getIPv6Address()
    output_file = output_file
    return Scan(addr_set,source_ip,output_file,tid)

if __name__ == '__main__':
    addr_set = set()
    addr_set.add('2400:da00:2::29')
    addr_set.add('2404:0:8f82:a::201e')
    addr_set.add('2404:0:8e04:9::201e')
    Scan(addr_set)
    print('Over!')
