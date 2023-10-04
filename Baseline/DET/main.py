from AliasScanD import *
from DynamicScan import Start
import sys,os,re,time
# file_path = 'DET/det_output.txt'
# os.makedirs(os.path.dirname(file_path), mode=777,exist_ok=True)

print("我开始啦")

# sys.stdout = open(file_path, "w")

# f = open("few_test_prefix_list.txt","r")

# prefixs = eval(f.readline())

# prefix_num = 464
# prefix_num = 449

# num = [100,1000,5000,10000]
# num = [100]
# budget = [prefix_num*i for i in num]

budget = [5000]
# times = time.asctime().replace(' ','_')
input = "Baseline/Database/dataset3.txt"
output = "Baseline/DET/dataset3/"

for b in budget:

    # for p in prefixs:
    # # p=prefixs[0]
    #     input = "data/few_"+str(p)+".txt"
    #     output = "DET/output_"+str(budget)+"/few_"+str(p)
    #     result.append([p,Start(input,output,budget)]) 
    # output = "Baseline/DET/output_su/output_"+str(b)+"/total_"+str(times)
    sub_output = output+str(b)
    os.makedirs(os.path.dirname(sub_output),exist_ok=True)
    target_len, result_len, hit_rate = Start(input,sub_output,b)
    
    filename = sub_output+"/analydata.txt"
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    w = open(filename,"w")
    w.write("target {} , active {} , hit_rate {} \n".format(target_len, result_len, hit_rate))
    w.close()
    # file = sub_output+'/zmap/scan_input_0.txt'
    # scan(sub_output,file)


    # test_data = open(sub_output+'/zmap/scan_output_0.txt').readlines()
    # sub_output_alias = sub_output+'/alias'

    # # # alias and save
    # alias = get_alias_prefix_fun(test_data,sub_output_alias)
    # # alias = open(sub_output_alias+'/alias_prefix.txt').readlines()
    
    # # samples应该是原样本
    # origin_samples = open(file).readlines()
    # origin_samples = [get_entire_ipv6(x.strip()) for x in origin_samples]

    # print(len(origin_samples))
    # no_alias_samples = delete_alias_ip(alias,origin_samples,sub_output_alias)
    # print(len(no_alias_samples))

    # filename = sub_output_alias+'/samples_alias_length.txt'
    # os.makedirs(os.path.dirname(filename),exist_ok=True)
    # f = open(filename,"w")
    # f.write("origin_samples: "+str(len(origin_samples)))
    # f.write("no_alias_samples: "+str(len(no_alias_samples)))
    # f.write("samples_no_alias: "+str(len(origin_samples)-len(no_alias_samples)))
    # f.close()