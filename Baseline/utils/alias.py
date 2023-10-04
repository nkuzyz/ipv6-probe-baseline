from __future__ import print_function
import pandas as pd
import secrets
import subprocess,json, time,re
import sys,os
import SubnetTree


def getIPv6Address():
    output = os.popen("ifconfig").read()
    # print(output)
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]

def get_rawIP(IP):
    # 标准IP -> hex IP
    seglist=IP.split(':')
    if seglist[0]=='':
        seglist.pop(0)
    if seglist[-1]=='':
        seglist.pop()
    sup=8-len(seglist)
    if '' in seglist:
        sup+=1
    ret=[]
    for i in seglist:
        if i=='':
            for j in range(0,sup):
                ret.append('0'*4)
        else:
            ret.append('{:0>4}'.format(i))
    rawIP=''.join(ret)
    assert(len(rawIP)==32)
    return rawIP


def read_aliased(tree, fh):
    return fill_tree(tree, fh, ",1")

def fill_tree(tree, fh, suffix):
    for line in fh:
        line = line.strip()
        try:
            tree[line] = line + suffix
        except ValueError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)
    return tree


def format_ipv6(ipv6):
    # add : to ipv6
    ipv6_list = []
    for i in range(0,len(ipv6),4):
        ipv6_list.append(ipv6[i:i+4])
    ipv6 = ":".join(ipv6_list)
    return ipv6

def format_ipv6_prefix(ipv6):
    prefix = format_ipv6(ipv6)
    prefix = prefix+'::/'+str(len(prefix)*4)
    return prefix


def get_prefix(x,prefix_len=16):
    x = x.replace(':','')
    return x[:prefix_len]




def generate_ipv6_from_prefix(prefix_list):
    generate_samples = []
    for prefix in prefix_list:
        ipv6s = [prefix]*16
        left_length = 32-len(prefix)-1
        for i in range(16):
            ipv6s[i] = ipv6s[i] + hex(i)[2:] + secrets.token_hex(left_length//2 + 1)[:left_length]
            ipv6s[i] = format_ipv6(ipv6s[i])
        generate_samples+=ipv6s
    return generate_samples



def data_to_prefix(ip_samples):
    
    df = pd.DataFrame(ip_samples,columns=['addr'])
    
    prefix_list = []
    for i in range(16,31):
        df_copy = df.copy()
        df_copy['prefix'] = df_copy['addr'].apply(get_prefix,args=(i,))
        df_group_set = df_copy.groupby('prefix').agg({'addr':lambda x:','.join(x)})
        df_group_set['addr_num'] = df_group_set['addr'].apply(lambda x:len(x.split(',')))
        # print(df_group_set)
        # select addr_num > 2 as a new df
        df_group_set = df_group_set[df_group_set['addr_num']>=100]
        # print(df_group_set)
        prefix_list += df_group_set.index.tolist()
    return prefix_list



def Scan_icmp6(addr_set, source_ip, output_file, tid=0):
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

    scan_input = output_file + '/zmap_icmp/scan_input_{}.txt'.format(tid)
    scan_output = output_file + '/zmap_icmp/scan_output_{}.txt'.format(tid)
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
    # if len(addr_set) > 0:
    #     hit_rate = len(active_addrs)/len(addr_set)
    # else:
    #     hit_rate = 0
    # print('[+]hit rate = {}'.format(hit_rate))
    # return len(addr_set),len(active_addrs),hit_rate
    return active_addrs


def Scan_tcp(addr_set, source_ip, output_file, tid=0):
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

    scan_input = output_file + '/zmap_tcp/scan_input_{}.txt'.format(tid)
    scan_output = output_file + '/zmap_tcp/scan_output_{}.txt'.format(tid)
    os.makedirs(os.path.dirname(scan_input), exist_ok=True)
    os.makedirs(os.path.dirname(scan_output), exist_ok=True)

    with open(scan_input, 'w', encoding = 'utf-8') as f:
        for addr in addr_set:
            f.write(addr + '\n')

    active_addrs = set()

    command = 'sudo zmap --ipv6-source-ip={} --ipv6-target-file={} -M ipv6_tcp_synscan -p 80 -q -o {}'\
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
    # if len(addr_set) > 0:
    #     hit_rate = len(active_addrs)/len(addr_set)
    # else:
    #     hit_rate = 0
    # print('[+]hit rate = {}'.format(hit_rate))
    # return len(addr_set),len(active_addrs),hit_rate
    return active_addrs


def scan_addr(output_file,addr_set):
    source_ip = getIPv6Address()
    output_file = output_file
    # ICMPv6 and TCP/80
    x = list(Scan_icmp6(addr_set,source_ip,output_file))
    y = list(Scan_tcp(addr_set,source_ip,output_file))
    a = x+y

    return a


def get_alias_prefix(active_addr):
    df = pd.DataFrame(list(active_addr),columns=['addr'])
    
    prefix_list = []
    for i in range(16,31):
        df_copy = df.copy()
        df_copy['prefix'] = df_copy['addr'].apply(get_prefix,args=(i,))
        df_group_set = df_copy.groupby('prefix').agg({'addr':lambda x:','.join(x)})
        df_group_set['addr_num'] = df_group_set['addr'].apply(lambda x:len(x.split(',')))
        # print(df_group_set)
        # select addr_num > 2 as a new df
        df_group_set = df_group_set[df_group_set['addr_num']>=32]
        # print(df_group_set)
        prefix_list += df_group_set.index.tolist()
    prefix_list = [format_ipv6_prefix(x) for x in prefix_list]
    return prefix_list


def get_alias_prefix_fun(ip_samples,path):
    # 从样本中获取所有的 prefix
    prefix_list = data_to_prefix(ip_samples)
    # 每一个 prefix 生成 16 个 ipv6 地址
    samples = generate_ipv6_from_prefix(prefix_list)
    # 扫描样本中的 ipv6 地址得到活跃的 ipv6 地址
    activa_addr = scan_addr(path,samples)
    # 根据活跃的 ipv6 地址得到 alias prefix
    alias = get_alias_prefix(activa_addr)
    
    prefix_path = path+'/alias_prefix.txt'
    os.makedirs(os.path.dirname(prefix_path), exist_ok=True)
    open(prefix_path,'w').write('\n'.join(alias))
    return alias
    



def delete_alias_ip(alias,ip_samples,path):
    aliased_file = alias
    ip_address_file = ip_samples

    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()

    # Read aliased and non-aliased prefixes
    tree = read_aliased(tree, aliased_file)
    # tree = read_non_aliased(tree, non_aliased_file)
    output = path+'/non_aliased_ipv6_samples.txt'
    os.makedirs(os.path.dirname(output), exist_ok=True)
    f = open(output, "w")
    # Read IP address file, match each address to longest prefix and print output
    no_alias_samples = []
    for line in ip_address_file:
        line = line.strip()
        try:
            print(line + "," + tree[line])
        except KeyError as e:
            f.write(line+"\n")
            no_alias_samples.append(line)
    return no_alias_samples

def alias_fun(samples,path):
    alias = get_alias_prefix_fun(samples,path)
    no_alias_samples = delete_alias_ip(alias,samples,path)
    return no_alias_samples
