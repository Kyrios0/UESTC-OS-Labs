from .resource import Resources
from collections import Counter

class PCB(object):
    def __init__(self, pid, pname, prior, parent, queue):
        self.pid = pid
        self.name = pname
        self.status = 'ready' # ready / running / blocked
        self.priority = prior # 0: init, 1: user, 2: system
        self.resources = {} # rid: amount
        self.parent = parent
        self.children = []
        self.queue = queue
    
    def add_child(self, pid):
        self.children.append(pid)

    def del_child(self, pid):
        self.children.remove(pid)
    
    def add_resource(self, rid, n):
        self.resources = dict(Counter(self.resources) + Counter({rid: n}))

    def sub_resource(self, rid, n):
        # To-Do: exception
        self.resources = dict(Counter(self.resources) - Counter({rid: n}))

    def get_resources(self):
        return self.resources.items()

    def get_children(self)：
        return self.children

    def get_queue(self):
        return self.queue

    def set_state(self, state):
        self.status = state

    def set_queue(self, queue):
        self.queue = queue

class Process(object):
    def __init__(self, pcb):
        self.pcb = pcb
    
    def add_child(self, pid):
        self.pcb.add_child(pid)

    def del_child(self, pid):
        self.pcb.del_child(pid)

    def add_resource(self, rid, n):
        self.pcb.add_resource(rid, n)

    def sub_resource(self, rid, n):
        self.pcb.sub_resource(rid, n)

    def get_resources(self):
        return self.pcb.get_resources()

    def get_children(self):
        return self.pcb.get_children()

    def get_queue(self):
        return self.pcb.get_queue()

    def get_prior(self):
        return self.pcb.get_prior()
        
    def get_pcb(self):
        return self.pcb

    def set_state(self, state):
        self.pcb.set_state(state)

    def set_queue(self, queue):
        self.pcb.set_queue(queue)

    def __del__(self):
        del self.pcb