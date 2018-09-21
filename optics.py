import numpy as np
# from dataset_generator import ClusteringData
import matplotlib.pyplot as plt
from sys import argv
from random import shuffle
from scipy import spatial
import itertools 
from heapq import heappush, heappop
import time


################################################################################
# Helper Functions
################################################################################


def read_data_file(datafile):
	with open(datafile, 'r') as inputFile:
		lines = inputFile.readlines()
	# shuffle(lines)
	data = np.asarray([[float(i) for i in line.split()] for line in lines])
	print ("Finished reading inputfile")
	return data

# euclidean distance
def distance_from(pnt_1, pnt_2):
	difference = (np.asarray(pnt_1) - np.asarray(pnt_2))**2
	dist = np.sqrt(np.sum(difference))
	return dist

# get points within epsilon distance
def get_neighbours(tree, pnt, epsilon):
	index_neighbours = tree.query_ball_point(x=pnt, r=epsilon, n_jobs = -1)             
	return index_neighbours


def get_core_dist(tree, pnt, index_neighbours, min_pts):
	if len(index_neighbours)<min_pts:
		return np.inf
	else:
		distances, _ = tree.query(x=pnt, k=[min_pts-1], n_jobs = -1) 
		# distances, _ = tree.query(x=pnt, k=min_pts)
		return distances


################################################################################
# PRIORITY QUEUE
################################################################################

class PriorityQueue(object):
	def __init__(self):
		self.pq = []                       # list of entries arranged in a heap
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
		n = self.set_of_points.shape[0]
		self.processed  = np.ones(n)*0
		self.reach_dist, self.core_dist = np.ones(n)*np.inf, np.ones(n)*np.inf
		self.epsilon = epsilon
		self.min_pts = min_pts
		self.ordered_points = []
		self.order_seeds = PriorityQueue()
		self.KDtree = spatial.cKDTree(self.set_of_points)


	def expand_cluster_order(self):
		print ("starting to cluster")
		i = 0 
		data = self.set_of_points
		# for each point P in dataset which is not processed
		for i in range(len(data)):
			print(i)                
			pnt = data[i]
			if self.processed[i]==0:
				# mark P as processed 
				self.processed[i] = 1
				# print(f'Point: {pnt} not processed')
				# set reachability distance to infinity
				self.reach_dist[i] = np.inf
				# get P's neighbours
				index_neighbours = get_neighbours(self.KDtree, pnt, self.epsilon)
				self.core_dist[i] = get_core_dist(self.KDtree, pnt, index_neighbours, self.min_pts)
				# insert P in priority list
				# print(f'core_dist of {pnt}: {core_dist[i]}')
				# write point to outputfile
				self.ordered_points.append(i)
				# if P is a core point
				if not np.isposinf(self.core_dist[i]):
					# print (f'Core point distance is not infinity')
					self.order_seeds = PriorityQueue()
					self.update_order_seeds(index_neighbours, pnt, i)
 					# print(f'length of order_seed: {len(order_seeds)}')
					# if P's neighbours are not processed
					while True:
						try:
							index_of_curr_pnt = self.order_seeds.pop_task()
							curr_pnt = self.set_of_points[index_of_curr_pnt]
						except KeyError:
							# print("Empty PQ . . ")
							break
						# neighbour with smallest reachability distance - N, mark N as processed
						self.processed[index_of_curr_pnt] = 1
						# find N's neighbours
						index_nbors = get_neighbours(self.KDtree, curr_pnt, self.epsilon)
						# set core distance of N
						self.core_dist[index_of_curr_pnt] = get_core_dist(self.KDtree, curr_pnt, index_nbors, self.min_pts)
						self.ordered_points.append(index_of_curr_pnt)
						# if N is a core point
						if not np.isposinf(self.core_dist[index_of_curr_pnt]):
							self.update_order_seeds(index_nbors, curr_pnt, index_of_curr_pnt)
			# else:
			# 	print(f'Point: {pnt} is already processed')
			i += 1


	def update_order_seeds(self, index_neighbours, centre_pnt, idx):
		# print (f'Updating order seeds: {centre_pnt}')
		for i in range(len(index_neighbours)):
			neighbour = self.set_of_points[ index_neighbours[i] ]
			dist = distance_from(neighbour, centre_pnt)
			# dist = self.KDtree.query(x=centre_pnt, k=[i])
			# d, _ = self.KDtree.query(x=centre_pnt, k=i+1)
			# if i+1>1:
			# 	# print(f'centre_pnt: {centre_pnt}')
			# 	# print(f'neighbour: {neighbour}')
			# 	# print(f'd: {d}')
			# 	# print(f'processed: {self.processed[index_neighbours[i]]}')
			# 	dist = d[len(d)-1]
			# else:
			# 	dist = d
			# if neighbor is not processed
			if self.processed[index_neighbours[i]]==0:
				# find new reachability distance
				r_dist = max(self.core_dist[idx], dist)
				if np.isposinf(self.reach_dist[index_neighbours[i]]): # if reachability distance is infinity
					# update reachability distance
					self.reach_dist[index_neighbours[i]] = r_dist
					# Insert point in order_seeds
					print(f'r_dist: {r_dist}')
					self.order_seeds.add_task(index_neighbours[i], priority=r_dist) 
				else: # if object is already in order_seeds, update update reachability distance and heapify
					if r_dist < self.reach_dist[index_neighbours[i]]:
						self.reach_dist[index_neighbours[i]] = r_dist
						print(f'r_dist: {r_dist}')
						# move object further to top of queue
						self.order_seeds.remove_task(index_neighbours[i])
						self.order_seeds.add_task(index_neighbours[i], priority=r_dist)
		

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
		reach_distances = [self.reach_dist[index] for index in self.ordered_points]
		pos = np.arange(1,len(reach_distances)+1)
		fig = plt.figure()
		plt.bar(pos, reach_distances, align='center', width=1.0)
		# plt.plot(pos, reach_distances)
		plt.title(f'Epsilon: {self.epsilon}, MinPts: {self.min_pts}')
		plt.xlabel('Ordered Points')
		plt.ylabel('Reachability Distances')
		plt.show()
						

if __name__ == '__main__': 

	min_pts = int(argv[1])
	epsilon = float(argv[2])
	inputfile = argv[3]

	step0 = time.time()
	optics = OPTICS(inputfile = inputfile, outputfile = outputfile, epsilon = epsilon, min_pts = min_pts)
	optics.cluster()
	# print(optics.reach_dist)
	# print(optics.core_dist)
	step1 = time.time()
	print(f'Total Time taken: {step1-step0}')
	optics.show_reachability_plot()
	# print(optics.ordered_points)



		









