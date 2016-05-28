import java.util.ArrayList;
import java.util.Scanner;

// There are a lot of methods here
public class Factory {
	int FlowNumber = 0;
	public ArrayList<Flow> initiateFlow(int node_number) {
		ArrayList<Flow> FlowSet = new ArrayList<Flow>();
		System.out.print("Please input the number of flow you want : ");
		@SuppressWarnings("resource")
		Scanner scanner = new Scanner(System.in);
		int temp = scanner.nextInt();
		if (temp > 0) {
			FlowNumber = temp;
		}
		
		for (int i = 0;i < FlowNumber;i++) {
			Flow f = new Flow();
			f.initiate(i+1, node_number);
			FlowSet.add(f);
		}
		printFlowSet(FlowSet);
		return FlowSet;
	}
	private void printFlowSet(ArrayList<Flow> FlowSet) {
		System.out.println("There are " + FlowNumber + " flows for the test.");
		for (Flow f : FlowSet) {
			System.out.println("Flow " + f.seq + " contains :");
			System.out.println("Flow in : " + f.innode + "; " + "flow out : " + f.outnode);
			System.out.println("Flow weight : " + f.weight);
			System.out.println("Flow package rate : " + f.pf);
		}
		System.out.println("--------------------------------------");
	}

	public void initiateMatrix(int[][] FL_matrix) {
		for(int[] row : FL_matrix) {
			for (int i = 0;i < row.length;i++) {
				row[i] = 0;
			}
		}
		System.out.print("The matrix is initiated as below : \n-----------------------\n");
		printMatrix(FL_matrix);
	}

	public void printMatrix(int[][] FL_matrix) {
//		System.out.print("The matrix is initiated as below : \n-----------------------\n");
		for(int[] row : FL_matrix) {
			for (int i = 0;i < row.length;i++) {
				System.out.print(row[i] + " ");
			}
			System.out.print("\n");
		}
		System.out.println("-----------------------");
	}
	
	public void weightSort(ArrayList<Flow> FlowSet) {
		int low = 0 ,high = FlowSet.size() - 1;
		quickSort(FlowSet, low, high);
		System.out.println("After quick sorting : ");
		printFlowSet(FlowSet);
	}
	public void quickSort(ArrayList<Flow> FlowSet, int low, int high) {
		if (low >= high)
			return;
		int left = low, right = high - 1;
		Flow mid_f = FlowSet.get(high); //choose the last as standard
		while (left < right) { // Loop condition every time
			while (left < right && FlowSet.get(left).weight > mid_f.weight)
				left++;
			while (left < right && FlowSet.get(right).weight < mid_f.weight)
				right--;
			// Swap data
			Flow temp_left = FlowSet.get(left);
			Flow temp_right = FlowSet.get(right);
			FlowSet.remove(left);
			FlowSet.add(left, temp_right);
			FlowSet.remove(right);
			FlowSet.add(right, temp_left);
		}
		if (FlowSet.get(left).weight <= mid_f.weight) {
			Flow temp_left = FlowSet.get(left);
			FlowSet.remove(left);
			FlowSet.add(left, mid_f);
			FlowSet.remove(high);
			FlowSet.add(high, temp_left);
		} else 
			left++;
		quickSort(FlowSet, low, left - 1);
		quickSort(FlowSet, left + 1, high);
		
	}
	public void BFS(Network net, int innode, int [] distance, int [] lastNode) {
		
		boolean [] visited = new boolean[net.SwitchNumber];
		ArrayList<Integer> checkList = new ArrayList<Integer>();
		
		for (int i = 0;i < lastNode.length;i++) 
			lastNode[i] = 0;
		for (int i = 0;i < distance.length;i++) 
			distance[i] = 0;
		
		for (int i = 0;i < visited.length;i++)
			visited[i] = false;
		
		checkList.add(innode);
		while (checkList.size() > 0) { // If not visited, then visit it and find all of its neighbours
			int ini_seq = checkList.get(0);
			visited[ini_seq - 1] = true;checkList.remove(0);
			ArrayList<Integer> neighbours = net.findCorreNodes(ini_seq);
			for(int node_seq : neighbours) {
				if (!visited[node_seq - 1] && lastNode[node_seq - 1] == 0) {
					checkList.add(node_seq);
					lastNode[node_seq - 1] = ini_seq;
				}
			}
		}
		// Set distance [] to be right values
		for (int node_seq = 1;node_seq <= net.SwitchNumber;node_seq++) {
			if (node_seq == innode)
				continue;
			int seq_recur = node_seq;
			while(lastNode[seq_recur - 1] != 0) {
				distance[node_seq - 1]++;
				seq_recur = lastNode[seq_recur - 1];
			}
		}
		
	}
	public boolean includeLinkEndNodes(ArrayList<Link> linkSet, int one_end, int other_end) {
		for (int i = 0;i < linkSet.size();i++) {
			if (linkSet.get(i).switch_seq_one == one_end && linkSet.get(i).switch_seq_other == other_end)
				return true;
			else if (linkSet.get(i).switch_seq_one == other_end && linkSet.get(i).switch_seq_other == one_end)
				return true;
		}
		return false;
	}

}
