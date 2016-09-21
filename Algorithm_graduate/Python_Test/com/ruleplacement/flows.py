from ruleplacement.Basic.flow import Flow
import random

class Flows(object):

    def __init__(self, flow_number = 10):
        self.FlowSet = []
        self.FlowNumber = flow_number # get a default flow number
        for i in range(self.FlowNumber):
            f = Flow()
            self.FlowSet.append(f)

        self.setFlowsPf();self.setFlowsWeight()

    def setFlowsPf(self): # set to be gauss distribution, failed... set to be exp distribution
        mu = Flow.max_pf / 2
        sigma = 1
        lambd = 0.5
        for flow in self.FlowSet:
            # flow.pf = random.gauss(mu, sigma)
            flow.pf = random.expovariate(lambd)

   # def setFlowsInOut(self): No need to set specially


    def setFlowsWeight(self):
        for flow in self.FlowSet:
            flow.weight = random.random()


    def printFlowsInfo(self):
        print "\nThe flows' information are shown as below:\n--------------------------------------------------"
        for num in range(self.FlowNumber):
            self.FlowSet[num].showInfo()