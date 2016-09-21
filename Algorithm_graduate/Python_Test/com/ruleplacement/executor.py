'''
This file creates an excutor for algorithm testing and comparing.
Its basic steps are listed as below:
1. print some useful information for users or first developers, let them know how to operate
2. create a network topology following the principle as in this program, better refer to netTopo.py
3. create many many flows with a few characteristics
4. create a rule placement controller which doesn't exist in Mininet itself
5. choose an algorithm and then run it with (net_topo, flow_set, rule_controller) triple
6. evaluate the performance of an algorithm and make comparisons
'''

from netTopo import NetTopo
from flows import Flows
from Basic.matrix import FL_Matrix
from controller import RuleController
from ruleplacement.AlgLibrary.officer import Officer
from ruleplacement.AlgLibrary.linkRank import LinkRank
from evaluator import Evaluator


class Executor:

    def __init__(self):

        print "\nNow it's ready to test the algorithm performance with testing flows and a testing topo.\n"
        (sw_num, link_num, flow_num) = self.getParamOfNetAndFlow()

        self.Network = NetTopo(sw_num, link_num);self.Network.printTopoInfo()
        self.FlowClass = Flows(flow_num);self.FlowClass.printFlowsInfo()
        self.MatrixClass = FL_Matrix(flow_num,link_num)
        self.MatrixClass.printMatrixInfo("Before algorithm executing")
        self.Controller = RuleController(self.Network)
        self.Alg = self.chooseAlg(self.Controller, self.FlowClass.FlowSet, self.Network)



    def getParamOfNetAndFlow(self):
        sw_num = raw_input("\nPlease input the number of switches in the test network (press 'Enter' to choose "
                           "default a switch number = 8): ")
        if len(sw_num) < 1:
            sw_num = 8
        else:
            sw_num = int(sw_num)

        link_num = raw_input("Please input the number of links in the test network (press 'Enter' to choose "
                               "default a switch number = 9): ")
        if len(link_num) < 1:
            link_num = 9
        else:
            sw_num = int(link_num)

        f_num = raw_input("Please input the number of flows in the test network (press 'Enter' to choose "
                               "default a flow number = 10): ")
        if len(f_num) < 1:
            f_num = 10
        else:
            f_num = int(f_num)

        return (sw_num, link_num, f_num)

    def chooseAlg(self, con, flowS, topo):
        type = raw_input('\nPlease choose the rule placement algorithm you want to use (1 represents OFFICER and '
                         'others represents LinkRank): ')
        if len(type) < 1 or type not in str(range(10)):
            type = 1

        if int(type) == 1:
            print '\nYou choose algorithm OFFICER!'
            return Officer(con, flowS, topo)
        else:
            print '\nYou choose algorithm LinkRank'
            return LinkRank(con, flowS, topo)


if __name__ == '__main__':
    ex = Executor()
    ex.Alg.go(ex.MatrixClass)
    eva = Evaluator(ex.Network)
    print '\nOutput max resource usage: ', eva.max_link_usage, eva.max_switch_usage
    print '\nAll usage: ', eva.all_usage
