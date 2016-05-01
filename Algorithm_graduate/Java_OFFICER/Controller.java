import java.util.ArrayList;

public class Controller {
	Factory factory = new Factory();
	ArrayList<Integer> neighbour_switches = new ArrayList<Integer>();
	public void setNeighbour(ArrayList<Integer> list) {
		for (int switch_seq : list) {
			neighbour_switches.add(switch_seq);
		}
	}
	// Compute a default path consisting of switches and links
	public void computeDefaultPath(Network net, Flow flow) {
		// Operate on flow.defaultPathSwitches and flow.defaultPathLinks
		int [] lastNode = new int[net.SwitchNumber];
		int [] distance = new int[net.SwitchNumber];
		factory.BFS(net, flow.innode, distance, lastNode); // distance and lastNode is useful []
		int min_seq = 0, min_dis = 100;
		
		// Find nearest path's switch
		for (int switch_seq : neighbour_switches) {
			if (distance[switch_seq - 1] < min_dis) {
				min_dis = distance[switch_seq - 1];
				min_seq = switch_seq;
			}
		}
		int seq_recur = min_seq;
		flow.DefaultPath_Switches.add(min_seq);
		while (lastNode[seq_recur - 1] != 0) {
			flow.DefaultPath_Switches.add(lastNode[seq_recur - 1]);
			seq_recur = lastNode[seq_recur - 1];
		} // All works well till now
		
		// Find links according to the switches
		flow.DefaultPath_Links = net.getLinksBetweenSwitches(flow.DefaultPath_Switches);
	}
	public ArrayList<Object> sortDefaultSwitches(Network net, Flow flow) {
		ArrayList<Object> multi_routes = new ArrayList<Object>();
		ArrayList<Integer> temp_defaultPath = new ArrayList<Integer>();
		
		for (int ele : flow.DefaultPath_Switches)
			temp_defaultPath.add(ele);
		
		int [] lastNode = new int[net.SwitchNumber];
		int [] distance = new int[net.SwitchNumber];
		factory.BFS(net, flow.outnode, distance, lastNode);
		
		while (temp_defaultPath.size() > 0) {
			int min = 1000, min_seq = 0;
			for(int switch_seq : temp_defaultPath) {
				if (min > distance[switch_seq - 1]) {
					min = distance[switch_seq - 1];
					min_seq = switch_seq;
				}
			}
			ArrayList<Integer> add_route = new ArrayList<Integer>();
			int index_in_defaultPath = flow.DefaultPath_Switches.indexOf(min_seq);
			// Add nodes in default path to a route
			for(int i = flow.DefaultPath_Switches.size() - 1;i >= index_in_defaultPath;i--) { 
				add_route.add(flow.DefaultPath_Switches.get(i));
			}
			int recur_seq = min_seq; // Add nodes in the nearest path towards out node
			while(lastNode[recur_seq - 1] != 0) {
				add_route.add(lastNode[recur_seq - 1]);
				recur_seq = lastNode[recur_seq - 1];
			}
			int index_in_tempDefaultPath = temp_defaultPath.indexOf(min_seq);
			temp_defaultPath.remove(index_in_tempDefaultPath);
			// Add an add_route to multi_routes
			multi_routes.add(add_route);
		}

		
		return multi_routes;
	}
	public boolean canAllocate(Flow flow, ArrayList<Integer> route_switch, Network net) {
		ArrayList<Integer> route_link = net.getLinksBetweenSwitches(route_switch);
		for (int route_switch_seq : route_switch) {
			if (net.SwitchSet.get(route_switch_seq - 1).memory <= 0)
				return false;
		}
		for (int route_link_seq : route_link) {
			if (net.LinkSet.get(route_link_seq - 1).capacity <= flow.pf)
				return false;
		}
		System.out.println("This path : " + " Switches " + route_switch + " and Links " + route_link + " can be allocated!");
		return true; // If all the links and switches can be utilized, then canAllocate() return true
	}
	public void allocate(int[][] fL_matrix, Flow flow, ArrayList<Integer> route_switch, Network net) {
		ArrayList<Integer> route_link = net.getLinksBetweenSwitches(route_switch);
		for (int route_switch_seq : route_switch) {
			net.SwitchSet.get(route_switch_seq - 1).memory--;
		}
		for (int route_link_seq : route_link) {
			net.LinkSet.get(route_link_seq - 1).capacity -= flow.pf;
			fL_matrix[flow.seq - 1][route_link_seq - 1] = 1;
		}
		System.out.println("Allocation of flow " + flow.seq + " is over! Now the FLMatrix is as below :");
		factory.printMatrix(fL_matrix);
	}
}
