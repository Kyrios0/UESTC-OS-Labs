from .process import Process, PCB
from .resource import Resources
import logging

class TestShell(object):
    def __init__(self):
        self.resources = Resources()

        self.ready_list = [[] for _ in range(3)] # store pcb
        self.process_list = [] # store process
        self.next_pid = 0
        # To-Do: add a prior queue for pid reusing 

        self.create_process(pname='init', prior=0, parent=None)

        self.running_process = 0

    def create_process(self, pname, prior, parent):
        pcb = PCB(self.next_pid, pname, prior, parent, self.ready_list[prior])
        self.ready_list[prior].append(pcb)
        self.process_list.append(Process(pcb))
        if parent != None:
            self.process_list[parent].add_child(self.next_pid)
        
        self.scheduler(self.next_pid)
        self.next_pid += 1

    def delete_process(self, pid):
        process = self.process_list[pid]

        for child in process.get_children():
            self.delete_process(child)
        # release all resources
        for rid, amount in process.get_resources():
            self.release(pid, rid, amount)
        process.get_queue().remove(process.get_pcb()) # pcb.queue.remove(pcb)
        del process

        self.scheduler(None)

    def request(self, pid, rid, n=1):
        rcb = self.resources.get_rcb(rid)
        process = self.process_list[pid]
        
        if rcb.status >= n:
            rcb.status -= n
            process.add_resource(rid, n)
        else:
            # To-Do: exception
            process.set_state('blocked')
            process.get_queue().remove(process.get_pcb()) # pcb.queue.remove(pcb)
            process.set_queue(rcb.waiting_list) # pcb.queue = rcb.waiting_list
            rcb.join_waiting(pid, n) # rcb.waiting_list.append(pcb)

            self.scheduler(pid)

    def release(self, pid, rid, n=1):
        rcb = self.resources.get_rcb(rid)
        process = self.process_list[pid]
        pcb = process.pcb

        process.sub_resource(rid, n)
        rcb.status += n

        bpid = None
        if len(rcb.waiting_list) > 0:
            if rcb.waiting_list.values()[0] <= rcb.status:
                # pop waiting_list[0]
                bpid, bn = list(rcb.waiting_list.items())[0]
                del rcb.waiting_list[bpid]

                bprocess = self.process_list[bpid]
                bprocess.set_state('ready')
                bprocess.set_queue(self.ready_list[bprocess.get_prior()])
                self.ready_list[bprocess.get_prior()].append(bprocess.get_pcb())
                bprocess.add_resource(rid, bn)
        self.scheduler(bpid)

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
            print("[Res%d]: %s" % (res_id, res_status))

    def clock_interrupt(self):
        process = self.process_list[self.running_process]
        pcb = process.get_pcb()
        prior = process.get_prior()

        process.set_state('ready')
        self.ready_list[prior].pop(0)
        self.ready_list[prior].append(pcb)

        self.scheduler(self.running_process)

    def scheduler(self, pid):
        # get highest priority process
        for prior in self.ready_list[::-1]:
            if len(prior) > 0:
                p = prior[0]
                break
        
        # called from delete_process
        if pid == None:
            # preempt p
            p.set_state('running')
            self.running_process = p.pid
            return

        s = self.process_list[pid]

        if s.get_state() != 'running' or s.get_prior() < p.get_prior():
            # preempt p
            p.set_state('running')
            self.running_process = p.pid
            return
        

    def run(self, logger):
        logger.info('test pass')