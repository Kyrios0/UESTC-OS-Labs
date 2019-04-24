from .process import Process, PCB
from .resource import Resources
import logging

class TestShell(object):
    def __init__(self):
        self.resources = Resources()

        self.ready_list = [[] for _ in range(3)]
        self.process_list = []
        self.next_pid = 0
        # To-Do: add a prior queue for pid reusing 

        self.create_process(pname='init', prior=0, parent=None)

    def create_process(self, pname, prior, parent):
        pcb = PCB(self.next_pid, pname, prior, parent)
        self.ready_list[prior].append(pcb)
        self.process_list.append(Process(pcb))
        if parent != None:
            self.process_list[parent].add_child(self.next_pid)
        self.next_pid += 1   

    def delete_process(self, pid):
        process = self.process_list[pid]
        for child in self.process.pcb.children:
            self.delete_process(child)
        # release all resources
        for rid, amount in process.get_resources():
            self.release(pid, rid, amount)
        # **To-Do**: unlink
        del process

    def request(self, pid, rid, n=1):
        pass

    def release(self, pid, rid, n=1):
        pass

    def list_ready(self):
        for prior, pri_ready_list in enumerate(self.ready_list):
            print("[Pri%d]: %s" % (prior, '-'.join([pcb.name for pcb in pri_ready_list])))

    def list_block(self):
        block_list = self.resources.get_block_list()
        for res_id, res_block_list in enumerate(block_list):
            print("[Res%d]: %s" % (res_id, '-'.join([pcb.name for pcb in res_block_list])))

    def list_res(self):
        res_list = self.resources.get_res_list()
        for res_id, res_status in enumerate(res_list):
            print("[Res%d]: %s" % (res_id, res_status)))

    def clock_interrupt(self):
        pass

    def scheduler(self):
        pass

    def run(self, logger):
        logger.info('test pass')