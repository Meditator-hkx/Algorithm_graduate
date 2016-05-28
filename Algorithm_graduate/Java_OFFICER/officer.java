import java.util.ArrayList;

// Main process to execute
public class officer {
	Network net = new Network(); // It's a network we need for test with some methods in itself
	Controller controller = net.controller; // Main algorithms are all encapsulated in controller
	ArrayList<Flow> FlowSet = new ArrayList<Flow>(); // Flows we need for test
	Factory factory = new Factory(); // Auxiliary methods are inside a factory
	
	public static void main(String[] args) {
		officer of = new officer();
		of.go();  // All test passes!Get ready for your own version and Python-Mininet Version
	}
	public void go() { //Main execution method
		net.setTopo(); // Initiate a network
		FlowSet = factory.initiateFlow(net.SwitchNumber); // Get n flows for test
		
		// Step 1 : Initiate a |F|-by-|L| matrix
		int [][] FL_matrix = new int[FlowSet.size()][net.LinkNumber];
		factory.initiateMatrix(FL_matrix);
		
		// Step 2 : Sort Flow in descending order by weight
		factory.weightSort(FlowSet); // It's quick sort and test passes
		
		// Step 3 : For all (f,e) in M, Loop :
		for (Flow flow : FlowSet) {
			// Step 4 : sort default path for flow in ascending method
	          // 4-1:Compute default path
			controller.computeDefaultPath(net, flow); // It's okay!
			  // 4-2:divert from the default path
			ArrayList<Object> multi_routes = controller.sortDefaultSwitches(net,flow);
			
			// Step 5 : for every route in multi_routes, execute
			for (int i = 0;i < multi_routes.size();i++) {
				@SuppressWarnings("unchecked")
				ArrayList<Integer> route_switch = (ArrayList<Integer>) multi_routes.get(i);
				System.out.println("I want to check what does route_switch looks like :" + route_switch);
				
				// Step 6 : check if the route can be allocated
				if (controller.canAllocate(flow, route_switch, net)) { 
					
					// Step 7 : if it's possible, then just allocate
					controller.allocate(FL_matrix, flow, route_switch, net);
					
					break; // Step 8 : start for next flow
				}
			}
		}
	}
}
