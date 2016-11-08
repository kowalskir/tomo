#!/usr/bin/python3

import sys

import algorithmes as algo
import data
import graph
import misc

from skimage.measure import compare_nrmse


filename, algorithm = misc.read_options(sys.argv[1:])
parameters = data.read_config("parameters.conf")

image = data.open_image(filename)
theta = misc.generate_theta(parameters["scan_options"]["start_angle"], parameters["scan_options"]["end_angle"], parameters["scan_options"]["nb_angles"])

sinogram = misc.create_sinogram(image, theta)

image_rebuild, t = misc.perform_algo(sinogram, theta, algorithm)
rmse = compare_nrmse(image, image_rebuild, "mean")

print("Image rebuild in {}s with an RMSE of : {}\n".format(t, rmse))

graph.image(image_rebuild)
graph.show()


