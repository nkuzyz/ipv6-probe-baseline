from _Definition import *
import Space_Partition as sp
import Target_Generation as tg
import time,os,re,sys



if __name__ == '__main__':
    
    #  *** super params ***

    dataset_name = 'dataset3'
    # prefix_num = 464
    prefix_num = 1
    # prefix_num = 449
    # prefix_num = 10000000 # 50000
    
    m = 476
    # m = 5228198  # number of seeds dataset1
    # m = 4928112  # number of seeds dataset2
    # m = 112
    # m = 1000000

    # num = [100,1000,5000,10000]
    num = [5000]

    budgets = [prefix_num*i for i in num]


    input_seeds = "Baseline/Database/{}.txt".format(dataset_name)  # file name of seeds' file
    output_dataset = "Baseline/6Hit/{}/".format(dataset_name)  # output directory name
    sys.stdout = open('Baseline/6Hit/{}_{}_log.txt'.format(dataset_name,prefix_num), 'a')
    # input_seeds ='Baseline/6Hit/test.txt'
    # output_dataset = "Baseline/6Hit/test/"
    

    for beta in budgets:
        b =  3*m # number of probes per round
        
        output_dir = output_dataset+str(beta)  # output directory name
        os.makedirs(output_dir, exist_ok=True)
        s_time = int(time.time())
        
        time1=time.time()
        root = sp.init_partition(seeds_num=m, file_name=input_seeds)
        time2=time.time()
        print("-------init_partition time:",time2-time1)
        sys.stdout.flush()
        # print(root)
        
        alg2 = tg.Alg2(root, beta,output_dir)  # 1 000
        print("--- Start scanning ...")
        sys.stdout.flush()
        while True:
            try:
                print("-------main_loop begin ...")
                sys.stdout.flush()
                time1=time.time()
                alg2.main_loop(b, s_time)
                time2=time.time()
                print("-------main_loop time:",time2-time1)
                sys.stdout.flush()
                break
            except SpaceRepartitionError:
                print("--- 重新分片 ...")
                sys.stdout.flush()
                time1=time.time()
                root = sp.space_repartition(m, addr_pool=alg2.A, pc=0.1, pu=0.01)
                alg2.root = root
                time2=time.time()
                print("-------space_repartition time:",time2-time1)
                sys.stdout.flush()
    
    sys.stdout.close()

    
