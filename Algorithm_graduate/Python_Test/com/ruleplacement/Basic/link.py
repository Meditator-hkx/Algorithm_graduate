import random

class Link:
    # this class is defined as a link in SDN network

    count = 0
    max_bw = 200 # Maximum bandwidth is 20Mbps

    def __init__(self):
        Link.count = Link.count + 1
        self.seq = Link.count
        self.link_used = 0
        self.link_usage = 0
        self.sw1 = 0
        self.sw2 = 0
        self.MAX_CAPACITY = self.getRandomSize(Link.count)
        self.CapacityLeft = self.MAX_CAPACITY

    def getRandomSize(self, seed = 100):
        random.seed(seed)
        return 10 + (Link.max_bw - 100) * random.random() # promise the minimum bw is 5Mbps

    def showInfo(self):
        print 'link %d: link_used %d, MAX_CAPACITY %f, switches connection %d --- %d' \
              %(self.seq, self.link_used, self.MAX_CAPACITY, self.sw1, self.sw2)

