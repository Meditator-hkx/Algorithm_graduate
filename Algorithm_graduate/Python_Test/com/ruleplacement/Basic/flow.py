import random

class Flow:
    count = 0
    max_weight = 10 # Just a metric for the importance of a flow
    max_pf = 5 # 5Mbps

    def __init__(self, switch_number = 8):
        Flow.count = Flow.count + 1
        self.seq = Flow.count
        self.weight = 0
        self.pf = 0
        self.DefaultPath_links = None
        self.DefaultPath_switches = None
        self.innode, self.outnode = self.getRandomInOut(switch_number)

    def getRandomWeight(self, seed = 10):
        random.seed(seed)
        return Flow.max_weight * random.random()

    def getRandomInOut(self,sw_number = 8):
        self.innode, self.outnode = 0, 0
        random.seed(20 * self.seq)
        while self.innode == self.outnode:
            self.innode = int(sw_number * random.random() + 1)
            self.outnode = int(sw_number * random.random() + 1)
        return self.innode, self.outnode

    def showInfo(self):
        print 'Flow %d: weight %f, packet rate %fMbps, in-out set (%d, %d)' \
              %(self.seq, self.weight, self.pf, self.innode, self.outnode)