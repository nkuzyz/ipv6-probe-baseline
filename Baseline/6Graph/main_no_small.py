import random
import ipaddress
import sys,os,re
from ActiveScan import scan_addr




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
    
    result = []
    result.append([0,scan_addr(sub_output,file)])
    
    filename = sub_output+"/analydata.txt"
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    w = open(filename,"w")
    for r in result:
        w.write("su_{}.txt : target {} , active {} , hit_rate {} \n".format(r[0],r[1][0],r[1][1],r[1][2]))



if __name__ == '__main__':
    # 参数
    prefix_num = 464
    # prefix_num = 449
    dataset_name = 'dataset1'
    algorithm = '6Graph'
    prefix_file = 'Baseline/Database/dataset1_all_no_seeds_prefix.txt'
    # prefix_file = 'Baseline/Database/test_pre.txt'
    
    # begin
    su_data_file = 'Baseline/'+algorithm+'/'+dataset_name+'/'
    output_file = 'Baseline/'+algorithm+'/'+dataset_name+'_no/'
    # with open(prefix_file, 'r') as f:
    #     lines = f.readlines()
    # # f =  open(prefix_file, 'r').readlines()
    # prefix_read = [i.split(',')[1] for i in lines]
    
    # # print(len(prefix_read))
    # # print(prefix_read[0])

    # prefix_data = [tran_prefix(i) for i in prefix_read]
    # no_prefix_num = len(prefix_data)

    
    budgets = [1000]
    for budget in budgets:
        # sample_file = su_data_file+str(prefix_num*budget)+'/generate_samples.txt'
        
        # su_samples = open(sample_file, 'r').readlines()
        # su_samples = [i.strip() for i in su_samples]
        # sample = random.sample(su_samples,budget)

        output_dir = output_file+'{}/generate_samples.txt'.format(budget)
        # os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        # f = open(output_dir,'w')

        # for prefix in prefix_data:
        #     for i in range(len(sample)):
        #         f.write(combine_address(prefix,sample[i])+'\n')
        # f.close()
        print(output_dir)
        scan(output_file+'{}'.format(budget),output_dir)