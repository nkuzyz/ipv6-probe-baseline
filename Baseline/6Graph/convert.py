# convert IPv6 str to numpy seeds.npy
import numpy as np
from IPy import IP
import sys,os


def convert(filename,outputfile):
    with open(filename+".txt") as f:
        arrs = []
        # for ip in f.read().splitlines()[:10000]:
        for ip in f.read().splitlines():
            ip = ip.split(",")[0]
            arrs.append([int(x, 16)
                        for x in IP(ip).strFullsize().replace(":", "")])
        
        np.save(outputfile+"/data.npy", np.array(arrs, dtype=np.uint8))
