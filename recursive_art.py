""" Generate a random image based off of randomized functions. """

from random import randint
import random
import math
from PIL import Image


def build_random_lambda_function(min_depth, max_depth):
	""" Builds a random function of depth at least min_depth and depth
		at most max_depth (see assignment writeup for definition of depth
		in this context)

		min_depth: the minimum depth of the random function
		max_depth: the maximum depth of the random function
		returns: the randomly generated function represented as a nested lambda functions
	"""

	l_functions =  [lambda x,y: random.choice([x,y]), 													# Return self
					lambda x: math.sin(math.pi*x),									# sin(x)
					lambda x: math.cos(math.pi*x),									# cos(x)
					lambda x: (math.exp(x)-math.exp(-1))/(math.e-math.exp(-1))-0.5,	# e^x adjusted to be between 
					lambda x,y: x*y,											
					lambda x,y: (x+y)/2,
					lambda x,y: math.sqrt(abs(x*y))				 					# Geometric mean
					]	

	funcIdx = randint(1, len(l_functions)-1)
	random_func = l_functions[funcIdx]

	min_count = 1

	if max_depth == 0:
		return l_functions[0]

	if min_depth == 0:
		min_count = 0

		if randint(0, max_depth) == 0:		# There is a random chance that I'll stop at the current minimum depth
			return l_functions[0]

	if 1 <= funcIdx and funcIdx <= 3:
		# Function has one input
		rec_func = build_random_lambda_function(min_depth-min_count, max_depth-1)
		return lambda a,b: random_func(rec_func(a,b))
	else:
		# Function has two inputs
		rec_func1 = build_random_lambda_function(min_depth-min_count, max_depth-1)
		rec_func2 = build_random_lambda_function(min_depth-min_count, max_depth-1)

		return lambda a,b: random_func(rec_func1(a,b), rec_func2(a,b))
		


def build_random_function(min_depth, max_depth):
	""" Builds a random function of depth at least min_depth and depth
		at most max_depth (see assignment writeup for definition of depth
		in this context)

		min_depth: the minimum depth of the random function
		max_depth: the maximum depth of the random function
		returns: the randomly generated function represented as a nested list
				 (see assignment writeup for details on the representation of
				 these functions)
	"""

	# geomean is the geometric mean. exp is the exponential function adjusted to have a range of [-1,1]
	functions = ['x', 'y', 'sin_pi', 'cos_pi', 'exp', 'prod', 'avg', 'geomean']

	funcIdx = randint(2, len(functions)-1)
	theRandomFunc = functions[funcIdx]

	if 2 <= funcIdx and funcIdx <= 4:
		has_one_input = True
	else:
		has_one_input = False


	if max_depth == 0:
		randomToggle = randint(0,1) # Used to determine whether to return x or y

		return [randomToggle*functions[0] + (not randomToggle)*functions[1]]
	if min_depth == 0:

		if randint(0, max_depth) == 0:	# There is a random chance that I'll stop at the current minimum depth
			randomToggle = randint(0,1) 					# Used to determine whether to return x or y
			return [randomToggle*functions[0] + (not randomToggle)*functions[1]]
		
		if has_one_input: 
			return [theRandomFunc, build_random_function(0, max_depth-1)]
		return [theRandomFunc, build_random_function(0, max_depth-1), \
								build_random_function(0, max_depth-1)]

	# Only make two function calls if the function requires two inputs
	if has_one_input: 
		return [theRandomFunc, build_random_function(min_depth-1, max_depth-1)]
	return [theRandomFunc, build_random_function(min_depth-1, max_depth-1), \
							build_random_function(min_depth-1, max_depth-1)]



def evaluate_random_function(f, x, y):
	""" Evaluate the random function f with inputs x,y
		Representation of the function f is defined in the assignment writeup

		f: the function to evaluate
		x: the value of x to be used to evaluate the function
		y: the value of y to be used to evaluate the function
		returns: the function value

		>>> evaluate_random_function(["x"],-0.5, 0.75)
		-0.5
		>>> evaluate_random_function(["y"],0.1,0.02)
		0.02
	"""

	if f[0] == 'x':
		return x
	elif f[0] == 'y':
		return y
	elif f[0] == 'sin_pi':
		return math.sin(math.pi*evaluate_random_function(f[1], x,y))
	elif f[0] == 'cos_pi':
		return math.cos(math.pi*evaluate_random_function(f[1], x,y))
	elif f[0] == 'exp':
		neg1 = math.exp(-1)
		return (math.exp(evaluate_random_function(f[1], x,y))-neg1)/(math.e-neg1)-0.5
	elif f[0] == 'prod':
		return evaluate_random_function(f[1], x,y)*evaluate_random_function(f[2], x,y)
	elif f[0] == 'avg':
		return 0.5*(evaluate_random_function(f[1], x,y)+evaluate_random_function(f[2], x,y))
	elif f[0] == 'geomean':
		return math.sqrt(abs(evaluate_random_function(f[1], x,y)*evaluate_random_function(f[2], x,y)))


	


