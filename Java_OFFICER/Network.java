
import java.util.ArrayList;
import java.util.Scanner;

class Switch {
	final static int MAX_MEM_SIZE = 10000;
	int seq = 0;
	int memory = 0;
	public void getRandomMemorySize() {
		memory = (int)(Math.random() * MAX_MEM_SIZE + 1); //Randomize memory to 1~15
	}
}
class Link {
	final static float MAX_LINK_SIZE = 10000f; //20Mbps
	int seq = 0;
	int switch_seq_one = 0; //Two ends of a link
	int switch_seq_other = 0;
	float capacity = 0;
	public void getRandomLinkSize() {
		capacity = (float)(Math.random() * MAX_LINK_SIZE); //Randomize capacity to 0.0~20.0
	}
}
public class Network {
	String key = "auto";
	int SwitchNumber = 0;
	int LinkNumber = 0;
	Controller controller = new Controller();
	Factory factory = new Factory();
	ArrayList<Switch> SwitchSet = new ArrayList<Switch>();
	ArrayList<Link> LinkSet = new ArrayList<Link>();
	public Network() {
		System.out.println("Please initate a network for test...\nInput auto then it will create a network of 10 nodes"
				+ " automatically,\nand input custom then you should interact with the programme to custom a network\n(If you input nothing or" +
				" something else, then a default topo will be given automatically):");
		@SuppressWarnings("resource")
		Scanner scan = new Scanner(System.in);
		String str = scan.nextLine();
		if (str.equals("custom")) {
			key = str;
		}
	}
	public void setTopo() {
		if (key == "auto") {
			SwitchNumber = 8;
			LinkNumber = 9;
			autoCreateTopo();
		} else 
			customizeTopo();
	}
	private void autoCreateTopo() {
		// Mainly written for test
		for (int i = 0;i < SwitchNumber;i++) { // Initiate switches
			Switch sw = new Switch();
			sw.seq = i + 1;
			sw.getRandomMemorySize();
			SwitchSet.add(sw);
		}
		for (int i = 0;i < LinkNumber;i++) { // Initiate links - step1  
			Link link = new Link();
			link.seq = i + 1;
			link.getRandomLinkSize();
			LinkSet.add(link);
		}
		// Initiate links - step2
		LinkSet.get(0).switch_seq_one = 1;LinkSet.get(0).switch_seq_other = 2;
		LinkSet.get(1).switch_seq_one = 2;LinkSet.get(1).switch_seq_other = 3;
		LinkSet.get(2).switch_seq_one = 2;LinkSet.get(2).switch_seq_other = 4;
		LinkSet.get(3).switch_seq_one = 3;LinkSet.get(3).switch_seq_other = 5;
		LinkSet.get(4).switch_seq_one = 4;LinkSet.get(4).switch_seq_other = 6;
		LinkSet.get(5).switch_seq_one = 5;LinkSet.get(5).switch_seq_other = 6;
		LinkSet.get(6).switch_seq_one = 5;LinkSet.get(6).switch_seq_other = 7;
		LinkSet.get(7).switch_seq_one = 7;LinkSet.get(7).switch_seq_other = 8;
		LinkSet.get(8).switch_seq_one = 6;LinkSet.get(8).switch_seq_other = 8;
		
		// Initiate the location of controller
		ArrayList<Integer> controllerNeighbours = new ArrayList<Integer>();
		controllerNeighbours.add(8);
		controller.setNeighbour(controllerNeighbours);
		
		
		printNetwork();
	}

