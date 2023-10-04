import collections
import time, sys, os, re
import datetime
from math import exp, ceil
from _Definition import *
# from icmplib import ping
from Active_Scan import Scan


def update_reward(update_regions):
    alpha = 0.1
    for region in update_regions:
        try:
            r = (len(region.A) - len(region.D)) / len(region.node.unassigned_dimension)
        except ZeroDivisionError:
            r = 0
        region.reward = (1 - alpha) * region.reward + alpha * r

def getIPv6Address():
    output = os.popen("ifconfig").read()
    # print(output)
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]

class Alg2:
    def __init__(self, root: Node, beta: int, output_dir:str):
        self.root = root
        self.A = list()
        self.A_ = set()
        self.consumed_budget = 0
        self.beta = beta
        # self.source_ip = source_ip
        self.id = 0
        self.output_dir = output_dir

    def main_loop(self, b: int, s_time: int):
        def dfs(node: Node, father=None):
            if len(node.child_nodes) == 0:
                tmp_region = Region(node, father)
                if tmp_region.node_chipping():
                    chip_regions.append(tmp_region)
                else:
                    regions.append(tmp_region)
            else:
                for n in node.child_nodes:
                    dfs(n, node)

        def target_gen():
            def compute_prob():
                for rg in regions:
                    rg.prob = exp(rg.reward)
                    yield rg.prob

            prob_sum = sum(compute_prob())
            cur_b = 0
            for r in regions:
                if cur_b >= b:
                    break
                else:
                    target_num = min(b - cur_b, ceil(b * r.prob / prob_sum))
                    ret_a = []
                    for a in r.target_gen(target_num):
                        cur_b += 1
                        ret_a.append(a)
                    yield r, ret_a

        def do_chip(rs):
            addr_active = collections.defaultdict()
            addr_test = list()
            addr_test_str = list()
            print("-------要遍历的region数:",str(len(rs)))
            print(len(rs))
            for r in rs:
                time11=time.time()
                # print(r.D)
                for a in r.target_gen(-1):
                    # print(a)
                    if a not in self.A_:
                        self.consumed_budget += 1
                        addr_test.append(a)
                        str_a = str(a)
                        addr_test_str.append(str_a)
                        addr_active[str_a] = False
                if len(addr_test_str) >= self.beta:
                    break
            print(len(addr_test))
            print(len(addr_test_str))
            for a in Scan(addr_test_str, getIPv6Address(), self.output_dir, self.id):
                addr_active[a] = True
            self.id += 1
            for a in addr_test:
                if addr_active[str(a)]:
                    self.A_.add(a)

        def logout(f_out):
            hit_num = len(self.A_) - len(self.root.child_nodes[0].assigned_seed)
            use_time = int(time.time()) - s_time
            log = f"[*]consume {self.consumed_budget} hit {hit_num} in { datetime.timedelta(seconds=use_time)} hit rate = {float(hit_num)/self.consumed_budget}\n"
            f_out.write(log)
            print(log)

        # add seeds into A
        self.A_ = set(self.root.child_nodes[0].assigned_seed)
        # find all regions
        regions = list()
        chip_regions = list()
        dfs(self.root)

        # quit(0)
        # main loop
        with open(self.output_dir+'/progress.txt', 'a') as f_out:
            # node chipping
            chip_step = b // 10

            for i in range(0, len(chip_regions), chip_step):
                do_chip(chip_regions[i:min(i+chip_step, len(chip_regions))])
                logout(f_out)
            
            while self.consumed_budget <= self.beta:
                regions.sort(key=lambda r: r.reward, reverse=True)
                a_star = []
                update_regions = list()
                # ATest
                r_addr = []
                test_addr = set()
                addr_map = collections.defaultdict()
                for region, addrs in target_gen():
                    r_addr.append((region, addrs))
                    update_regions.append(region)
                    for addr in addrs:
                        str_addr = str(addr)
                        addr_map[str_addr] = False
                        if addr not in self.A_:
                            test_addr.add(str_addr)
                        else:
                            region.D.add(addr)
                for active_addr in Scan(test_addr, getIPv6Address(), self.output_dir, self.id):
                    addr_map[active_addr] = True
                self.id += 1
                for region, addrs in r_addr:
                    for addr in addrs:
                        if addr_map[str(addr)]:
                            region.A.append(addr)
                            a_star.append(addr)
                # self.A.extend(a_star)
                self.A_.update(set(a_star))
                update_reward(update_regions)
                self.consumed_budget += b
                if len(update_regions) <= len(regions) / 20:
                    raise SpaceRepartitionError()
                logout(f_out)
        return list(self.A_)
