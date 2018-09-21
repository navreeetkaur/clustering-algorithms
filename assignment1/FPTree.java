import java.io.*;
import java.util.*;

class Node
{
	int item;
	int count;
	Node parent;
	Node next;
	ArrayList<Node> children;

	public Node()
 	{
 		this.item = -1;
 		this.count = 0;
 		this.parent = null;
 		this.next = null;
 		this.children = new ArrayList<Node>();

 	}

 	public Node(int item, int count)
 	{
 		this.item = item;
 		this.count = count;
 		this.parent = null;
 		this.next = null;
 		this.children = new ArrayList<Node>();

 	}

	public int GetItem()
	{
		return this.item;
	}

	public void SetItem(int x)
	{
		this.item = x;
	}

	public void SetParent(Node parent)
	{
		this.parent = parent;
	}

	public Node GetParent()
	{
		return this.parent;
	}

	public void addChild(Node child)
	{
		this.children.add(child);
	}

	public ArrayList<Node> GetChildren()
	{
		return this.children;
	}

	public int getCount()
	{
		return this.count;
	}

	public void incrementCount()
	{
		this.count++;
	}

	public Node hasChild(int i)
	{
		Iterator<Node> it = this.children.iterator();
		while(it.hasNext()){
			Node curr_node = it.next();
			if (curr_node.GetItem() == i){
				return curr_node;
			}
		}
		return null;
	}

	public void printNode(){
		System.out.print(item);
		System.out.print(":  ");
		System.out.println(count);
	}


}


public class FPTree
{
	Node root;
	HashMap<Integer, ArrayList<Node>> HeaderTable;
	ArrayList<Integer> flist;
	int minSup;

// FP-tree constructor
	public FPTree(int x)
	{
		root = new Node();
		HeaderTable = new HashMap<Integer, ArrayList<Node>>();
		flist = new ArrayList<Integer>();
		minSup = x;
	}

// Insert given transaction into FP-tree as a path
	public void insert(ArrayList<Integer> new_itemset)
 	{	
 		Node pointer = this.root;
 		Node curr_node = this.root;
 		Iterator<Integer> it = new_itemset.iterator();
 		while(it.hasNext()){
 			int curr_item = it.next();
 			Node child = curr_node.hasChild(curr_item);
 			if (child != null){
 				child.incrementCount();
 				curr_node = child;
 			}
 			else{
 				Node next_node = new Node(curr_item, 1);
 				next_node.SetParent(curr_node);
 				// Link next_node to last node of Header Table
 				if (this.HeaderTable.get(curr_item) == null){
 					ArrayList<Node> new_node_list = new ArrayList<Node>();
 					new_node_list.add(next_node);
 					this.HeaderTable.put(curr_item, new_node_list);
 				}
 				else{
 					this.HeaderTable.get(curr_item).add(next_node);
 				}
 				curr_node = next_node;
 			}
 		}
 	}

//	Obtain hashmap for each item to map item to its support
	public HashMap<Integer, Integer> makeHashmap(ArrayList<ArrayList<Integer>> transactions)
	{	
		HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();

		for (int i = 0; i < transactions.size(); i++){
			ArrayList<Integer> temp = transactions.get(i);
			for (int j = 0; j < temp.size(); j++){
				int t = temp.get(j);
				if (map.containsKey(t)) 
				{
	            	int count = map.get(t);
					map.put(t, count + 1);
				} 
				else 
				{
					map.put(t, 1);
				}
			}
		}
		return map;
	}

