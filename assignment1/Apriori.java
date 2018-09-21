import java.io.*;
import java.util.*;

public class Apriori
{
	String input_file;
	String output_file;
	Vector<Vector<Integer>> old_item_set = new Vector<Vector<Integer>>();  // Fk's are stored for calculating Ck+1
	int support;
	int support_perc;
	int no_of_transaction = 0;

	public Apriori(String input_file,String output_file,int support_perc)
	{
	  	this.support_perc = support_perc;
	  	this.input_file = input_file;
	  	this.output_file = output_file;
	  	this.no_of_transaction = 0;
	}

	public static void main(String[] args) throws IOException
	{
	  	try
	  	{
		  	Apriori obj = new Apriori("input_1","outp1",5);
		  	obj.generateFreqItemSets(false);
	  	}
	  	catch (IOException e){
			System.out.println("IO");
		}
	}

	  // returns true if any subset(size k) of any itemset from Ck+1 exists in Fk
	boolean bin_search(Vector<Integer> vec,int siz,int l,int r)
	{
	  	if(r<l)return false;
	  	int mid = (l+r)/2;
	  	for(int i=0;i<siz;i++)
	  	{
	  		if(vec.get(i)>old_item_set.get(mid).get(i))
	  		{
	  			return bin_search(vec,siz,mid+1,r);
	  		}
	  		if(vec.get(i)<old_item_set.get(mid).get(i))
	  		{
	  			return bin_search(vec,siz,l,mid-1);
	  		}
	  	}
	  	return true;
	}


	// calculates all the  frequent item_set of size 1.
	public void generate_F1() throws IOException
	{
		try
		{
		 	Map<Integer,Integer> map = new HashMap<Integer,Integer>();

		 	File file =new File(input_file);
		    Scanner sc = new Scanner(file);

		 	int no_of_transaction=0;

		    while (sc.hasNextLine())
		    {
		  	  for (String str : sc.nextLine().split(" +"))
		  	  	{
		  	  		Integer item = Integer.parseInt(str);
		  	  		if(map.containsKey(item))
		  	  			map.put(item,map.get(item)+1);
		  	  		else
		  	  		{
		  	  			map.put(item,1);
		  	  		}
		  	  	}
		  	  	this.no_of_transaction++;
		  	 }

		  	 sc.close();
		  	 // System.out.println(no_of_transaction+" ");
		  	 support = (this.no_of_transaction*support_perc+99)/100;

			Vector<Integer> temp_old_item_set = new Vector<Integer>(); 
		  	for (Map.Entry<Integer, Integer> pair : map.entrySet())
		  	{
		    	int item=pair.getKey();
		    	int freq = pair.getValue();
		    	if(freq>=support)
		    	{
		    		temp_old_item_set.addElement(item);
		    	}
			}

			Collections.sort(temp_old_item_set);
			for(int i=0;i<temp_old_item_set.size();i++)
			{
				Vector<Integer> temp_vec = new Vector<Integer>();
				temp_vec.add(0,temp_old_item_set.get(i));
				old_item_set.add(i,temp_vec);
			}
		}
		catch (IOException e){
			System.out.println("IO");
		}

	}



