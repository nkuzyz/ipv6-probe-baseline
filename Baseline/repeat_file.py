
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


# 与原数据的问题！

# 6Forest_变小几个
# 6GAN_变小一点点
# 6GEN——不变
# 试了6Graph_一点点？？
# 6Hit_不变
# 试了6Tree_少一半
# AddrMiner 少一半
# DET 少一半
# Entropy-ip_小一半



file ='DET'
dataset = open('Baseline/Database/dataset2.txt', 'r').readlines()
dataset = [i.strip() for i in dataset]
dataset_set = set(dataset)

budgets = [44900,449000,2245000,4490000]
for budget in budgets:
    base = open('Baseline/{}/dataset2/{}/zmap/scan_output_0.txt'.format(file,budget), 'r').readlines()
    base = [tran_ipv6(i.strip()) for i in base]
    base_set = set(base)
    # print(tran_ipv6('240e:659:1b0:626:9ced:d96d:38f7:a60f'))
    print(len(base_set))    
    base_set = base_set - dataset_set
    print(len(base_set))
    result = open('Baseline/{}/dataset2/{}/seeds_no_repeat.txt'.format(file,budget), 'w')
    result.write('\n'.join(base_set))




# for i in base_set:
#     print(i)



