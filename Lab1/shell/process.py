from .resource import Resources

class PCB(object):
    def __init__(self, pid, pname, prior, parent):
        self.pid = pid
        self.name = pname
        self.status = 'ready' # ready / running / block
        self.priority = prior # 0: init, 1: user, 2: system
        self.resources = {}
        self.parent = parent
        self.children = []
    
    def add_child(self, pid):
        self.children.append(pid)

    def del_child(self, pid):
        self.children.remove(pid)

class Process(object):
    def __init__(self, pcb):
        self.pcb = pcb
    
    def add_child(self, pid):
        self.pcb.add_child(pid)

    def del_child(self, pid):
        self.pcb.del_child(pid)

    def request(self, rid, n=1):
        pass

    def release(self, rid, n=1):
        pass

    def __del__(self):
        del self.pcb