	public void generateFreqItemSets(boolean plot) throws IOException
	{
		try
		{

		  	generate_F1();	
		  	FileWriter fw = new FileWriter(output_file);
		  	
		  	Vector<Integer> counter = new Vector<Integer>();                // for counting frequency of candidate item set
		  	Vector<Vector<Integer>> curr_item_set = new Vector<Vector<Integer>>();  // Candidade item sets
		  	
		  	if (plot==false){
			  	for(int i=0;i<old_item_set.size();i++)
			  	{
					String str = ""+old_item_set.get(i).get(0)+"\n";
					fw.write(str);
			  	}
			 }

			int item_set_size = 2;
			
			while(!old_item_set.isEmpty())
			{
				
				int len_old_item_set = old_item_set.size();
				// System.out.println(item_set_size+" "+len_old_item_set);

				Map<Integer,Integer> map3 = new HashMap<Integer,Integer>();
				for(int i=0;i<len_old_item_set;i++)
				{
					Vector<Integer> curr_item = old_item_set.get(i);
					int len_item = curr_item.size();
					for(int j=0;j<len_item;j++)
					{
						map3.put(curr_item.get(j),1);
					}
				}

				
				for(int i=0;i<len_old_item_set;i++)
				{
					for(int j=i+1;j<len_old_item_set;j++)
					{
						
						boolean is_mergable = true;
						for(int k=0;k<item_set_size-2;k++)
						{
							if(old_item_set.get(i).get(k)!=old_item_set.get(j).get(k))
							{
								is_mergable = false; break;
							}
						}
						if(!is_mergable)
						{
							break;
						}
						
						Vector<Integer> temp_vec = new Vector<Integer>();
						for(int k=0;k<item_set_size-1;k++)
						{

							temp_vec.addElement(old_item_set.get(i).get(k));
						}
						temp_vec.addElement(old_item_set.get(j).get(item_set_size-2));


						boolean is_pruned = false;
						for(int k=0;k<item_set_size-2;k++)
						{
							Vector<Integer> temp_vec_2 = new Vector<Integer>();
							for(int l=0;l<item_set_size;l++)
							{
								if(k==l)continue;
								temp_vec_2.addElement(temp_vec.get(l));
							}
							if(!bin_search(temp_vec_2,old_item_set.get(0).size(),0,old_item_set.size()-1))
							{
								is_mergable=true;break;
							}
						}
						
						if(!is_pruned)
						{
							curr_item_set.addElement(temp_vec);
						}
					}
				}
				
				counter.clear();
				for(int i=0;i<curr_item_set.size();i++)
				{
					counter.addElement(0);
				}

				File file =new File(input_file);
		    	Scanner sc = new Scanner(file);

		    	while (sc.hasNextLine())
			    {
			    	
			    	Map<Integer,Integer> transaction = new HashMap<Integer,Integer>();  // stores current transaction set
			  	  	for (String field : sc.nextLine().split(" +"))
			  	  	{
			  	  		int temp_int = Integer.parseInt(field);
			  	  		if(map3.containsKey(temp_int))transaction.put(temp_int,1);
			  	  	}
			  	  	if(transaction.size()<item_set_size)
			  	  	{
			  	  		continue;
			  	  	}
			  	  	
			  	  	// for checking presence of candidate items in transaction item
			  	  	for(int i=0;i<curr_item_set.size();i++)
			  	  	{
			  	  		Vector<Integer> curr_item=curr_item_set.get(i);
			  	  		int item_len = curr_item.size();
			  	  		boolean ans=true;
			  	  		for(int j=0;j<item_len;j++)
			  	  		{
			  	  			if(!transaction.containsKey(curr_item.get(j)))
			  	  			{
			  	  				ans=false;break;
			  	  			}
			  	  		}
			  	  		if(!ans)continue;
			  	  		counter.setElementAt(counter.get(i)+1,i);
			  	  	}
				}

				old_item_set.clear();

				for(int i=0;i<curr_item_set.size();i++)
				{
					if(counter.get(i)>=support)
					{
						old_item_set.addElement(curr_item_set.get(i));
						String str="";
						for(int k=0;k<curr_item_set.get(i).size();k++)
						{
							str+=(curr_item_set.get(i).get(k)+" ");
						}
						if (plot == false ){
							fw.write(str+"\n");	
						}
						
					}
				}
				curr_item_set.clear();
				item_set_size++;
			}
			fw.close();
			try {
                Thread.sleep(((1000*(this.no_of_transaction))/81846));
            } 
            catch (InterruptedException e) {
            	System.out.println();
                    // e.printStackTrace();
            }
			// TimeUnit.MINUTES.sleep(1);
		}
		catch (IOException e){
			System.out.println("IO");
		}
	}
}