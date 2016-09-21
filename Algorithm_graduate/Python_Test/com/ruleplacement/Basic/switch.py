import random

class Switch:
    # this class is defined as an OpenFlow Switch that forwards flows to other switches or exports

    count = 0 # class variable
    max_num = 15 # the maximum number of rule space

    def __init__(self):
        Switch.count = Switch.count + 1
        self.seq = Switch.count
        self.rule_num = 0
        self.MAX_MEM_SIZE = self.getRandomSize(Switch.count)
        self.RuleSpaceLeft = self.MAX_MEM_SIZE

    def getRandomSize(self, seed = 1000):
        random.seed(seed)
        return int(10 + Switch.max_num * random.random())

    def showInfo(self):
        print 'switch %d: rule_num %d, MAX_MEM_SIZE %f' %(self.seq, self.rule_num, self.MAX_MEM_SIZE)