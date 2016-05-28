from ruleplacement.Basic.matrix import FL_Matrix

class Officer:

    def __init__(self, con, Flows, topo):
        self.controller = con
        self.FlowSet = Flows
        self.NetTopo = topo


    def getController(self, controller):
        return controller


    def go(self, matrix_class):
        # Step 1: Initiate a FL-Matrix to all-zero matrix
        self.fl_matrix = matrix_class  # Initiation has been done while instantiation

        # Step 2: Sort flows by weights
        self.FlowsSortedByWeight = self.controller.flowSort(self.FlowSet)

        # Step 3: for all (f,e) in Flows, loop
        for flow in self.FlowsSortedByWeight:
            print '\n\nNow ready to allocate rules for flow %d\n--------------------------------------------------' \
                  % flow.seq
            # Step 4 : sort default path for flows in ascending method
            # 4-1: Compute default path
            self.controller.computeDefaultPath(self.NetTopo, flow)
            # 4-2: Divert from default path
            self.MultiRouteSwitches = self.controller.sortDefaultSwitches(self.NetTopo, flow)
            print 'Multiple routes with switches are listed as: ', self.MultiRouteSwitches

            # Step 5: for every route in multi_routes, execute
            for route_switches in self.MultiRouteSwitches:

                # Step 6: check if the route can be allocated
                if self.controller.canAllocate(flow, route_switches, self.NetTopo):
                    # Step 7: if allocation is allowed, then allocate
                    self.controller.allocate(flow, route_switches, self.NetTopo, self.fl_matrix.matrix)
                    print '\nAllocation for flow %d is successful, and the route composed of switches is: ' % flow.seq, \
                        route_switches
                    print 'the route composed of links is: ', self.NetTopo.findLinksBySwitches(route_switches)
                    # Step 8: start for next flow
                    break
                # else:
                #     print '\nAllocation for flow %d is failed!' %flow.seq

        # Step 9: Get the F-L matrix
        self.fl_matrix.printMatrixInfo("After algorithm executing")
