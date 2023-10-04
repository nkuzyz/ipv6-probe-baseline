import random
import ipaddress
import sys,os
from ActiveScanD import scan_addr

def tran_prefix(strs):
    strs_list = strs.split('::/')
    if len(strs_list) == 1:
        strs_list = strs.split('/')
    prefix = strs_list[0]
    # print(prefix)
    prefix_num = int(strs_list[1])/4
    prefix_list = prefix.split(':')
    for i in range(len(prefix_list)):
        if len(prefix_list[i]) != 4:
            prefix_list[i] = prefix_list[i] + '0'*(4-len(prefix_list[i]))
    if len(prefix_list) < prefix_num/4:
        for i in range(8-len(prefix_list)):
            prefix_list.append('0000')
    temp = ":".join(prefix_list)
    # temp = temp[:int(prefix_num)]

    return temp

# print(tran_prefix('2001:da8:ff:212::/64'))

def combine_address(prefix,sample):
    if sample.startswith(prefix):
        return sample
    else:
        new_string = prefix + sample[len(prefix):]
        return new_string
    
def scan(sub_output,file):
    # scan and analysis
    
    results = []
    results.append([0,scan_addr(sub_output,file),0])
    
    filename = sub_output+"/analydata.txt"
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    w = open(filename,"w")
    for r in results:
        w.write("su_{}.txt : target {} , active {} , hit_rate {} \n".format(r[0],r[1][0],r[1][1],r[1][2]))

def tran_ipv6(sim_ip):
    if  sim_ip == "::":
        return "0000:0000:0000:0000:0000:0000:0000:0000"
    ip_list=["0000","0000","0000","0000","0000","0000","0000","0000"]
    if sim_ip.startswith("::"):
        tmplist = sim_ip.split(":")
        for i in range(0, len(tmplist)):
            ip_list[i+8-len(tmplist)] = ("0000"+tmplist[i])[-4:]
    elif sim_ip.endswith("::"):
        tmplist = sim_ip.split(":")
        for i in range(0, len(tmplist)):
            ip_list[i] = ("0000"+tmplist[i])[-4:]
    elif "::" not in sim_ip:
        tmplist = sim_ip.split(":")
        for i in range(0,len(tmplist)):
            ip_list[i] = ("0000" + tmplist[i])[-4:]
    # elif sim_ip.index("::") > 0:
    else:
        tmplist = sim_ip.split("::")
        tmplist0 = tmplist[0].split(":")
        #print(tmplist0)
        for i in range(0, len(tmplist0)):
            ip_list[i] = ("0000" + tmplist0[i])[-4:]
        tmplist1 = tmplist[1].split(":")
        #print(tmplist1)
        for i in range(0, len(tmplist1)):
            ip_list[i + 8 - len(tmplist1)] = ("0000" + tmplist1[i])[-4:]
    # else:
    #     tmplist = sim_ip.split(":")
    #     for i in range(0,tmplist):
    #         ip_list[i] = ("0000" + tmplist[i])[-4:]
    #print(ip_list)
    return ":".join(ip_list)


if __name__ == '__main__':
    # 参数
    # prefix_num = 464
    prefix_num = 449
    dataset_name = 'dataset2'
    algorithm = '6Tree'
    
    prefix_file = 'Baseline/Database/{}_all_no_seeds_prefix.txt'.format(dataset_name)
    # prefix_file = 'Baseline/Database/test_pre.txt'
    
    # begin
    su_data_file = 'Baseline/'+algorithm+'/'+dataset_name+'/'
    output_file = 'Baseline/'+algorithm+'/'+dataset_name+'_no/'
    with open(prefix_file, 'r') as f:
        lines = f.readlines()
    # f =  open(prefix_file, 'r').readlines()
    prefix_read = [i.split(',')[1] for i in lines]
    
    # print(len(prefix_read))
    # print(prefix_read[0])

    prefix_data = [tran_prefix(i) for i in prefix_read]
    no_prefix_num = len(prefix_data)

    
    budgets = [100,1000]
    for budget in budgets:
        sample_file = su_data_file+str(prefix_num*budget)+'/zmap/scan_input_0.txt'
        
        su_samples = open(sample_file, 'r').readlines()
        su_samples = [i.strip() for i in su_samples]
        sample = random.sample(su_samples,budget)
        # sample这里需要处理一下格式！！！！
        sample = [tran_ipv6(i) for i in sample]
        # print(sample[0])
        output_dir = output_file+'{}/generate_samples.txt'.format(budget)
        os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        f = open(output_dir,'w')

        for prefix in prefix_data:
            for i in range(len(sample)):
                f.write(combine_address(prefix,sample[i])+'\n')
        f.close()
        print(output_dir)
        scan(output_file+'{}'.format(budget),output_dir)