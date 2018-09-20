import numpy as np
# from dataset_generator import ClusteringData
import matplotlib.pyplot as plt
from sys import argv
from random import shuffle
# from sklearn.cluster import DBSCAN, OPTICS

################################################################################
# POINT
################################################################################

class Point(object):

	def __init__(self, data_point, reach_dist = float("inf"), core_dist = float("inf"), processed=False):
		self.data_point = data_point
		self.reach_dist = reach_dist
		self.core_dist = core_dist
		self.processed = processed

	def set_core_dist(self, neighbours, distances, min_pts):
		if len(neighbours)>=min_pts:
			distances.sort()
			core_dist = distances[min_pts-1]
			self.core_dist = core_dist
		else:
			self.core_dist = float("inf")

	# euclidean distance
	def distance_from(self, new_point):
		difference = (np.asarray(self.data_point) - np.asarray(new_point.data_point))**2
		dist = np.sqrt(np.sum(difference))
		return dist


################################################################################
# SET OF POINTS
################################################################################


class Set_Points(object):

	def __init__(self, datafile):
		self.points = []
		self.read_data_file(datafile)


	def get_neighbours(self, pnt, epsilon):
		neighbours = []
		distances = []
		for curr_point in self.points:
			dist = pnt.distance_from(curr_point)
			if dist<=epsilon and float(dist)!=0.0:
				neighbours.append(curr_point)
				distances.append(dist)                
		return neighbours, distances

		
	def read_data_file(self, datafile):
		data = []
		with open(datafile, 'r') as inputFile:
			lines = inputFile.readlines()
		shuffle(lines)
		data_points_list = [[float(i) for i in line.split()] for line in lines]
		data = [Point(data_point = data_point) for data_point in data_points_list]
		print ("Finished reading inputfile")
		self.points = data


	def print_points(self):
		for point in self.points:
			print(point.data_point)


################################################################################
# OPTICS
################################################################################

class OPTICS(object):

	def __init__(self, inputfile, outputfile = 'out.txt', epsilon = float("inf"), min_pts = 3):
		self.set_of_points = Set_Points(inputfile) #list of datapoints(Points)
# 		self.set_of_points.print_points()
		self.epsilon = epsilon
		self.min_pts = min_pts
		self.outputfile = outputfile # for each point: point, core distance, reachability distance in 3 lines
		self.ordered_points = []
		self.order_seeds = []
		self.order_reach_dist = []


	def expand_cluster_order(self):
		print ("starting to cluster")
		data = self.set_of_points
		# with open(self.outputfile, 'a') as output:
		i = 0 
		# for each point P in dataset which is not processed
		while len(data.points):
			# print(i)                
			pnt = data.points[0]
			del data.points[0]
			if not pnt.processed:
				# mark P as processed 
				pnt.processed = True
				# print(f'Point: {pnt.data_point} not processed')
				# set reachability distance to infinity
				pnt.reach_dist = float("inf")
				# get P's neighbours
				neighbours, distances = self.set_of_points.get_neighbours(pnt, self.epsilon)
				pnt.set_core_dist(neighbours, distances, self.min_pts)
				# insert P in priority list

# 				print(f'core_dist of {pnt.data_point}: {pnt.core_dist}')
				# write point to outputfile
				# str_point = str(pnt.data_point).replace(",", "")
				# str_point = str_point.replace("]", "")
				# str_point = str_point.replace("[", "")
				# output.write(str(pnt.data_point)+'\n')
				# output.write(str(pnt.core_dist)+'\n')
				# output.write(str(pnt.reach_dist)+'\n')
				self.ordered_points.append(pnt)
				# if P is a core point
				if not np.isposinf(pnt.core_dist):
# 					print (f'Core point distance is not infinity')
					self.order_seeds = []
					self.update_order_seeds(neighbours, distances, pnt)
					# order_seeds = self.order_seeds
