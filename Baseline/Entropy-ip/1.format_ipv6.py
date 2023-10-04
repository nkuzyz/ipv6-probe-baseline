import numpy as np
import os


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
    return "".join(ip_list)


def format_ipv6(filename,dealname):

    with open(filename,'r') as f:
        arrs = []
        for line in f.readlines():
            # print('before:'+line.strip())
            line = line.split(',')[0]
            arr = tran_ipv6(line.strip())
            # print('after:'+arr)
            arrs.append(arr)

    with open(dealname, "w") as file:
        # Loop through each row in the array
        for row in arrs:
            # Convert the row to a string and write it to the file
            file.write(''.join(row)+'\n')


filename="Baseline/Database/dataset3.txt"
dealname="Baseline/Entropy-ip/data/dataset3.txt"
format_ipv6(filename,dealname)

# print(tran_ipv6('2001:1248:433f:f036:6295:575:c29b:d001'))