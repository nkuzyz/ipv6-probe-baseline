import ipaddress,sys,time

from iteration_utilities import first
from random import sample, choice, randint


class Addr:
    def __init__(self, ipv6addr: str):
        if ":" not in ipv6addr:
            ipv6addr = int(ipv6addr, 16)
        self.ipv6addr = ipaddress.IPv6Address(ipv6addr)
        self.addr = int(self.ipv6addr.exploded.replace(":", ""), 16)

    def __getitem__(self, item: int) -> int:
        assert (1 <= item <= 32)
        return int(hex(self.addr)[1 + item], 16)

    def __hash__(self):
        return self.addr.__hash__()

    def __eq__(self, other):
        return self.addr.__eq__(other.addr)

    def __str__(self):
        return str(self.ipv6addr)

    def to_hex(self):
        return hex(self.addr)[2:]


class Node:
    def __init__(self, assigned_value=None):
        self.assigned_dimension = set()
        self.assigned_seed = set()
        self.child_nodes = list()
        self.assigned_value = assigned_value

    @property
    def unassigned_dimension(self):
        return set([i for i in range(1, 33)]) - self.assigned_dimension

    def add_assigned_dimension(self):
        for dimension in self.unassigned_dimension:
            c = set()
            for seed in self.assigned_seed:
                c.add(seed[dimension])
                if len(c) > 1:
                    break
            if len(c) == 1:
                self.assigned_dimension.add(dimension)

    def is_r_node(self) -> bool:
        return self.assigned_value is not None


class Region:
    def __init__(self, node, father):
        self.father = father  # father node
        self.node = node
        try:
            self.reward = 0 if node.is_r_node() else len(node.assigned_seed) / len(node.unassigned_dimension)
        except ZeroDivisionError:
            self.reward = 0
        self.D = set()  # duplicate nodes
        self.A = list()
        self.prob = 0
        self.count = 0

    def __str__(self):
        return f"node is {self.node.assigned_dimension}\nreward is {self.reward}\n"

    def node_chipping(self):
        unassigned_dimension = self.node.unassigned_dimension
        if len(unassigned_dimension) > 0:
            limit = 16 ** (len(unassigned_dimension) - 1) / len(unassigned_dimension)
            if self.reward > limit:
                return True
        return False

    def target_gen(self, num: int):
        self.A.clear()
        if len(self.node.assigned_dimension) == 32:
            return []
        unassigned_dimension = self.node.unassigned_dimension
        limit = 16 ** len(unassigned_dimension)
        if self.node.assigned_seed:
            seed_pattern = first(self.node.assigned_seed).to_hex()
        else:
            return []
        # seed_pattern = first(self.node.assigned_seed).to_hex()
        # print(seed_pattern)
        target_pattern = ['*'] * 32
        for i in self.node.assigned_dimension:
            target_pattern[i - 1] = seed_pattern[i - 1]
        if num <= 0 or num > limit:
            # if num is not normal, it means search all region
            num = limit

        if self.node.is_r_node():
            # raise ValueError("Cannot get an element from r node!")
            # print("$$$ Trying to get {num} ips from r node!")
            cur_num = 0
            selected = list()
            
            while cur_num < num:
                for i, dimension in enumerate(unassigned_dimension):
                    s = hex(randint(0, 15))[2:]
                    while s in self.node.assigned_value[dimension]:
                        s = hex(randint(0, 15))[2:]
                    target_pattern[dimension - 1] = s
                t = "".join(target_pattern)
                if t not in selected:
                    yield Addr(t)
                    cur_num += 1
                    selected.append(t)   
        else:
            for target_random in sample(range(limit), num) if num < limit else range(limit):
                s = ipaddress.IPv6Address(target_random).exploded.replace(":", "")[32 - len(unassigned_dimension):]
                for i, dimension in enumerate(unassigned_dimension):
                    target_pattern[dimension - 1] = s[i]
                yield Addr("".join(target_pattern))

    def target_gen_record(self, num: int):
        self.count = 0
        self.A.clear()
        if len(self.node.assigned_dimension) == 32:
            return []
        unassigned_dimension = self.node.unassigned_dimension
        
        if len(unassigned_dimension) > 2:
            limit = 16 ** 2
        else:
            limit = 16 ** len(unassigned_dimension)
        
        if self.node.assigned_seed:
            seed_pattern = first(self.node.assigned_seed).to_hex()
        else:
            return []
        # seed_pattern = first(self.node.assigned_seed).to_hex()
        # print(seed_pattern)
        target_pattern = ['*'] * 32
        for i in self.node.assigned_dimension:
            target_pattern[i - 1] = seed_pattern[i - 1]
        if num <= 0 or num > limit:
            # if num is not normal, it means search all region
            num = limit

    
        if self.node.is_r_node():
            # raise ValueError("Cannot get an element from r node!")
            # print("$$$ Trying to get {num} ips from r node!")
            cur_num = 0
            selected = list()
            # print("-------r_node_start-------")
            # sys.stdout.flush()
            # time_r_start = time.time()
           
            while cur_num < num:
                self.count += 1
                for i, dimension in enumerate(unassigned_dimension):
                    s = hex(randint(0, 15))[2:]
                    while s in self.node.assigned_value[dimension]:
                        s = hex(randint(0, 15))[2:]
                    target_pattern[dimension - 1] = s
                t = "".join(target_pattern)
                if t not in selected:
                    yield Addr(t)
                    cur_num += 1
                    selected.append(t)
            
            # print("-------r_node_time:",time.time()-time_r_start)
            # print("-------r_node_count循环次数:",count)
            # print("-------r_node_end-------")
            # sys.stdout.flush()
        else:
            # print("-------not_r_node_start-------")
            # sys.stdout.flush()
            # time_not_r_start = time.time()
            # count = 0
            for target_random in sample(range(limit), num) if num < limit else range(limit):
                self.count += 1
                s = ipaddress.IPv6Address(target_random).exploded.replace(":", "")[32 - len(unassigned_dimension):]
                for i, dimension in enumerate(unassigned_dimension):
                    target_pattern[dimension - 1] = s[i]
                yield Addr("".join(target_pattern))
            # print("-------not_r_node_time:",time.time()-time_not_r_start)
            # print("-------not_r_node_count循环次数:",count)
            # print("-------not_r_node_end-------")
        print ("-------count:",self.count)
        sys.stdout.flush()


class SpaceRepartitionError(Exception):
    pass
