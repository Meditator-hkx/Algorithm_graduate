from ruleplacement.Basic.matrix import FL_Matrix
import copy

'''You have to finish this algorithm to make a comparison with officer under some conditions'''

class LinkRank:

    def __init__(self,  con, Flows, topo):
        self.controller = con
        self.FlowSet = Flows
        self.NetTopo = topo

    def go(self, matrix_class):

        # Step 1: Initiate a FL-Matrix to all-zero matrix
        self.fl_matrix = matrix_class  # Initiation has been done while instantiation
        # self.G = copy.deepcopy(self.NetTopo) # Initiate G* = G

        # Step 2: Sort flows by weights
        self.FlowsSortedByPf = self.controller.flowSort(self.FlowSet, keyword = 'pf')
        self.BigFlows, self.SmallFlows = self.controller.flowsPartition(self.FlowsSortedByPf, 0.8)

        # Step 3: deal with big flows
        for flow in self.BigFlows:
            self.dealWithBigFlow(flow)

        # Step 4: deal with small flows
        for flow in self.SmallFlows:
            self.dealWithSmallFlow(flow)

        # Step 5: Get the F-L matrix
        self.fl_matrix.printMatrixInfo("After algorithm executing")

    def dealWithBigFlow(self, flow, count = 3):
        k = count
        G = copy.copy(self.NetTopo)
        flag = False
        PathSetRecorded = []

        while k > 0:

            # Step 3-1: compute shortest path according to current G
            ShortPathSwitches = self.controller.computeShortestPath(flow, G)
            if len(ShortPathSwitches) < 2:
                break
            PathSetRecorded.append(ShortPathSwitches)

            # Step 3-2: Judge if safe allocation is possible
            if self.controller.canSafeAllocate(flow, ShortPathSwitches, self.NetTopo, 0.5):

                # Step 3-3 and 3-4: allocate rules and update link state
                self.controller.allocate(flow, ShortPathSwitches, self.NetTopo, self.fl_matrix.matrix)
                flag = True
                print '\nAllocation for flow %d is successful, and the route composed of switches is: ' % flow.seq, \
            ShortPathSwitches
                print 'the route composed of links is: ', self.NetTopo.findLinksBySwitches(ShortPathSwitches)
                break

            # 3-5: if count is not 0, then compute second shortest path with updating G by removing useless links
            else:
                print '\nLast safe allocation try failed!'

                # 3-6: update count(k) and G
                k -= 1
                self.controller.updateGraph(flow, G, self.NetTopo, ShortPathSwitches)

                # 3-7: return to Step 3-1
                continue

            # 3-8 to 3-10: if the last try by computing shortest path fails, then use chooseBestPath func
        if flag is False:
            print '\nAll tries of safe allocation fail, start link rank mode: '
            path_switches = self.controller.chooseBestPath(flow,self.NetTopo, PathSetRecorded) # the core of LinkRank
            if path_switches is not None:
                self.controller.allocate(flow, path_switches, self.NetTopo, self.fl_matrix.matrix)
                flag = True
            else:
                print '\nAllocation for flow %d finally failed!\n' %flow.seq

    def dealWithSmallFlow(self, flow): # Almost the same as OFFICER processing
        G = copy.copy(self.NetTopo)
        flag = False

        # Step 4-1-1: Default and deviated path computing
        self.controller.computeDefaultPath(self.NetTopo, flow)
        MultiRouteSwitches = self.controller.sortDefaultSwitches(self.NetTopo, flow)
        print '\nMultiple routes with switches are listed as: ', MultiRouteSwitches

        # Step 4-1-2: for every route in multi_routes, execute deviation
        for route_switches in MultiRouteSwitches:
            # Step 4-2: judge if safe allcation is possible
            if self.controller.canSafeAllocate(flow, route_switches, self.NetTopo):

                # Step 4-3 to 4-7: if safe allocation is allowed, then allocate and update links state
                self.controller.allocate(flow, route_switches, self.NetTopo, self.fl_matrix.matrix)
                flag = True
                print '\nAllocation for flow %d is successful, and the route composed of switches is: ' % flow.seq, \
                    route_switches
                print 'the route composed of links is: ', self.NetTopo.findLinksBySwitches(route_switches)
                # Step 8: start for next flow
                break

        # 4-8 to 4-10:
        if flag is False:

            print '\nAll tries of safe allocation fail, start link rank mode: '
            path_switches = self.controller.chooseBestPath(flow,self.NetTopo, MultiRouteSwitches)  # the core of LinkRank
            self.controller.allocate(flow, path_switches, self.NetTopo, self.fl_matrix.matrix)