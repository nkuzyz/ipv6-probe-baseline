from __future__ import print_function
import sys,os,resource
import SubnetTree



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

def delete_alias_ip(alias,ip_samples,path):
    aliased_file = alias
    ip_address_file = ip_samples

    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()

    # Read aliased and non-aliased prefixes
    tree = read_aliased(tree, aliased_file)

    output1 = path+'/address_alias.txt'
    os.makedirs(os.path.dirname(output1), exist_ok=True)
    f1 = open(output1, "w")

    output2 = path+'/address_no_alias.txt'
    os.makedirs(os.path.dirname(output2), exist_ok=True)
    f2 = open(output2, "w")

    # # Read IP address file, match each address to longest prefix and print output
    # no_alias_samples = []
    for line in ip_address_file:
        line = line.strip()
        try:
            f1.write(line + "," + tree[line]+"\n")
        except KeyError as e:
            f2.write(line + "\n")
    #         no_alias_samples.append(line)
    # return no_alias_samples



if __name__ == '__main__':
    # limit_memory(4*2**30)
    dataset = 'Baseline/6Forest/dataset2/'
    num = 2245000
    sub_output = dataset+'{}'.format(num)

    alias = open('Baseline/Database/data2_alias_prefix.txt').readlines()
    origin_samples = open(sub_output+'/zmap/scan_output_0.txt').readlines()

    delete_alias_ip(alias,origin_samples,sub_output)
    
    # # 要减去的数值
    # alias_samples = open(sub_output+'/alias_address.txt').readlines()
    # print(len(alias_samples))


    #去除别名
    # sub_output = "./dataset/"   # 输出文件保存路径
    # alias = open("/home/chengdaguo/ipv6_scan/result_data_save/dataset/alias.txt").readlines()   # 别名前缀文件
    # origin_samples = open("/home/chengdaguo/ipv6_scan/result_data_save/dataset/test.txt").readlines()   #地址文件
    # delete_alias_ip(alias,origin_samples,sub_output)
    
    