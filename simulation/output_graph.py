
import matplotlib.pyplot as plt
import csv

csvfile = open("output.csv", "r", newline="")
reader = csv.reader(csvfile, "excel", delimiter=",")

algo_list = ["scikit_par_fbp", "scikit_par_sart"]

p = {}
t = {}
e = {}

for row in reader:
	algo = row[0]
	if not algo in algo_list:
		raise Exception("Algorithm {} not in list".format(algo))
		exit()
	if not algo in p:
		p[algo] = []
		t[algo] = []
		e[algo] = []
	p[algo].append(row[2]) #Projections
	t[algo].append(row[3]) #Time
	e[algo].append(row[4]) #Rmse

#~ f, (ax1, ax2) = plt.subplots(1, 2)

#~ plt.subplot(111)
plt.figure(1)
#~ plt.subplot(111)

for algo in algo_list:
	plt.plot(p[algo], t[algo], label=algo)

plt.xlabel("Nombre de projections")
plt.ylabel("Temps(s)")

plt.axis([5.,180.,0., 1.5])

plt.legend()

plt.figure(2)
#~ plt.subplot(122)

for algo in algo_list:
	plt.plot(p[algo], e[algo], label=algo)

plt.xlabel("Nombre de projections")
plt.ylabel("RMSE")

plt.axis([5.,180.,0., 2])

plt.legend()

plt.show()
