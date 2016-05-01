import java.util.ArrayList;

public class Flow {
	final static float MAX_WEIGHT = 10;
	final static float MAX_PF = 5; // 5Mbps
	int seq = 0;
	float weight = 0;
	int innode = 0, outnode = 0;
	float pf = 0;
	ArrayList<Integer> DefaultPath_Switches = new ArrayList<Integer>();
	ArrayList<Integer> DefaultPath_Links = new ArrayList<Integer>();
	public void initiate(int seq,int node_number) {
		this.seq = seq;
		weight = (float)(Math.random() * MAX_WEIGHT); //Randomize weight to 0.0~10.0
		pf = (float)(Math.random() * MAX_PF); //Randomize pf to 0.0~5.0Mbps
		while (innode == outnode) {
			innode = (int)(Math.random() * node_number + 1);
			outnode = (int)(Math.random() * node_number + 1);
		}
	}
}
