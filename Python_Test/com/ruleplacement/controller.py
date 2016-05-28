from flows import Flows
from netTopo import NetTopo

class RuleController(object):

    def __init__(self, topo):
        self.NetTopo = topo
        self.NeighbourSwitches = topo.controller_neighbours # Get neighbour switches

    def flowSort(self, FlowSet, keyword = 'weight'):
        if keyword is 'weight': # sorted by weight
            return sorted(FlowSet, key = lambda flow: flow.weight, reverse = True)
        elif keyword is 'pf': # sorted by bandwidth
            return sorted(FlowSet, key = lambda flow: flow.pf, reverse = True)

    def flowsPartition(self, FlowSet, p = 0.8): # Partition flows into big flows and small flows
        Big = [];Small = []
        pf_sum = 0
        for flow in FlowSet:
            pf_sum += flow.pf
        pf_p = pf_sum * p

        sum_recur = 0
        for flow in FlowSet:
            if sum_recur < pf_p:
                sum_recur += flow.pf
                Big.append(flow)
            else:
                Small.append(flow)

        return Big, Small

    def computeShortestPath(self, flow, G):
        # compute BFS for a flow under the topo condition
        self.BFS(G, flow.innode)
        print '\nAfter BFS processing,  the distance list looks like: ', self.distance

        path_switches = []
        seq_recur = flow.outnode
        path_switches.append(seq_recur)
        while self.last_node[seq_recur - 1] != 0:
            seq_recur = self.last_node[seq_recur - 1]
            path_switches.append(seq_recur)
    #    path_links = G.findLinksBySwitches(path_switches)
        return path_switches

    def computeDefaultPath(self, topo, flow):

        # compute BFS for a flow under the topo condition
        self.BFS(topo, flow.innode)

        print '\nAfter BFS processing,  the distance list looks like: ', self.distance

        # find the min distance towards f_innode and the switch number beside controller
        self.MinSeqSet = []
        self.min_distance, self.min_seq = 100, 0 # set default min_distance and min_seq
        for neigbour_seq in self.NeighbourSwitches:
            if self.min_distance > self.distance[neigbour_seq - 1]:
                self.min_distance = self.distance[neigbour_seq - 1]
        for neigbour_seq in self.NeighbourSwitches:
            if self.distance[neigbour_seq - 1] == self.min_distance:
                self.MinSeqSet.append(neigbour_seq)

       # print '\nMinSeqSet info: ',self.MinSeqSet

        # find the default_path composed of switches
        self.default_path_switches = []
        for seq in self.MinSeqSet:
            self.one_path = []
            self.seq_recur = seq
            self.one_path.append(self.seq_recur)
            while self.last_node[self.seq_recur - 1] != 0:
                self.seq_recur = self.last_node[self.seq_recur - 1]
                self.one_path.append(self.seq_recur)
            self.default_path_switches.append(self.one_path)

        self.default_path_links = topo.findLinksBySwitches(self.default_path_switches)
        flow.DefaultPath_switches, flow.DefaultPath_links = self.default_path_switches, self.default_path_links

        return self.default_path_switches, self.default_path_links

    def sortDefaultSwitches(self, topo, flow):
        self.MultiRoutes = []
        self.BFS(topo,flow.outnode)

        # choose the diverting point
        divert_distance, divert_seq, divert_index = 100, 0, 0
        DefaultPathOne = flow.DefaultPath_switches[0]

        # print '\nThe first default_path composed of switches for flow %d is: ' %flow.seq, DefaultPathOne

        count = -1 # it is used to get divert_index
        for switch_seq in DefaultPathOne:
            count += 1
            if self.distance[switch_seq - 1] < divert_distance: # list index out of range, debug over
                divert_distance = self.distance[switch_seq - 1]
                divert_index = count

        # TempSwitchSetInRoute is used for loop from the first diverting point to the last one
        TempSwitchSetInRoute = []
        for num in range(divert_index, len(DefaultPathOne)):
            TempSwitchSetInRoute.append(DefaultPathOne[num])

        while len(TempSwitchSetInRoute) > 0:
            OneRoute = []
            divert_seq = TempSwitchSetInRoute.pop(0)

            # add switches between divert_seq and outnode into one_route
            seq_recur = divert_seq
            OneRoute.insert(0, seq_recur)

            while self.last_node[seq_recur - 1] != 0:
                seq_recur = self.last_node[seq_recur - 1]
                OneRoute.insert(0, seq_recur)

            # add switches on DefaultPathOne
            for ele in TempSwitchSetInRoute:
                OneRoute.append(ele)
            self.MultiRoutes.append(OneRoute)

        for route in self.MultiRoutes:
            # delete the route which is not reasonable
            for item in route:
                if route.count(item) > 1:
                    self.MultiRoutes.remove(route)
                    break
        # end route adding

        # delete repetitive route data
        self.ReturnRoutes = []
        for route in self.MultiRoutes:
            if route not in self.ReturnRoutes:
                self.ReturnRoutes.append(route)
        return self.ReturnRoutes
    # waiting for testing and debugging

    def BFS(self, topo, node_seq):
        # Iniate visted[], last_node[] and distance[]
        self.visted = []
        self.last_node = []
        self.distance = []
        for num in range(topo.SwitchNumber):
            self.visted.append(False)
            self.last_node.append(0)
            self.distance.append(0)

        self.check_list = []
        self.check_list.append(node_seq)
        while len(self.check_list) > 0:
            self.ini_seq = self.check_list.pop(0)
            self.visted[self.ini_seq - 1] = True
            self.neighbours = topo.findCorreSwitches(self.ini_seq)

            # print 'Neighbours of switch %d' % self.ini_seq, ' is ', self.neighbours

            for switch_seq in self.neighbours:
                if self.visted[switch_seq - 1] == False and self.last_node[switch_seq - 1] == 0:
                    self.check_list.append(switch_seq)
                    self.last_node[switch_seq - 1] = self.ini_seq

        # set distance to right values
        for switch_seq in range(topo.SwitchNumber):
            if switch_seq == node_seq:
                continue
            self.seq_recur = switch_seq
            while self.last_node[self.seq_recur - 1] != 0:
                self.distance[switch_seq - 1] += 1
                self.seq_recur = self.last_node[self.seq_recur - 1]

            #   print '\nSome useful debug info: ', self.visted, self.last_node, self.distance

    def canAllocate(self, flow, route_switches, topo):
        route_links = topo.findLinksBySwitches(route_switches) # findLinksBySwitches func is not proper
        for switch_seq in route_switches:
            if topo.SwitchSet[switch_seq - 1].RuleSpaceLeft <= 0:
               return False
        for link_seq in route_links:
            if topo.LinkSet[link_seq - 1].CapacityLeft < flow.pf:
                return False
        return True # if only there are route satisfying such conditions, return True

    def canSafeAllocate(self, flow, route_switches, topo, u = 0.5):
        route_links = topo.findLinksBySwitches(route_switches)  # findLinksBySwitches func is not proper
        for switch_seq in route_switches:
            if topo.SwitchSet[switch_seq - 1].RuleSpaceLeft <= 0:
                return False
        for link_seq in route_links:
            suppose_pf = topo.LinkSet[link_seq - 1].link_used + flow.pf
            if suppose_pf / topo.LinkSet[link_seq - 1].MAX_CAPACITY > u:
                return False
        return True

    def allocate(self, flow, route_switches, topo, matrix):
        route_links = topo.findLinksBySwitches(route_switches)
        for switch_seq in route_switches:
            topo.SwitchSet[switch_seq - 1].RuleSpaceLeft -= 1
            topo.SwitchSet[switch_seq - 1].rule_num += 1
        for link_seq in route_links:
            topo.LinkSet[link_seq - 1].CapacityLeft -= flow.pf
            topo.LinkSet[link_seq - 1].link_used += flow.pf
            topo.LinkSet[link_seq - 1].link_usage = topo.LinkSet[link_seq - 1].link_used / topo.LinkSet[link_seq -
                                                                                                        1].MAX_CAPACITY

            matrix[flow.seq - 1][link_seq - 1] = 1 # config F-L matrix

    def updateGraph(self, flow, G, topo, route_switches, u = 0.5):
        route_links = topo.findLinksBySwitches(route_switches)
        for link_seq in route_links:
            suppose_pf = topo.LinkSet[link_seq - 1].link_used + flow.pf
            if suppose_pf / topo.LinkSet[link_seq - 1].MAX_CAPACITY > u:
                # Unable a link by setting two end switches to be invalid
                G.LinkSet[link_seq - 1].sw1 = 0; G.LinkSet[link_seq - 1].sw2 = 0

    def chooseBestPath(self, flow, topo, PathSet):
        PathLinkSet = []
        MaxUsageSet = []
        for path in PathSet:
            links = topo.findLinksBySwitches(path)
            PathLinkSet.append(links)

        for num in range(len(PathLinkSet)):
            max_link_usage = 0
            for link_seq in PathLinkSet[num]:
                if (topo.LinkSet[link_seq - 1].link_used + flow.pf) / \
                        topo.LinkSet[link_seq - 1].MAX_CAPACITY > max_link_usage:
                    max_link_usage = (topo.LinkSet[link_seq - 1].link_used + flow.pf) \
                                     / topo.LinkSet[link_seq - 1].MAX_CAPACITY
            MaxUsageSet.append(max_link_usage)

        min_usage = 1
        min_index = -1
        for num in range(len(MaxUsageSet)):
            if min_usage > MaxUsageSet[num]:
                min_usage = MaxUsageSet[num]
                min_index = num

        if min_index is -1:
            return None
        else:
         return PathSet[min_index]

    def printNewFlowInfo(self, NewFlows, flow_number = 10):
        print '\nAfter quick sorting for flows:\n--------------------------------------------------'
        for num in range(flow_number):
            NewFlows[num].showInfo()