def remap_interval(val,
				   input_interval_start,
				   input_interval_end,
				   output_interval_start,
				   output_interval_end):
	""" Given an input value in the interval [input_interval_start,
		input_interval_end], return an output value scaled to fall within
		the output interval [output_interval_start, output_interval_end].

		val: the value to remap
		input_interval_start: the start of the interval that contains all
							  possible values for val
		input_interval_end: the end of the interval that contains all possible
							values for val
		output_interval_start: the start of the interval that contains all
							   possible output values
		output_inteval_end: the end of the interval that contains all possible
							output values
		returns: the value remapped from the input to the output interval

		>>> remap_interval(0.5, 0, 1, 0, 10)
		5.0
		>>> remap_interval(5, 4, 6, 0, 2)
		1.0
		>>> remap_interval(5, 4, 6, 1, 2)
		1.5
	"""
	input_interval_size = float(abs(input_interval_end - input_interval_start))
	output_interval_size = float(abs(output_interval_end - output_interval_start))

	# Normalize val to the 0-1 range  
	normVal = (val - input_interval_start)/input_interval_size

	# Expand it into the desired range
	return normVal*output_interval_size + output_interval_start 
	


def color_map(val):
	""" Maps input value between -1 and 1 to an integer 0-255, suitable for
		use as an RGB color code.

		val: value to remap, must be a float in the interval [-1, 1]
		returns: integer in the interval [0,255]

		>>> color_map(-1.0)
		0
		>>> color_map(1.0)
		255
		>>> color_map(0.0)
		127
		>>> color_map(0.5)
		191
	"""
	# NOTE: This relies on remap_interval, which you must provide
	color_code = remap_interval(val, -1, 1, 0, 255)
	return int(color_code)


def test_image(filename, x_size=350, y_size=350):
	""" Generate test image with random pixels and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	# Create image and loop over all pixels
	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	for i in range(x_size):
		for j in range(y_size):
			x = remap_interval(i, 0, x_size, -1, 1)
			y = remap_interval(j, 0, y_size, -1, 1)
			pixels[i, j] = (random.randint(0, 255),  # Red channel
							random.randint(0, 255),  # Green channel
							random.randint(0, 255))  # Blue channel

	im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
	""" Generate computational art and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	# Functions for red, green, and blue channels - where the magic happens!
	red_function = build_random_function(3,5)
	green_function = build_random_function(3,5)
	blue_function = build_random_function(3,5)

	# Create image and loop over all pixels
	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	for i in range(x_size):
		for j in range(y_size):
			x = remap_interval(i, 0, x_size, -1, 1)
			y = remap_interval(j, 0, y_size, -1, 1)
			pixels[i, j] = (
					color_map(evaluate_random_function(red_function, x, y)),
					color_map(evaluate_random_function(green_function, x, y)),
					color_map(evaluate_random_function(blue_function, x, y))
					)

	im.save(filename)

def generate_lambda_art(filename, x_size=350, y_size=350):
	""" Generate computational art with lambda functions and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	# Functions for red, green, and blue channels - where the magic happens!
	red_function = build_random_lambda_function(7,9)
	green_function = build_random_lambda_function(7,9)
	blue_function = build_random_lambda_function(7,9)

	# Create image and loop over all pixels
	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	for i in range(x_size):
		for j in range(y_size):
			x = remap_interval(i, 0, x_size, -1, 1)
			y = remap_interval(j, 0, y_size, -1, 1)
			pixels[i, j] = (
					color_map(red_function(x, y)),
					color_map(green_function(x, y)),
					color_map(blue_function(x, y))
					)

	im.save(filename)


if __name__ == '__main__':
	import doctest
	doctest.testmod()

	# Create some computational art!
	generate_lambda_art("myart.png")

