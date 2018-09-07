## Clustering

### K-means, DBSCAN, OPTICS

This repository contains the implementation of k-means, DBSCAN and OPTICS from scratch as a part of Homework-2 of the Data Mining Course(COL761) at IIT Delhi.

The dataset is of the following format, where each line corresponds to an n-dimensional point. Each dimension is separated by a space. The number of dimensions and lines can be of any value till 5 and ~1-million points respectively. The feature values are floating point numbers.

3 4 5... 

1 7 8... 

...

- ```sh compile.sh``` clones the following Github repo and compiles  code with respect to all implementations.
- ```sh <rollno>.sh -kmeans <k>``` executes k-means algorithm with k as the numberof clusters and produces the cluster assignment of each data point
- ```sh <rollno>.sh -dbscan -<minPts> <epsilon>``` executes DBSCAN and produces the list of cluster assignment of each data point
- ```sh <rollno>.sh -optics -<minPts> <epsilon>``` executes OPTICS and plots the reachability data using matplotlib

##### Output format for DBSCAN and k-means
Files called dbscan.txt and kmeans.txt rare produced by DBSCAN and k-means espectively. Each file is of the following format:
```#<cluster ID>
<Point1 line no>
<Point 2 line no>
...
#<cluster ID> 
<Point 1 line no>
<Point 2 line no> 
...```
  
The “#” indicates the start of a cluster ID, followed by the line number of all points belonging to the cluster. The line numbers start from 0 and can be treated as an ID of each point. For DBSCAN, all outliers are grouped under the special cluster ID “#outlier”. 
```<cluster ID>``` are assigned integer values only starting from 0.
