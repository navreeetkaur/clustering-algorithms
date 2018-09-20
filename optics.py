import numpy as np
# from dataset_generator import ClusteringData
import matplotlib.pyplot as plt
from sys import argv
from random import shuffle
from scipy import spatial
import itertools 
from heapq import heappush, heappop
import time
# from sklearn.cluster import DBSCAN, OPTICS

def read_data_file(datafile):
	with open(datafile, 'r') as inputFile:
		lines = inputFile.readlines()
	# shuffle(lines)
	data = np.asarray([[float(i) for i in line.split()] for line in lines])
	print ("Finished reading inputfile")
	return data


def set_processed(num_points):
	processed = []
	for i in range(num_points):
		processed.append(False)
	return processed


def set_c_r_distances(num_points):
	c_dists = []
	r_dists = []
	for i in range(num_points):
		c_dists.append(np.inf)
		r_dists.append(np.inf)
	return r_dists, c_dists


# euclidean distance
def distance_from(pnt_1, pnt_2):
	difference = (np.asarray(pnt) - np.asarray(pnt_2))**2
	dist = np.sqrt(np.sum(difference))
	return dist

# get points within epsilon distance
def get_neighbours(tree, pnt, epsilon):
	index_neighbours = tree.query_ball_point(x=pnt, r=epsilon)             
	return index_neighbours


def get_core_dist(tree, pnt, index_neighbours, min_pts):
	if len(index_neighbours)<min_pts:
		return np.inf
	else:
		# distances, _ = tree.query(x=pnt, k=[min_pts-1]) 
		distances, _ = tree.query(x=pnt, k=min_pts)
		return distances[min_pts-1]


def print_points(points):
	for point in points:
		print(point)


def form_KDtree(data):
	# if data.shape[1]==1:
	# 	points = zip(data[:,0].ravel())
	# if data.shape[1]==2:
	# 	points = zip(data[:,0].ravel(), data[:,1].ravel())
	# if data.shape[1]==3:
	# 	points = zip(data[:,0].ravel(), data[:,1].ravel(), data[:,2].ravel())
	# if data.shape[1]==4:
	# 	points = zip(data[:,0].ravel(), data[:,1].ravel(), data[:,2].ravel(), data[:,3].ravel())
	# if data.shape[1]==5:
	# 	points = zip(data[:,0].ravel(), data[:,1].ravel(), data[:,2].ravel(), data[:,3].ravel(), data[:,4].ravel())
	tree = spatial.cKDTree(data)
	return tree


################################################################################
# PRIORITY QUEUE
################################################################################

class PriorityQueue(object):
	def __init__(self, data):
		self.pq = data                       # list of entries arranged in a heap
		self.entry_finder = {}               # mapping of tasks to entries
		self.REMOVED = '<removed-task>'      # placeholder for a removed task
		self.counter = itertools.count()     # unique sequence count

	def add_task(self,task, priority=0):
	    'Add a new task or update the priority of an existing task'
	    if task in self.entry_finder:
	        self.remove_task(task)
	    count = next(self.counter)
	    entry = [priority, count, task]
	    self.entry_finder[task] = entry
	    heappush(self.pq, entry)

	def remove_task(self,task):
	    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
	    entry = self.entry_finder.pop(task)
	    entry[-1] = self.REMOVED

	def pop_task(self):
	    'Remove and return the lowest priority task. Raise KeyError if empty.'
	    while self.pq:
	        priority, count, task = heappop(self.pq)
	        if task is not self.REMOVED:
	            del self.entry_finder[task]
	            return task
	    raise KeyError('pop from an empty priority queue')


################################################################################
# OPTICS
################################################################################

