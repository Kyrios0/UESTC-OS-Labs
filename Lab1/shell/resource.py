class RCB(object):
    def __init__(self, id, s):
        self.rid = id
        self.status = s
        self.waiting_list = []

class Resources(object):
    def __init__(self):
        self.rcbs = []
        # To-Do: support import config file
        for i in range(1, 5):
            self.rcbs.append(RCB(i, i))