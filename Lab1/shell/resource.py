def dict_plus(x, y):
    for k, v in y.items():
        if k in x.keys():
            x[k] += v
        else:
            x[k] = v
    return x

class RCB(object):
    def __init__(self, rid, s):
        self.rid = rid
        self.status = s
        self.waiting_list = {} # {pcb: n}

    def join_waiting(self, pid, n):
        self.waiting_list = dict_plus(self.waiting_list, {pid: n})

class Resources(object):
    def __init__(self):
        self.rcbs = []
        # To-Do: support import config file
        for i in range(1, 5):
            self.rcbs.append(RCB(i, i))
    
    def get_rcb(self, rid):
        return self.rcbs[rid]

    def get_block_list(self):
        return [rcb.waiting_list for rcb in self.rcbs]

    def get_res_list(self):
        return [rcb.status for rcb in self.rcbs]