import csv, numpy, io, sys, configparser
from skimage.io import imread

def export_data(filename, data):
	csvfile = io.open(filename, "w", newline='')
	csvwriter = csv.writer(csvfile)
	csvwriter.writerows(data)

def import_data(filename):
	csvfile = io.open(filename, newline='')
	csvwriter = csv.writer(csvfile)
	csvwriter.writerows(data)
	
def read_config(filename):
	config = configparser.ConfigParser()
	config.read(filename)
	return config

def open_image(filename):
	return imread(filename, as_grey=True)
