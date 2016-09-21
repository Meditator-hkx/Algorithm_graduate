from netTopo import NetTopo
from flows import Flows
from ruleplacement.Basic.flow import Flow
from Basic.matrix import FL_Matrix
from controller import RuleController
from ruleplacement.AlgLibrary.officer import Officer
from ruleplacement.AlgLibrary.linkRank import LinkRank

# net = NetTopo()
# net.setTopo()
# net.printTopoInfo()
# print '\nCorreSwitches searching test: ', net.findCorreSwitches(7) # test passes
#
# FlowS = Flows(10)
# FlowS.printFlowsInfo()
#
# m = FL_Matrix()
# m.printMatrixInfo()
#
#
# con = RuleController(net)
#
# NewFlows = con.flowSort(FlowS.FlowSet)
# con.printNewFlowInfo(NewFlows)
#
# print '\nflow default path computing test: ', con.computeDefaultPath(net, NewFlows[0])
#
# # test_path_switches = [[1,2,3],[1,2,4],[5,7,8]]
# # links = net.findLinksBySwitches(test_path_switches)
# # print '\nfindLinksBySwitches test: ', links # test func findLinksBySwitches in NetTopo, test passes
#
# # test func sortDefaultPath in controller
# f_test = Flow()
# f_test.innode, f_test.outnode = 5, 6
# f_test.seq = 100
# f_test.DefaultPath_switches =[[8, 7, 5]]
# multi_route = con.sortDefaultSwitches(net, f_test)
# print '\nsortDefaultSwitches func test: ', multi_route

# Officer algorithm test
# net = NetTopo()
# net.setTopo()
# net.printTopoInfo()
#
# FlowS = Flows(10)
# FlowS.printFlowsInfo()
#
# con = RuleController(net)
# NewFlows = con.flowSort(FlowS.FlowSet, keyword = 'pf')
# print 'New flows are: ', NewFlows
# Big, Small = con.flowsPartition(NewFlows)
# con.printNewFlowInfo(NewFlows)
# print 'Big flows has ', len(Big), ' and small flows has ', len(Small)

# of = Officer(con, FlowS.FlowSet, net)

# LinkRank algorithm test
# net = NetTopo()
# net.setTopo()
# net.printTopoInfo()
#
# FlowS = Flows(10)
# FlowS.printFlowsInfo()
#
# con = RuleController(net)
# NewFlows = con.flowSort(FlowS.FlowSet, keyword = 'pf')
# print 'New flows are: ', NewFlows
# Big, Small = con.flowsPartition(NewFlows)
# con.printNewFlowInfo(NewFlows)
# print '\nBig flows has ', len(Big), ' and small flows has ', len(Small)
#
# lr = LinkRank(con, FlowS.FlowSet, net)

# test matrix specifically

fl_matrix_class = FL_Matrix(fnum=15)
fl_matrix_class.printMatrixInfo("Test fnum = 15 ")
fl_matrix_class.matrix[14][1] = 1
fl_matrix_class.printMatrixInfo("After giving a specific value")

