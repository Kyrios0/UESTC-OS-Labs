from .process import Process, PCB
from .resource import Resources
import logging


class TestShell(object):
    def __init__(self):
        self.ready_list = [[] for _ in range(3)]
        self.block_list = [[] for _ in range(3)]
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
        for child in self.process_list[pid].pcb.children:
            self.delete_process(child)
        # To-Do: collect resources
        del self.process_list[pid]

    def list_ready(self):
        for prior in range(3):
            prior_list = '-'.join([p.pcb.name for p in self.ready_list[prior]])
            print("[%d]: %s" % (prior, prior_list))

    def list_block(self):
        for prior in range(3):
            prior_list = '-'.join([p.pcb.name for p in self.block_list[prior]])
            print("[%d]: %s" % (prior, prior_list))

    def clock_interrupt(self):
        pass

    def scheduler(self):
        pass

    def run(self, logger):
        logger.info('test pass')