from Forest import Start,generate_test
import sys,os,re,time
from AliasScanF import *
# file_path = 'DET/det_output.txt'
# os.makedirs(os.path.dirname(file_path), mode=777,exist_ok=True)

print("我开始啦")



# prefix_num = 464
# prefix_num = 449

# num = [100,1000,5000,10000]
# num = [100]
# budget = [prefix_num*i for i in num]

budget = [5000]
times = time.asctime().replace(' ','_')
input = "Baseline/Database/dataset3"
output = "Baseline/6Forest/dataset3/"

# input ='Baseline/Database/few_data_500'
# output = "Baseline/6Forest/output_test/total_01"

# 生成模式
Start(input,output)


for b in budget:
    result = []
    # sub_output = output+'/'+str(b)+"_alias"
    # 子文件夹
    sub_output = output+str(b)
    print(sub_output)
    # 根据模式生成样本
    generate_test(input,sub_output,b,output)
    file = sub_output+'/generate_samples.txt'
    # 扫描样本
    scan(sub_output,file)

    # test_data = open(sub_output+'/zmap/scan_output_0.txt').readlines()
    # sub_output = sub_output+'/alias'

    # # 检测别名前缀
    # alias = get_alias_prefix_fun(test_data,sub_output)

    # origin_samples = open(file).readlines()
    # print(len(origin_samples))
    # # 删除别名样本
    # no_alias_samples = delete_alias_ip(alias,origin_samples,sub_output)
    # print(len(no_alias_samples))

    # filename = sub_output+'/samples_alias_length.txt'
    # os.makedirs(os.path.dirname(filename),exist_ok=True)
    # f = open(filename,"w")

    # alias_samples = len(origin_samples)-len(no_alias_samples)
    # f.write("origin_samples: "+str(len(origin_samples))+ "\n")
    # f.write("no_alias_samples: "+str(len(no_alias_samples))+ "\n")
    # f.write("alias_samples: "+str(alias_samples)+ "\n")
    # f.write("now hit rate: "+str(len(test_data)-alias_samples/len(no_alias_samples))+ "\n")

    # f.close()