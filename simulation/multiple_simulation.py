#!/usr/bin/python3

import sys
import numpy as np
import csv

import algorithmes
import data

import matplotlib.pyplot as plt
from skimage.measure import compare_nrmse

image = data.open_image(sys.argv[1])

algos = ["scikit_par_fbp", "scikit_par_sart"]
projections = np.arange(5, 181, 5)

t = {}
e = {}

for algo in algos:
	algo_config = data.read_config("algorithmes.conf")
	if not algo in algo_config:
		raise Exception("Algorithm {} not in config file".format(algo))
		exit()
	parameters = data.read_config("parameters.conf")
	
	t[algo] = []
	e[algo] = []
	
	for i in projections:
		parameters["parallel_geometry"]["nb_angles"] = str(i)
		rebuild_image, process_time = getattr(algorithmes, algo)(image, algo_config[algo], parameters)
		rmse = compare_nrmse(image, rebuild_image, "mean")
		t[algo].append(process_time)
		e[algo].append(rmse)

csvfile = open("output2.csv", "a", newline="")
writer = csv.writer(csvfile, "excel", delimiter=",")

for algo in algos:
	for i in np.arange(0, len(projections)):
		writer.writerow([algo, sys.argv[1], str(projections[i]),str(t[algo][i]), str(e[algo][i])])

	#~ plt.plot(projections, t[algo])
	#~ plt.plot(projections, e[algo])

#~ plt.show()

csvfile.close()

	
	#~ if algo_config[algo]["return_type"] == "sinogram":
		#~ theta, sinogram, process_time = globals()[algo](image, algo_config[algo], parameters)
		#~ graph.sinogram(theta, sinogram)
	#~ elif algo_config[algo]["return_type"] == "image":
		#~ rebuild_image, process_time = globals()[algo](image, algo_config[algo], parameters)
		#~ graph.image(rebuild_image)
		#~ rmse = compare_nrmse(image, rebuild_image, "Euclidean")
	#~ else:
		#~ raise Exception("return_type must be sinogram or image")
		#~ exit()
	
	#~ graph.show()
