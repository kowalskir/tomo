import sys
import getopt
import numpy as np
import algorithmes as algo

from skimage.measure import compare_nrmse
from skimage.transform import radon as skiradon

def generate_theta(start, stop, n):
	return np.linspace(float(start), float(stop), float(n), endpoint=False)

def create_sinogram(image, theta):
	#~ theta = np.linspace(0., 180., float(n), endpoint=False, dtype=float)
	return skiradon(image, theta, True)

def read_options(argv):
	try:
		opts, args = getopt.getopt(argv, "hi:a:", ["help", "input=", "algorithm="])
	except getopt.GetoptError as err:
		print(err)
		print_help()
		sys.exit()
	
	input_image, algorithm = "", ""
	
	for o, a in opts:
		if o in ("-h", "--help"):
			print_help()
			sys.exit()
		elif o in ("-i", "--input"):
			input_image = a
		elif o in ("-a", "--algorithm"):
			algorithm = a
	
	for o in input_image, algorithm:
		if not o:
			raise Exception("Required argument(s) missing")
			sys.exit()
	
	return input_image, algorithm

def perform_algo(sinogram, theta, algorithm):
	try:
		rebuild_image, t = getattr(algo, algorithm)(sinogram, theta)
	except Exception as err:
		print(err)
		sys.exit()
	
	return rebuild_image, t