class OPTICS(object):

	def __init__(self, inputfile, outputfile = 'out.txt', epsilon = np.inf, min_pts = 3):
		self.set_of_points = read_data_file(inputfile) #list of datapoints(Points)
		n = len(self.set_of_points)
		self.processed = set_processed(n)
		self.reach_dist, self.core_dist = set_c_r_distances(n)
		self.epsilon = epsilon
		self.min_pts = min_pts
		self.outputfile = outputfile # for each point: point, core distance, reachability distance in 3 lines
		self.ordered_points = []
		self.order_seeds = PriorityQueue([])
		self.KDtree = form_KDtree(self.set_of_points)


	def expand_cluster_order(self):
		print ("starting to cluster")
		with open(self.outputfile, 'a') as output:
			i = 0 
			data = self.set_of_points
			# for each point P in dataset which is not processed
			for i in range(len(data)):
				print(i)                
				pnt = data[i]
				if not self.processed[i]:
					# mark P as processed 
					self.processed[i] = True
					# print(f'Point: {pnt} not processed')
					# set reachability distance to infinity
					self.reach_dist[i] = np.inf
					# get P's neighbours
					index_neighbours = get_neighbours(self.KDtree, pnt, self.epsilon)
					self.core_dist[i] = get_core_dist(self.KDtree, pnt, index_neighbours, self.min_pts)
					# insert P in priority list
	# 				print(f'core_dist of {pnt}: {core_dist[i]}')
					# write point to outputfile
					# str_point = str(pnt).replace(",", "")
					# str_point = str_point.replace("]", "")
					# str_point = str_point.replace("[", "")
					# output.write(str_point+'\n')
					# output.write(str(self.core_dist[i])+'\n')
					print(self.reach_dist[i])
					output.write(str(self.reach_dist[i])+'\n')
					# self.ordered_points.append(pnt)
					# if P is a core point
					if not np.isposinf(self.core_dist[i]):
	# 					print (f'Core point distance is not infinity')
						self.order_seeds = PriorityQueue([])
						self.update_order_seeds(index_neighbours, pnt, i)
						# order_seeds = self.order_seeds
	# 					print(f'length of order_seed: {len(order_seeds)}')
						# if P's neighbours are not processed
						# for j in range(len(self.order_seeds)):
						while True:
							try:
								index_of_curr_pnt = self.order_seeds.pop_task()
								curr_pnt = self.set_of_points[index_of_curr_pnt]
							# while self.order_seeds:
								# neighbour with smallest reachability distance - N
								# curr_pnt = np.asarray(self.order_seeds[j])
								# mark N as processed
								self.processed[index_of_curr_pnt] = True
								# find N's neighbours
								index_nbors = get_neighbours(self.KDtree, curr_pnt, self.epsilon)
								# set core distance of N
								self.core_dist[index_of_curr_pnt] = get_core_dist(self.KDtree, curr_pnt, index_nbors, self.min_pts)
								# write to outputfile
								# str_curr_point = str(curr_pnt).replace(",", "")
								# str_curr_point = str_curr_point.replace("]", "")
								# str_curr_point = str_curr_point.replace("[", "")
								# output.write(str(str_curr_point)+'\n')
								# output.write(str(self.core_dist[index_of_curr_pnt])+'\n')
								print(self.reach_dist[index_of_curr_pnt])
								output.write(str(self.reach_dist[index_of_curr_pnt])+'\n')
								# self.ordered_points.append(curr_pnt)
								# if N is a core point
								if not np.isposinf(self.core_dist[index_of_curr_pnt]):
									self.update_order_seeds(index_nbors, curr_pnt, index_of_curr_pnt)
							except:
								print("Empty PQ . . ")
								break
				# else:
				# 	print(f'Point: {pnt} is already processed')
				i += 1
    

	# def key(self,x):
	# 	return x[0]


	def update_order_seeds(self, index_neighbours, centre_pnt, idx):
		# print (f'Updating order seeds: {centre_pnt.data_point}')
		for i in range(len(index_neighbours)):
			neighbour = self.set_of_points[ index_neighbours[i] ]
			# dist = self.KDtree.query(x=centre_pnt, k=[i])
			d, _ = self.KDtree.query(x=centre_pnt, k=i+1)
			if i+1>1:
				# print(f'centre_pnt: {centre_pnt}')
				# print(f'neighbour: {neighbour}')
				# print(f'd: {d}')
				# print(f'processed: {self.processed[index_neighbours[i]]}')
				dist = d[len(d)-1]
			else:
				dist = d
			# if neighbor is not processed
			if not self.processed[index_neighbours[i]]:
				# find new reachability distance
				r_dist = max(self.core_dist[idx], dist)
				if np.isposinf(self.reach_dist[index_neighbours[i]]): # if reachability distance is infinity
					# update reachability distance
					self.reach_dist[index_neighbours[i]] = r_dist
					# Insert point in order_seeds
					# print(f'r_dist: {r_dist}')
					self.order_seeds.add_task(index_neighbours[i], priority=r_dist)
					######### purane vala ############
