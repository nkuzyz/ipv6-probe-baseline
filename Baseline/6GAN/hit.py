from ActiveScang import scan_addr_list
import os,random,ipaddress
import re

def validate_string(input_string):
    pattern = r'^[0-9a-f:]{39}$'
    if re.match(pattern, input_string):
        return True
    else:
        return False
# 遍历一个文件夹下的文件
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files

def is_ipv6_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return ip.version == 6
    except ValueError:
        return False


if __name__ == '__main__':
    dataset ='Baseline/6GAN/dataset3_little_copy/'
    # budgets = [46400,464000,2320000,4640000]
    # 44900 449000 2245000 4490000
    # budgets = [44900,449000,2245000,4490000]
    budgets = [5000]
    for budget in budgets:
        print(budget)
        file_dir = dataset+'candidate_set_{}'.format(budget)
        print(file_dir)
        files = file_name(file_dir+'/data/')
        result = []
        # # 每个文件都自己测自己的
        # for ll,file in enumerate(files):
        #     print(file)
        #     file_path = file_dir+'/data/'+file
        #     sample = []
        #     with open(file_path, 'r') as f:
        #         lines = f.readlines()
        #         # sample = [i.strip() for i in lines]
        #         for i in lines:
        #             i=i.strip()
        #             if is_ipv6_address(i):
        #                 sample.append(i)
        #     result.append(scan_addr_list(file_dir,sample,ll))
        
        # 合起来抽样
        samples = set()
        print(files)
        for ll,file in enumerate(files):
            file_path = file_dir+'/data/'+file
            with open(file_path, 'r') as f:
                lines = f.readlines()
                # sam = [i.strip() for i in lines]
                sam = []
                for i in lines:
                    i=i.strip()
                    if is_ipv6_address(i):
                        sam.append(i)
                # print(len(sam))
                samples = samples | set(sam)
        print(len(samples))
        if len(samples) > budget:
            sample = random.sample(samples,budget)
        else:
            sample = samples
        print(len(sample))
        result.append(scan_addr_list(file_dir,sample))
        
        # file_generate_samples = file_dir+"generate_samples.txt"
        # os.makedirs(os.path.dirname(file_generate_samples),exist_ok=True)

        filename = file_dir+"/analydata.txt"
        os.makedirs(os.path.dirname(filename),exist_ok=True)
        t = 0.0
        a = 0.0
        with open(filename,"w") as w:
            for r in result:
                t += r[0]
                a += r[1]
                w.write(str(r)+'\n')
            h = a/t if t!=0 else 0
            w.write("total : target {} , active {} , hit_rate {} \n".format(t,a,h))
