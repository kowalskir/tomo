import matplotlib.pyplot as plt

def sinogram(theta, sino):
	plt.imshow(sino, cmap=plt.cm.Greys_r)


def image(image):
	plt.imshow(image, cmap=plt.cm.Greys_r)

def show():
	plt.show()