	private void customizeTopo() {
		// Left for the final test
		int type = 2;
		System.out.println("You choose to customize a topo, and there are two types.\nOne needs you type all the element one by one," +
		" and the other just needs you type the number of switches.\nAnd then a stochastic topo can be given by the program.Please input " +
				"1 for input all yourself and 2 for stochastic : ");
		@SuppressWarnings("resource")
		Scanner scan = new Scanner(System.in);
		type = scan.nextInt();
		if (type == 1)
			customizeTopoDetail();
		else {
			customizeTopoStochastic();
			printNetwork();
		}
	}
	private void customizeTopoStochastic() {
		// TODO Auto-generated method stub
		System.out.print("You only have to input how many switches you want(a number between about 5~1000) :");
		@SuppressWarnings("resource")
		Scanner scan = new Scanner(System.in);
		SwitchNumber = scan.nextInt();
		// Set switches and links
		int link_seq = 1;
		for(int i = 0;i < SwitchNumber;i++) {
			Switch sw = new Switch();
			sw.seq = i + 1;
			sw.getRandomMemorySize();
			SwitchSet.add(sw);
			
			if (i >= 1) {
				int neighbour_node_number = (int)(Math.random() * i  + 1);
				for (int j = 0;j < neighbour_node_number;j++) {
					Link link = new Link();
					boolean include_flag = true;
					link.seq = link_seq;
					link.getRandomLinkSize();
					int one_end = 0, other_end = 0;
					while (one_end == other_end || include_flag == true) {
						one_end = sw.seq;
						other_end = (int)(Math.random() * i  + 1);
						if (factory.includeLinkEndNodes(LinkSet, one_end, other_end)) {
							include_flag = true;
						} else
							include_flag = false;
					}
					link.switch_seq_one = one_end;
					link.switch_seq_other = other_end;
					LinkSet.add(link);
					LinkNumber++;link_seq++;
					// Tomorrow you have to check and adjust codes above
				}
			}
		}
		ArrayList<Integer> controllerNeighbours = new ArrayList<Integer>();
		int neighbour_number = (int)(Math.random() * SwitchNumber  + 1);
		for (int i = 0;i < neighbour_number;i++) {
			boolean contain_flag = true;
			while (contain_flag == true) {
				int neighbour_seq = (int)(Math.random() * SwitchNumber  + 1);
				if (controllerNeighbours.contains(neighbour_seq) == false)
					contain_flag = false;
			}
			controllerNeighbours.add(neighbour_number);
		}
		controller.setNeighbour(controllerNeighbours);
	}
	private void customizeTopoDetail() {
		//
		
	}
	private void printNetwork() {
		System.out.println("There are " + SwitchNumber + " switches and " + LinkNumber + " links in the network.");
		for (Switch sw : SwitchSet) {
			System.out.println("Switch " + sw.seq + " contains :");
			System.out.println("Switch memory : " + sw.memory);
		}
		System.out.println("---------------------------------------------------------------------------");
		for (Link link : LinkSet) {
			System.out.println("Link " + link.seq + " contains :");
			System.out.println("End switches : " + link.switch_seq_one + ", " + link.switch_seq_other);
			System.out.println("Link capacity : " + link.capacity + "Mbps");
		}
		System.out.println("---------------------------------------------------------------------------");
	}
	public ArrayList<Integer> findCorreNodes(int ini_seq) {
		ArrayList<Integer> correNodes = new ArrayList<Integer>();
		for (Link link : LinkSet) {
			if (link.switch_seq_one == ini_seq)
				correNodes.add(link.switch_seq_other);
			else if (link.switch_seq_other == ini_seq)
				correNodes.add(link.switch_seq_one);
		}
		return correNodes;
	}
	
	public ArrayList<Integer> getLinksBetweenSwitches(ArrayList<Integer> switches) {
		ArrayList<Integer> links = new ArrayList<Integer>();
		for(int i = 0;i < switches.size() - 1;i++) {
			for (int j = i + 1;j < switches.size();j++) {
				int one = switches.get(i);
				int other = switches.get(j);
				for(Link link : LinkSet) {
					if (link.switch_seq_one == one && link.switch_seq_other == other)
						links.add(link.seq);
					else if (link.switch_seq_other == one && link.switch_seq_one == other)
						links.add(link.seq);
				}
			}
		}
		return links;
	}

}