	public HashMap<Integer, Integer> makeHashmap_online(Scanner s)
	{	
		HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
		while (s.hasNext()) 
		{
			int t = s.nextInt();
		 	if (map.containsKey(t)) 
		 	{
  		       	int count = map.get(t);
		 		map.put(t, count + 1);
		 	} 
		 	else 
		 	{
		 		map.put(t, 1);
		 	}
		 }
		return map;
	}


//	Get hashmap as per descending values of counts of items
	private ArrayList<Integer> sortHashmap(HashMap<Integer, Integer> map, int total)
	{
		Set set = map.keySet(); 
		ArrayList<Integer> list = new ArrayList<Integer>(set);
		Collections.sort(list, new Comparator() 
		{
			public int compare(Object o1, Object o2) {
				return ((Comparable) (map.get(o2))).compareTo(map.get(o1));
			}
		});

		
		// [TODO]: optimise
		ArrayList<Integer> pruned = new ArrayList<Integer>();
		for (int i = 0; i < list.size(); i ++){
			if (map.get(list.get(i)) > (this.minSup*total)/100){
				pruned.add(list.get(i));
			}
		}

		return pruned;

	}


//	Remove non frequent items from each transaction itemset
	private ArrayList<Integer> RemoveNonFrequent(ArrayList<Integer> transaction, HashMap<Integer, Integer> map, int total)
	{
		ArrayList<Integer> list = transaction;
		if(map.size() != 0)
		{
			Collections.sort(list, new Comparator() 
			{
				public int compare(Object o1, Object o2) {
					return ((Comparable) (map.get((Integer)o2))).compareTo(map.get((Integer)o1));
				}
			});
		}

		ArrayList<Integer> pruned = new ArrayList<Integer>();
		for (int i = 0; i < transaction.size(); i ++){
			if (map.get(transaction.get(i)) > (this.minSup*total)/100){
				pruned.add(transaction.get(i));
			}
		}

		return pruned;
	}

	
	public void constructTree(String filepath, int total) throws FileNotFoundException{
		// Find support of all 1-itemsets
		File file = new File(filepath);
		Scanner sc = new Scanner(file);
		HashMap<Integer, Integer> one_itemset_support = makeHashmap_online(sc);
		sc.close();
		// Rearrange transactions in Flist order
		ArrayList<Integer> flist = this.sortHashmap(one_itemset_support, total);
		this.flist = flist;
		// Add each transaction as a path and Link nodes of same item
		Scanner scan_trans = new Scanner(file);
		while(scan_trans.hasNextLine()){
			String trans = scan_trans.nextLine();
			List<String> arrayList = new ArrayList<String>(Arrays.asList(trans.split("\\s")));
			ArrayList<Integer> transaction = new ArrayList<Integer>();
			for(String x:arrayList){
			    transaction.add(Integer.parseInt(x.trim()));
			}

			ArrayList<Integer> pruned_trans = this.RemoveNonFrequent(transaction, one_itemset_support, total);
			this.insert(pruned_trans);
		}
		
	}


// build Conditional Pattern Base for a given item
	public ArrayList<ArrayList<Integer>> buildCPB(int item){
		ArrayList<ArrayList<Integer>> cpb = new ArrayList<ArrayList<Integer>>(); 
		ArrayList<Node> allItems = this.HeaderTable.get(item);

		for (Node temp : allItems)
		{	
			Node temp1 = temp.parent;
			int count = temp.count;
			if(temp1.parent == null) continue;
			ArrayList<Integer> parents = new ArrayList<Integer>();
			while (temp1.parent != null){
				parents.add(temp1.item);
				temp1 = temp1.parent;
			}
			Collections.reverse(parents);
			for (int i = 0; i<count; i++){
				cpb.add(parents);	
			}
		}
		return cpb;
	}



	public FPTree generateFPT(ArrayList<ArrayList<Integer>> transactions, int minSup, int total){
		FPTree conditional_FPT = new FPTree(minSup);
		
		HashMap<Integer, Integer> one_itemset_support = conditional_FPT.makeHashmap(transactions);

		ArrayList<Integer> s = new ArrayList<Integer>(one_itemset_support.keySet());
		
		// Rearrange transactions in Flist order
		ArrayList<Integer> flist = conditional_FPT.sortHashmap(one_itemset_support, total);

		conditional_FPT.flist = flist;
		// Add each transaction as a path and Link nodes of same item
		for (ArrayList<Integer> trans : transactions)
		{
			ArrayList<Integer> pruned_trans = conditional_FPT.RemoveNonFrequent(trans, one_itemset_support, total);
			if (pruned_trans.size() != 0)
			{
				conditional_FPT.insert(pruned_trans);	
			}
			
		}
		return conditional_FPT;
	}

	
	// Returns Conditional Frequent Patterns in FPtree tree 
	public void FPgrowth(ArrayList<ArrayList<Integer>> transactions, int item, ArrayList<Integer> list, int total) throws FileNotFoundException{
		
		for(int i = 0; i < list.size(); i++)
		{
			System.out.print(list.get(i) + " ");
		}
		System.out.println();
		
		
		if (transactions.size() == 0){
			return;
		}

		FPTree curr_tree = this.generateFPT(transactions, this.minSup, total);
	
		// - - - - - - - - - Optimisation - - - - - - - - - 
		// Mining single prefix-path FP-tree
		// genarate all combinations of the items left in the tree ree contains a single prefix path
		// check linearity
		if (curr_tree.flist.size() != 0){
			int last = curr_tree.flist.get(curr_tree.flist.size()-1);
			ArrayList<Node> temp = curr_tree.HeaderTable.get(last);

			if (temp.size() == 1){
				if (transactions.size() < (this.minSup*total)/100){
					return;
				}
				else{
					getAllComb(transactions.get(0));
				}
			}

			// Mining multipath FP-tree
			// recursively find frequent patterns
			
			else if (curr_tree.flist.size() != 0)
			{
				for(int i = curr_tree.flist.size() - 1; i >= 0; i--)
				{
					ArrayList<ArrayList<Integer>> curr_cpb = curr_tree.buildCPB(curr_tree.flist.get(i));
					ArrayList<Integer> new_list = new ArrayList<Integer>(list);
					new_list.add(curr_tree.flist.get(i));
					curr_tree.FPgrowth(curr_cpb, curr_tree.flist.get(i), new_list, total);

				}
			}

			else
			{
				return;
			}
		}
	}

	
	public void getAllComb(ArrayList<Integer> list){
		for (int i = 0; i < list.size(); i++){
			for (int j = i; j < list.size(); j++){
				ArrayList<Integer> temp = new ArrayList<Integer>(list.subList(i, j));
				this.print(temp);
			}
		}
	}

	public void print(ArrayList<Integer> list){
		for (int i = 0; i < list.size(); i++){
			System.out.print(list.get(i) + " ");
		}
	}


// Print FP-tree in DFS manner
	private void traversalPrint(Node node){
		ArrayList<Node> children = node.GetChildren();
		if (children.size()==0){
			node.printNode();
			return; 
		}
		for(Node child : children){
			child.printNode();
		}

	}

	public void printTree(){
		traversalPrint(this.root);
	}



}








