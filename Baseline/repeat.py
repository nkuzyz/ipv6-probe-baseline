

file ='6gan'
dataset = open('dataset3.txt', 'r').readlines()

base = open('{}/zmap/scan_output_0.txt'.format(file), 'r').readlines()


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

dataset = [i.strip() for i in dataset]
dataset_set = set(dataset)
base = [tran_ipv6(i.strip()) for i in base]
base_set = set(base)

# print(tran_ipv6('240e:659:1b0:626:9ced:d96d:38f7:a60f'))
print(len(base_set))
# for i in base_set:
#     print(i)

base_set = base_set - dataset_set
print(len(base_set))

result = open('{}/seeds_no_repeat.txt'.format(file), 'w')
result.write('\n'.join(base_set))