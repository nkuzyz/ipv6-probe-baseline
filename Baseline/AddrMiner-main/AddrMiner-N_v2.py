"""
    Probing in BGP-N
"""
from AD_Tools import *
from UGCPM import *
from GraphCommunity import *
from generatePD import *
import argparse,os,re
from tqdm import tqdm
from ActiveScan import scan_addr_list

def getIPv6Address():
    output = os.popen("ifconfig").read()
    # print(output)
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]
def generateTarget(PD, bgp_n, bgplen2prefix64, target_file,budget=1e6):
    """
    Args:
        PD: address pattern library
        budget: Limit the number of generated destination addresses
    """
    # Organizational association strategy
    result = []
    new_ipv6 = []
    limit = len(bgp_n)
    with tqdm(total=limit) as pbar:
        for ll,bgp in enumerate(bgp_n):
            new_ipv6 += OrgRel(bgp, PD, bgplen2prefix64, budget)
            if budget >=5000:
                if ll!=0 and ll % 10000 == 0:
                    result.append(scan_addr_list(target_file,new_ipv6,ll//10000))
                    new_ipv6 = []
            pbar.update(1)
        result.append(scan_addr_list(target_file,new_ipv6,ll))
    
    filename = target_file+"/analydata.txt"
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

    

def Start():
    """
    python AddrMiner-N.py --prefix=dataset1_all_no_seeds_prefix.txt --output=result --budget=1000
    sudo python3 AddrMiner-N.py --prefix=2606:2800:235::/48 --output=result --budget=10000 --IPv6=XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX
    """
    parse=argparse.ArgumentParser()
    # parse.add_argument('--prefix',type=str,help='prefix directory name')
    # parse.add_argument('--output', type=str, default='result', help='output directory name')
    # parse.add_argument('--budget',type=int, default=1e6, help='the upperbound of scan times')
    # parse.add_argument('--IPv6',type=str, help='local IPv6 address')
    parse.add_argument('--hmin',type=float, default=14.0, help='similarity threshold')
    parse.add_argument('--hmax',type=float, default=16.0, help='similarity threshold')
    parse.add_argument('--algorithm',type=str, default='louvain', help='graph community discovery algorithm')
    parse.add_argument('--sst',type=int,default=1e7,help="mode space upper limit")
    parse.add_argument('--types',type=int,default=4,help='nibble value type threshold')
    parse.add_argument('--emin',type=float,default=0.4,help='Shannon entropy lower bound,(0,1)')
    parse.add_argument('--emax',type=float,default=0.8,help='Shannon entropy upper bound,(0,1)')
    args = parse.parse_args()
    
    
    # args.prefix = 'Baseline/Database/dataset2_all_no_seeds_prefix.txt'
    # args.diroutput = 'Baseline/AddrMiner/dateset2'
    num = 2
    args.prefix = 'Baseline/Database/dataset{}_all_no_seeds_prefix.txt'.format(num)
    args.diroutput = 'Baseline/AddrMiner-main/dateset{}'.format(num)

    # args.prefix = 'Baseline/Database/test_pre.txt'
    # args.diroutput = 'Baseline/AddrMiner/result'
    
  
    
    
    f =  open(args.prefix, 'r').readlines()
    data = [i.split(',')[1] for i in f]
    print('[+]load data..')
    multi_level = dataloader("Baseline/AddrMiner-main/data/dataset{}.csv".format(num), "Baseline/AddrMiner-main/data/ipasn.20230522.dat")
    print('[+]load PD..')
    PD = getPD(num)
    print('[+]load bgp_n..')
    multi_level['prefix_len'] = multi_level['bgp_prefix'].map(lambda x:x.split("/")[1])
    bgplen2prefix64 = getBgplen2prefix64(multi_level)
    
    print('[+]generate target address..')

    # budgets = [10]
    budgets = [100,1000,5000,10000] # 艹，这里是每个前缀的预算，不是总预算
    for budget in budgets:
        args.output = args.diroutput + '/no_{}'.format(budget)
        os.makedirs(args.output, exist_ok=True)
        
        target_file = args.output
        result_file = args.output+"/result-N.txt"
        generateTarget(PD, data, bgplen2prefix64, target_file,budget=budget)

        # activeAddr = Scan(new_ipv6, getIPv6Address(), args.output,0)
        # with open(result_file,'wb') as f:
        #     for addr in activeAddr:
        #         f.write(addr.encode())
        #         f.write('\n'.encode())
        # print(str(budget)+' [+]Over!')

        # with open(target_file, 'r') as f:
        #     target_Nnum = len(f.readlines())
        
        # result_Nnum = len(activeAddr)
        # hitrate_N = result_Nnum / target_Nnum
        # with open(args.output+"/hit_rate.txt",'w') as f:
        #     f.write('target {}\nresult {}\nhit_rate {}\n'.format(target_Nnum,result_Nnum,hitrate_N))
        # print('target {}\nresult {}\nhit_rate {}\n'.format(target_Nnum,result_Nnum,hitrate_N))

if __name__ == "__main__":
    Start()

