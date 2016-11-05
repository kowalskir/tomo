
import numpy as np
import math
import sys
import time
import matplotlib.pyplot as plt

import data
import graph

import skimage.transform as ski
import radontea

from skimage.measure import compare_nrmse

def perform_algo(image, algo, bench):
	algo_config = data.read_config("algorithmes.conf")
	if not algo in algo_config:
		raise Exception("Algorithm {} not in config file".format(algo))
		exit()
	
	parameters = data.read_config("parameters.conf")
	
	rmse = -1
	
	if algo_config[algo]["return_type"] == "sinogram":
		theta, sinogram, process_time = globals()[algo](image, algo_config[algo], parameters)
		graph.sinogram(theta, sinogram)
	elif algo_config[algo]["return_type"] == "image":
		rebuild_image, process_time = globals()[algo](image, algo_config[algo], parameters)
		graph.image(rebuild_image)
		rmse = compare_nrmse(image, rebuild_image, "Euclidean")
	else:
		raise Exception("return_type must be sinogram or image")
		exit()
	
	graph.show()
	
	if bench:
		print(parameters)
		print(algo_config[algo])
		print("Algorithm {} performed in : {}s".format(algo, process_time))
		if not rmse == -1:
			print("With an error of : {}\n".format(rmse))
	
	return (process_time, rmse)

def scikit_par_radon(image, config, param):
	start_angle = param["parallel_geometry"]["start_angle"]
	end_angle = param["parallel_geometry"]["end_angle"]
	nb_angles = param["parallel_geometry"]["nb_angles"]
	circle = config["circle"]
	if circle == "yes" : circle = True
	else : circle = False
	
	theta = np.linspace(float(start_angle), float(end_angle), nb_angles, endpoint=False, dtype=float)
	
	t = time.time()
	sinogram = ski.radon(image, theta, circle)
	t = time.time() - t
	
	return theta, sinogram, t

def scikit_par_fbp(image, config, param):
	start_angle = param["parallel_geometry"]["start_angle"]
	end_angle = param["parallel_geometry"]["end_angle"]
	nb_angles = param["parallel_geometry"]["nb_angles"]
	circle = config["circle"]
	if circle == "yes" : circle = True
	else : circle = False
	filter_name = config["filter"]
		
	theta = np.linspace(float(start_angle), float(end_angle), nb_angles, endpoint=False, dtype=float)
	
	#~ theta, sinogram, t = scikit_par_radon(image, config, param)
	
	sinogram = ski.radon(image, theta, circle)
	#~ print(sinogram.shape)
	
	t = time.time()
	rebuild_image = ski.iradon(sinogram, theta, None, filter_name, "linear", circle)
	t = time.time() - t
	
	return rebuild_image, t

def scikit_par_sart(image, config, param):
	start_angle = param["parallel_geometry"]["start_angle"]
	end_angle = param["parallel_geometry"]["end_angle"]
	nb_angles = param["parallel_geometry"]["nb_angles"]
	relax = float(config["relaxation"])
	
	#~ theta, sinogram, t = scikit_par_radon(image, config, param)
	theta = np.linspace(float(start_angle), float(end_angle), nb_angles, endpoint=False, dtype=float)
	
	#~ sinogram = scikit_radon(image, geometry)
	
	#~ sinogram = ski.radon(image, theta, circle=False)
	sinogram = ski.radon(image, theta, circle=True)
	
	t = time.time()
	rebuild_image = ski.iradon_sart(sinogram, theta, relaxation=relax)
	t = time.time() - t
	
	#~ print("{}\n{}".format(image.shape, rebuild_image.shape))
	
	return rebuild_image, t

#~ def radondea_fbp(image, geometry):
	#~ algo_config = io.read_config("algorithmes.conf")["scikit_sart"]
	#~ parameters = io.read_config("parameters.conf")
	
	#~ angle_start = io.get_config_elem(parameters, "parallel_geometry", "start_angle")
	#~ angle_stop = io.get_config_elem(parameters, "parallel_geometry", "end_angle")
	#~ nb_angles = io.get_config_elem(parameters, "parallel_geometry", "nb_angles")
	
	#~ theta = np.linspace(float(angle_start*math.pi/180), float(angle_stop*math.pi/180), nb_angles, endpoint=False, dtype=float)
	
	#~ sinogram = radontea.radon(image, theta)
	
	#~ plt.imshow(sinogram, cmap=plt.cm.Greys_r)
	#~ plt.show()
	
	#~ rebuild_image = radontea.backprojection(sinogram, 
	
