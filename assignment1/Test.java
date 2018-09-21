import java.io.*;
import java.util.*;

class Test {
	public static void main(String[] args) throws FileNotFoundException, IOException{
		// $1: <inputfile>	   $2:X	  $3: -apriori/-fptree    $4: <outputfilename>

		// retail.txt 1 -apriori output_apriori
		// retail.txt 1 -fptree output_fptree

		int minSup = Integer.parseInt(args[1]);
		String filepath = args[0];
		String f1 = args[3];
		int args_len = args.length;
		boolean plot = (args_len==5 && args[4].equals("-plot"));

		if (args[2].equals("-fptree")){
			// read database to count total transactions
			BufferedReader reader = new BufferedReader(new FileReader(filepath));
			int lines = 0;
			while (reader.readLine() != null) {
				lines++;
			}
			reader.close();

			int total_transactions = lines;

			long start = System.nanoTime();
			FPTree fptree = new FPTree(minSup);
			fptree.constructTree(filepath, total_transactions);

			for (int i = fptree.flist.size() - 1; i>=0; i--){
				ArrayList<ArrayList<Integer>> list = fptree.buildCPB(fptree.flist.get(i));
				ArrayList<Integer> list1 = new ArrayList<Integer>();
				list1.add(fptree.flist.get(i)); 
				fptree.FPgrowth(list, fptree.flist.get(i), list1, total_transactions);
			}
			long end = System.nanoTime();
			long total = end - start;
		}

		else if (args[2].equals("-apriori")){
		  	Apriori obj = new Apriori(filepath, f1, minSup);
		  	if (plot){
		  		obj.generateFreqItemSets(true);
		  	}
		  	else{
		  		obj.generateFreqItemSets(false);
		  	}
		  	
		}

		else{
			System.out.println("Please specify -apriori or -fptree");
		}
		
	}
}