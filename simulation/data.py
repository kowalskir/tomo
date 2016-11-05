 
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

def get_config_elem(config, section, option):
	if (not section in config) or (not option in config[section]):
		raise Exception("Missing option or section in configuration file")
		sys.exit()
	else:
		return config[section][option]

def open_image(filename):
	return imread(filename, as_grey=True)
