#!/usr/bin/python3

import numpy as np
from skimage.io import imread
import getopt
import sys

import algorithmes as algo
import data
import graph


def read_options():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:a:b", ["help", "input=", "algorithm=", "benchmark"])
	except getopt.GetoptError as err:
		print_help()
		sys.exit()
	
	input_image, algorithm = ("", "")
	benchmark = False
	
	for o, a in opts:
		if o in ("-h", "--help"):
			print_help()
		elif o in ("-i", "--input"):
			input_image = a
		elif o in ("-a", "--algorithm"):
			algorithm = a
		elif o in ("-b", "--benchmark"):
			benchmark = True
	
	for o in (input_image, algorithm):
		if not o:
			raise Exception("Required argument(s) missing")
			sys.exit()
	
	return (input_image, algorithm, benchmark)


filename, algorithm, b = read_options()
image = data.open_image(filename)

algo.perform_algo(image, algorithm, b)