# 					print(f'length of order_seed: {len(order_seeds)}')
					# if P's neighbours are not processed
					while self.order_seeds:
						# neighbour with smallest reachability distance - N
						curr_pnt = self.order_seeds[0] 
						del self.order_seeds[0]
						# mark N as processed
						curr_pnt.processed = True
						# find N's neighbours
						nbors, dists = self.set_of_points.get_neighbours(curr_pnt, self.epsilon)
						# set core distance of N
						curr_pnt.set_core_dist(nbors, dists, self.min_pts)
						# str_curr_point = str(curr_pnt.data_point).replace(",", "")
						# str_curr_point = str_curr_point.replace("]", "")
						# str_curr_point = str_curr_point.replace("[", "")
						# output.write(str(curr_pnt.data_point)+'\n')
						# output.write(str(curr_pnt.core_dist)+'\n')
						# output.write(str(curr_pnt.reach_dist)+'\n')
						self.ordered_points.append(curr_pnt)
						# if N is a core point
						if not np.isposinf(curr_pnt.core_dist):
							self.update_order_seeds(nbors, dists, curr_pnt)
			i += 1
    

	def key(self,x):
		return x[0]


	def update_order_seeds(self, neighbours, distances, centre_pnt):
		# print (f'Updating order seeds: {centre_pnt.data_point}')
		for i in range(len(neighbours)):
			neighbour = neighbours[i]
			dist = distances[i]
			# if neighbor is not processed
			if not neighbour.processed:
				# find new reachability distance
				r_dist = max(centre_pnt.core_dist, dist)
				if np.isposinf(neighbour.reach_dist): # if reachability distance is infinity
					# update reachability distance
					neighbour.reach_dist = r_dist
					# Insert in order_seeds
					self.order_seeds.append(neighbour)
# 					print(f'APPENDING - - Order seeeeds:  {self.order_seeds}')
					self.order_reach_dist.append(r_dist)
					# Heapify
					qq = list(zip(self.order_reach_dist, self.order_seeds))
					qq.sort(key=self.key)
# 					order_reach_dist, order_seeds = zip(*sorted(zip(self.order_reach_dist, self.order_seeds)))
# 					self.order_reach_dist, self.order_seeds = list(order_reach_dist), list(order_seeds)
# 					print(f'SORTING -  - Order seeeeds:  {self.order_seeds}') 
				else: # if object is already in order_seeds, update update reachability distance and heapify
					if r_dist < neighbour.reach_dist:
						neighbour.reach_dist = r_dist
						# move object further to top of queue
						index = [i for i, e in enumerate(self.order_seeds) if e.data_point == neighbour.data_point]
						index = index[0]
						# index = self.order_seeds.index(neighbour)
						self.order_reach_dist[index] = r_dist
						# Heapify
						qq = list(zip(self.order_reach_dist, self.order_seeds))
						qq.sort(key=self.key)
# 						order_reach_dist, order_seeds = zip(*sorted(zip(self.order_reach_dist, self.order_seeds)))
# 						self.order_reach_dist, self.order_seeds = list(order_reach_dist), list(order_seeds)
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
		pos = []
		# with open('out.txt', 'r') as outfile:
		#     lines = outfile.readlines()
		# i = 0
		# for line in lines:
		#     if (i+1)%3==0:
		#         dist = float(line)
		#         reach_distances.append(dist)
		#     i += 1 
		print(f'Length of ordered_points: {len(self.ordered_points)}')
		for i in range(len(self.ordered_points)):
			pos.append(i)
			reach_distances.append(self.ordered_points[i].reach_dist)
		# pos = np.arange(1,len(reach_distances)+1)
		fig = plt.figure()
		plt.bar(pos, reach_distances, align='center', width=1.0)
		plt.title(f'Epsilon: {self.epsilon}, MinPts: {self.min_pts}')
		plt.show()
						

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

	optics = OPTICS(inputfile = inputfile, outputfile = outputfile, epsilon = epsilon, min_pts = min_pts)
	optics.cluster()
	optics.show_reachability_plot()



		









