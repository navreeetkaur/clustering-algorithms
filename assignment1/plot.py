import sys
from matplotlib import pyplot as plt
import subprocess
import timeit

# name of input file
inputfile = sys.argv[1]
# print (inputfile)
support = [1, 5, 10, 25, 50, 90]

compile_command = "javac Test.java"
subprocess.run(compile_command, shell=True)

# command_ap = ["java Test "+ inputfile + " " + str(x) + " -apriori time_ap -plot" for x in support]
# command_fp = ["java Test "+ inputfile + " " + str(x) + " -fptree time_ap -plot" for x in support]

time_ap = []
time_fp = []

for x in support:
	start = timeit.default_timer()
	subprocess.run("java Test "+ inputfile + " " + str(x) + " -apriori output_ap.txt -plot", shell=True)
	end = timeit.default_timer()
	time_ap.append(end-start)

	start1 = timeit.default_timer()
	subprocess.run("java Test "+ inputfile + " " + str(x) + " -fptree output_fp.txt -plot", shell=True)
	end1 = timeit.default_timer()
	time_fp.append(end1-start1)


# print (time_ap)
# print ()
# print (time_fp)


plt.figure()
plt.plot(support, time_ap, label='Apriori')
plt.plot(support, time_fp, label='FP-tree')
plt.title('Performance Comparison')
plt.xlabel('Support threshold')
plt.ylabel('Execution Time(s)')
plt.savefig("Plot.png")