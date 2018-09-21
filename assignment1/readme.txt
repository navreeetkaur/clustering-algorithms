--------------------------------------------------------COL761 Assignment #1------------------------------------------------------------------


Sanyam Gupta	2015EE30761
Navreet Kaur	2015TT10917
Anil Bera	2015EE10434
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
						      Frequent Itemset Mining
----------------------------------------------------------------------------------------------------------------------------------------------
Apriori Algorithm and FP-tree are used to mine frequent itemsets on this dataset: http://fimi.ua.ac.be/data/retail.dat
Details about the dataset can be found at http://fimi.ua.ac.be/data/retail.pdf
It is assumed that all items are integers.

----------------------------------------------------------------------------------------------------------------------------------------------
							Apriori v/s FP-tree
----------------------------------------------------------------------------------------------------------------------------------------------

The repository contains the following files:


(1) 2015TT10917.sh:

Executing the command: sh 2015TT10917.sh <inputfile> X -apriori <filename> generates a file <filename>.txt containing 
the frequent itemsets at >=X% support threshold with the Apriori algorithm. Similarly, executing the command:sh 2015TT10917.sh 

<inputfile> X -fptree <filename> generates a file<filename>.txt containing the frequent itemsets using FP-tree algorithm. 
X is in percentage and not the absolute count. Our implementations ensure that the transactions are not loaded into main memory. 
However, the frequent patterns and candidate sets are stored in memory. 

<filename>.txt follows the following format: 
	1. Each frequent itemset is on a new line.
	2. The items in each itemset are space separated.


(2) FPTree.java

Node class is the node element used to form fp-tree. It contains:
item: element name - integer in this case
count: count of the item
parent: its parent in fptree
next: pointer to next node in fptree containing same element
chidren: list of its children

FPTree class contains the implementation of the fp-tree and fp-growth for mining frequent itemsets. It contains:

root: root of the tree - null in this case
HeaderTable: Hash map for accessing the nodes of a particular element in the tree
flist: List of all elements in decreasing order of their support
minSup: minimum support for this tree in percentage

Functions:
makeHashmap: takes transactions and makes a hashmap of support counts corresponding to each item in DB
sortHashmap: generates flist from hashmap
RemoveNonFrequent: removes non frequent items from every transaction and arranges the items in each transaction as per flist
insert: given a transaction, inserts a path in the fp tree and also links the node to header table
constructTree: constructs the initial fp-tree from datafile
buildCPB: builds the conditional pattern base given an item and fp tree
generateFPT: generates conditional fp tree given the CPB
FPgrowth: implements the fp-growth algorithm and mines all the frequent item sets
getAllComb: returns all combinations of a list


 
(3) Apriori.java

Variable names and their purposes:
old_item_set : stores last iteration frequent itemsets for candidate generation.
curr_item_set : current candidate item_set.
counter : for storing frequency of candidate item_sets.
is_mergable : checks if two item_set are mergable for generating candidate item_set of greater size.
is_pruned : checks if candidate itemset was pruned.
transaction : Stores the currently accessed transaction set from dataset.
support,support_perc : Stores support threshold and its precentage. 
input_file,output_file : names of input and output files.

Functions
bin_search : returns true if a item_set exists in old_item_set
generate_F1 : generates single size frequent itemsets by itearting in dataset.
generateFreqItemSets : generates iteratively all the frequent itemset.

Apriori.java implements apriori algorithm for mining frequent itemsets. Function generateFreqItemSets takes input file name, 
output file name and support percentage, reads data set from input file and writes all the frequent item sets in output file with given support.


(4) Test.java

Contains the main function. Executes fp-growth or apriori depending on the arguments given. Call to this is made by the bash file



(5) plot.py

generates a plot using matplotlib where the x-axis varies the support threshold and y-axis shows the corresponding running times.
It plots the running times of apriori and fptree at support thresholds of 1%, 5%, 10%, 25%, 50%, and 90%


The performance of Apriori algorithm is compared with FP-tree in the report.

Executing the command: sh 2015TT10917.sh <inputfile> -plot generates a plot using plot.py
The results obtained are explained in the report.

----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------

								EXPLAINATION
----------------------------------------------------------------------------------------------------------------------------------------------

We observe that the running time of FP-growth is lesser than Apriori algorithm. Also, with increase in support threshold, the running 
time of both Apriori and FP-growth decrease. The decrease for FP-growth is less as compared to Apriori. 

In Apriori, the pattern matching operation of comparing candidate sets with transactions becomes expensive due to the increasing size of 
candidate sets. As large number of candidates are generated, they require more memory space. The breadth-first search approach can be 
quite costly in terms of memory as it requires at any moment to keep in the worst case all k and k − 1 itemsets in memory (for k > 1). 

On the other hand, for fp-tree, there is no candidate generation and hence it requires less memory. It removes the need to calculate the 
pairs to be counted (which requires expensive computation). The FP-Growth algorithm stores in memory a compact version of the database. 
A major advantage of fp-growth algorithm is that it only explores the frequent itemsets in the search space, thus avoiding considering 
many itemsets not appearing in the database, i.e.,  infrequent itemsets.

With the increase in number of items, more search space is needed and I/O will also increase for Apriori. Apriori requires more database 
scans as compared to fp-growth; whenever new candidates are generated, DB scan is required. However, FP- tree requires only 2 DB scans. 
Thus, fp-growth is much better computationally. 

Another limitation of Apriori is that the time complexity is O(m^2 * n), where m is the number of distinct items and n is the number 
of transactions. On the other hand, fp-growth algorithm is O(n) which is much faster than Apriori.
