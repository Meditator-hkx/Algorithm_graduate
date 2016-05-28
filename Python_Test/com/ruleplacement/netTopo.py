from ruleplacement.Basic.link import Link
from ruleplacement.Basic.switch import Switch

class NetTopo:
    # this class is defined as a SDN network, which includes switches and links
    def __init__(self, sw_num = 8, link_num = 9):
        self.SwitchNumber = sw_num
        self.LinkNumber = link_num
        # default numbers are given for a test network
        self.SwitchSet = []
        self.LinkSet = []

        print '\nThis is the first python version algorithm with a test topo, a default topo is given'
        self.setTopo()

    def setTopo(self):
        self.SwitchNumber = 8
        self.LinkNumber = 9

        # Initiate switches and links
        for num in range(1,self.SwitchNumber+1):
            switch = Switch()
            self.SwitchSet.append(switch)
        for num in range(1,self.LinkNumber+1):
            link = Link()
            self.LinkSet.append(link)

        # Initiate default links' parameter
        self.LinkSet[0].sw1, self.LinkSet[0].sw2 = 1, 2
        self.LinkSet[1].sw1, self.LinkSet[1].sw2 = 2, 3
        self.LinkSet[2].sw1, self.LinkSet[2].sw2 = 2, 4
        self.LinkSet[3].sw1, self.LinkSet[3].sw2 = 3, 5
        self.LinkSet[4].sw1, self.LinkSet[4].sw2 = 4, 6
        self.LinkSet[5].sw1, self.LinkSet[5].sw2 = 5, 6
        self.LinkSet[6].sw1, self.LinkSet[6].sw2 = 5, 7
        self.LinkSet[7].sw1, self.LinkSet[7].sw2 = 7, 8
        self.LinkSet[8].sw1, self.LinkSet[8].sw2 = 6, 8

        # Initiate the location of controller...
        self.controller_neighbours = [8]

    def findCorreSwitches(self, ini_seq):
        self.CorreSwitches = []
        for link in self.LinkSet:
            if (link.sw1 == ini_seq):
                self.CorreSwitches.append(link.sw2)
            elif (link.sw2 == ini_seq):
                self.CorreSwitches.append(link.sw1)
        return self.CorreSwitches

    def findLinksBySwitches(self, switches):
        self.links = []
        for i in range(len(switches) - 1):
            for j in range(i+1, len(switches)):
                self.one_sw = switches[i]
                self.the_other_sw = switches[j]
                for link in self.LinkSet:
                    if link.sw1 == self.one_sw and link.sw2 == self.the_other_sw:
                        self.links.append(link.seq)
                    elif link.sw2 == self.one_sw and link.sw1 == self.the_other_sw:
                        self.links.append(link.seq)
        return self.links




    def printTopoInfo(self):
        print '\nThere are %d switches and %d links in this network topology.' %(self.SwitchNumber,self.LinkNumber)
        print "The switches' information are shown as below:\n--------------------------------------------------"
        for num in range(self.SwitchNumber):
            self.SwitchSet[num].showInfo()
        print '--------------------------------------------------'
        for num in range(self.LinkNumber):
            self.LinkSet[num].showInfo()
