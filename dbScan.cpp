#include <bits/stdc++.h>
#include <cassert>
#include <fstream>

using namespace std;


typedef vector<float> pnt;
typedef vector< vector<float> > points;


float dist(pnt a,pnt b)
{
	int dim=a.size();
	float ret=0.0;
	for(int i=0;i<dim;i++)
	{
		float dif=b[i]-a[i];
		ret+=(dif*dif);
	}
	return sqrt(ret);
}

class dbScan
{
	public:
	points p;             // list of points
	int no_of_points;
	int dim;             // dimension of a point
	int* label;          // label[i] can be -1(not defined),0(Noise),x(cluster number,x>=1)
	float eps;
	int minPts;  
	int no_of_clusters;

	dbScan(float eps,int minPts)
	{
		this->eps = eps;
		this->minPts = minPts-1;    
	}

	// Read data points from txt file into this->p;
	void readData(string dataset_file)
	{
		ifstream dataFile;
		dataFile.open(&(dataset_file[0]));
		string line;

		pnt temp_pnt_1;
		stringstream ss;
	    getline (dataFile,line);
	    ss.str(line);
	    
	    float temp_float;
	    while(ss>>temp_float)
	    	temp_pnt_1.push_back(temp_float);
	    p.push_back(temp_pnt_1);
	    
	    this->dim = temp_pnt_1.size();
	    this->no_of_points = 1;

    	while (! dataFile.eof() )
    	{
    		pnt temp_pnt;
    		stringstream ss;
      		getline (dataFile,line);
    		ss.str(line);
    		temp_pnt.resize(this->dim);
    		for(int i=0;i<this->dim;i++)
    			ss>>temp_pnt[i];
    		p.push_back(temp_pnt);
    		this->no_of_points++;
    	}
    	dataFile.close();
	}

	void init()
	{
		label = (int *)malloc(sizeof(int)*this->no_of_points);
		for(int i=0;i<no_of_points;i++)
			label[i]=-1;   // undefined
	}


	// nbrs of xth point
	vector<int> Rangequery(int x)
	{
		vector<int> ret;
		for(int i=0;i<no_of_points;i++)
		{
			if(i==x)continue;
			if(dist(this->p[i],this->p[x])<eps)
			{
				ret.push_back(i);
			}
		}
		return ret;
	}


	void clustering_data()
	{
		int current_cluster = 0;
		
		int *status = (int *)malloc(sizeof(int)*no_of_points);   // status[i]=k means ith point has been added in queue/set for kth clusters.
		for(int i=0;i<no_of_points;i++)
			status[i]=0;
		
		for(int i=0;i<no_of_points;i++)
		{
			if(label[i]!=-1)continue;
			vector<int> nbrs = Rangequery(i);
			if(nbrs.size()<this->minPts)
			{
				label[i]=0;    // label as noise
				continue;
			}

			current_cluster++;
			label[i]=current_cluster;
			status[i]=current_cluster;
			for(int k=0;k<nbrs.size();k++)
			{
				status[nbrs[k]]=current_cluster;
			}
			
			int j=-1;
			while(j+1<nbrs.size())
			{
				j++;
				int crr_p = nbrs[j];
				if(label[crr_p]==0)
				{
					label[crr_p]=current_cluster;continue;
				}
				if(label[crr_p]!=-1)
				{
					continue;
				}
				label[crr_p]=current_cluster;
				vector<int> nbrs2 = Rangequery(crr_p);
				if(nbrs2.size()<this->minPts)continue;
				for(int k=0;k<nbrs2.size();k++)
				{
					if(status[nbrs2[k]]==current_cluster)continue;
					status[nbrs2[k]]=current_cluster;
					nbrs.push_back(nbrs2[k]);
				}
			}
		}
		no_of_clusters = current_cluster;
	}

	void writedata(string dataset_file)
	{
		ofstream dataFile;
		dataFile.open(&(dataset_file[0]));
		vector< vector<int> > list_pnts;
		list_pnts.resize(no_of_clusters+1);
		for(int i=0;i<no_of_points;i++)
			list_pnts[label[i]].push_back(i);
		for(int i=1;i<=no_of_clusters;i++)
		{
			dataFile<<"#"<<i-1<<"\n";
			int ln=list_pnts[i].size();
			for(int j=0;j<ln;j++)
			{
				dataFile<<list_pnts[i][j]<<"\n";
			}
		}
		int no_of_outliers = list_pnts[0].size();
		if(no_of_outliers!=0)
		{
			dataFile<<"#outliers\n";
			for(int j=0;j<no_of_outliers;j++)
				dataFile<<list_pnts[0][j]<<"\n";
		}
		dataFile.close();
	}
};


int main(int argc, char** argv)
{
	//ios_base::sync_with_stdio ( false );
	
	int minPts=atoi(argv[1]);
	float eps=atof(argv[2]);
	string input_filename=argv[3];
	string output_filename="dbscan.txt";
	cout<<minPts<<eps<<input_filename<<endl;
	//cin>>minPts>>eps>>input_filename>>output_filename;
	
	dbScan obj(eps,minPts);
	

	obj.readData(input_filename);
	obj.init();
	obj.clustering_data();
	obj.writedata(output_filename);
}