# 					self.order_seeds.append(self.set_of_points[index_neighbours[i]])
# # 					print(f'APPENDING - - Order seeeeds:  {self.order_seeds}')
# 					self.order_reach_dist.append(r_dist)
# 					# Heapify
# 					qq = list(zip(self.order_reach_dist, self.order_seeds))
# 					qq.sort(key=self.key)
# 					print(f'SORTING -  - Order seeeeds:  {self.order_seeds}') 
				else: # if object is already in order_seeds, update update reachability distance and heapify
					if r_dist < self.reach_dist[index_neighbours[i]]:
						self.reach_dist[index_neighbours[i]] = r_dist
						# print(f'r_dist: {r_dist}')
						# move object further to top of queue
						self.order_seeds.add_task(index_neighbours[i], priority=r_dist)
						# index = [i for i, e in enumerate(self.order_seeds) if e.data_point == neighbour.data_point]
						# index = index[0]
						# # index = self.order_seeds.index(neighbour)
						# self.order_reach_dist[index] = r_dist
						# # Heapify
						# qq = list(zip(self.order_reach_dist, self.order_seeds))
						# qq.sort(key=self.key)
# 						print(f'UPDATING & SORTING - - Order seeeeds:  {self.order_seeds}') 
		

	def cluster(self):
		self.expand_cluster_order()
		# clusters = []
		# seperators = []
		# for index, point in enumerate(self.ordered_points):
		# 	# this_i = i
  #  #          next_i = i + 1
  #  #          this_p = self.ordered[i]
  #  #          this_rd = this_p.rd if this_p.rd else float('infinity')
  #           r_dist = point.reach_dist 
            
  #           # upper limit to separate the clusters
            
  #           if r_dist > cluster_threshold:
  #               separators.append(index)

  #       separators.append(len(self.ordered))

  #       for i in range(len(separators) - 1):
  #           start = separators[i]
  #           end = separators[i + 1]
  #           if end - start >= self.min_cluster_size:
  #               clusters.append(self.ordered_points[start:end])

  #       return clusters


	def show_reachability_plot(self):
		reach_distances = []

		with open('out.txt', 'r') as outfile:
		    lines = outfile.readlines()
		outfile.close()
		for line in lines:
			reach_distances.append(float(line))

		pos = np.arange(1,len(reach_distances)+1)
		fig = plt.figure()
		# plt.bar(pos, reach_distances, align='center', width=1.0)
		plt.plot(pos, reach_distances)
		plt.title(f'Epsilon: {self.epsilon}, MinPts: {self.min_pts}')
		plt.show()


		# reach_distances = []
		# pos = []
		# with open('out.txt', 'r') as outfile:
		#     lines = outfile.readlines()
		# i = 0
		# for line in lines:
		#     # if (i+1)%3==0:
	 #        dist = float(line)
	 #        reach_distances.append(dist)
		#     i += 1 
		# pos = np.arange(1,len(reach_distances)+1)
		# # print(f'Length of ordered_points: {len(self.ordered_points)}')
		# # for i in range(len(self.ordered_points)):
		# # 	pos.append(i)
		# # 	reach_distances.append(self.ordered_points[i].reach_dist)
		# fig = plt.figure()
		# # plt.bar(pos, reach_distances, align='center', width=1.0)
		# plt.plot(pos, reach_distances)
		# plt.title(f'Epsilon: {self.epsilon}, MinPts: {self.min_pts}')
		# plt.show()
						

if __name__ == '__main__': 

	inputfile = argv[1]
	# labelfile = argv[2]
	outputfile = argv[2]
	# number_of_samples = argv[4]
	# number_of_dimensions = argv[5]
	# number_of_clusters = argv[6]
	# cluster_type = argv[7]
	epsilon = float(argv[3])
	min_pts = int(argv[4])

	# inputfile = 'clustering_dataset.txt'
	# labelfile = 'clustering_labels.txt'
	# outputfile = 'out.txt'
	# number_of_samples = 1000
	# number_of_dimensions = 2
	# number_of_clusters = 3
	# cluster_std = 0.2
	# centers = [(-1, -1), (0, 0), (1, 1)]
	# cluster_type = 'blob'
	

	# if argv[1]=='y':
	# 	cluster_type = argv[4]
	# 	data = ClusteringData(centers, cluster_type, inputfile, labelfile, 
	# 					number_of_samples, number_of_dimensions,
	# 					number_of_clusters, cluster_std)
	# 	data.plot()
	step0 = time.time()
	optics = OPTICS(inputfile = inputfile, outputfile = outputfile, epsilon = epsilon, min_pts = min_pts)
	optics.cluster()
	step1 = time.time()
	print(f'Total Time taken: {step1-step0}')
	optics.show_reachability_plot()



		









