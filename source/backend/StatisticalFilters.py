import numpy as np
import config
import logging
import cv2
import os
import utilities
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

# params = {}
def convolve(params):
	image = params["image"]
	filter_funct = params["filter_funct"]
	window_size = params["window_size"]


	m, n = window_size
	u, v = image.shape[:2]

	# Add zero padding
	pad = int((max(m, n) - 1) / 2)
	padded_image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)

	filtered_image = np.zeros((u, v), dtype="uint8")

	# Get global parameters
	g_mean, g_var = estimate_params(image)
	params["g_mean"] = g_mean
	params["g_var"] = g_var

	# Convolve through the image and apply the filter
	for y in np.arange(pad, u + pad):
		for x in np.arange(pad, v + pad):
			window = padded_image[y - pad:y + pad + 1, x - pad:x + pad + 1]
			params["window"] = window

			# Apply the filter and get the pixel value
			k = filter_funct(params)

			# Put the value in the final image
			filtered_image[y - pad, x - pad] = k
	return filtered_image

def mean_arithmetic_filter(params):
	"""
	Creates and returns a mean arithmetic filter
	:param params:
	:return:
	"""
	logging.info(filter)

	window = params["window"]
	return np.sum(window) / (window.shape[0] * window.shape[1])


def mean_geometric_filter(params):
	"""
	Creates and returns a mean geometric filter
	:param params:
	:return:
	"""
	window = params["window"].astype("float64")
	return np.prod(window, dtype="float32") ** (1 / (window.shape[0] * window.shape[1]))


def mean_harmonic_filter(params):
	"""
	Creates and returns a mean harmonic filter
	:param params:
	:return:
	"""
	window = params["window"].astype("float64")

	m_n = window.shape[0] * window.shape[1]
	num = np.ones((window.shape[0], window.shape[1]), dtype="float64")
	inv = np.divide(num, window, out=np.zeros_like(num), where=window != 0)
	den = np.sum(inv)

	return 0 if den == 0 else m_n / den


def mean_contraharmonic_filter(params):
	"""
	Creates and returns a mean contraharmonic filter
	:param params:
	:return:
	"""
	q = params["Q"]
	window = params["window"].astype("float64")

	num = np.sum(np.power(window, q + 1., out=np.zeros_like(window), where=window != 0))
	den = np.sum(np.power(window, q, out=np.zeros_like(window), where=window != 0))
	return 0 if den == 0 else num / den


def order_statistic_median_filter(params):
	"""

	:param params:
	:return:
	"""
	window = params["window"]
	return np.median(window)


def order_statistic_max_filter(params):
	"""

	:param params:
	:return:
	"""
	window = params["window"]
	return np.max(window)


def order_statistic_min_filter(params):
	"""

	:param params:
	:return:
	"""
	window = params["window"]
	return np.min(window)


def order_statistic_midpoint_filter(params):
	"""

	:param params:
	:return:
	"""
	window = params["window"]
	return (int(np.max(window)) + int(np.min(window))) / 2.0


def order_statistic_alpha_trimmed_filter(params):
	"""

	:param params:
	:return:
	"""
	window = params["window"]
	d = params["d"]

	sorted_window = np.sort(window.flatten())
	if d > len(sorted_window):
		return np.average(window)

	start = int(d / 2)
	end = len(sorted_window) - int(d / 2)
	trimmed_window = sorted_window[start:end]

	return int(np.average(trimmed_window))


def adaptive_filter(params):
	"""

	:param params:
	:return:
	"""

	window = params["window"]
	image = params["input_image"]

	# Get global parameters
	g_mean = params["g_mean"]
	g_var = params["g_var"]

	# Get local parameters
	l_mean = np.average(window)
	l_var = np.var(window)

	m = int(window.shape[0] / 2)
	n = int(window.shape[1] / 2)

	if g_var > l_var:
		l_var = g_var

	val = window[m, n] - (g_var / l_var) * (window[m, n] - l_mean)

	return val


def adaptive_median_filter(params):
	image = params["input_image"]
	m, n = params["window_size"]
	u, v = image.shape[:2]

	c_w = params["min_window_size"][0]
	max_window = params["max_window_size"][0]

	# Add zero padding
	pad = int((max(m, n) - 1) / 2)
	#     print(pad)
	padded_image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)

	filtered_image = np.zeros((u, v), dtype="uint8")

	# Convolve through the image and apply the filter
	for y in np.arange(pad, u + pad):
		for x in np.arange(pad, v + pad):

			k = image[y - pad, x - pad]

			# Create the first window of size 3x3
			m, n = params["min_window_size"]
			wpad = int((max(m, n) - 1) / 2)
			window = padded_image[y - (wpad):y + (wpad) + 1, x - (wpad):x + (wpad) + 1]
			params["window"] = window

			# Apply the filter, incresing the window size until conditions are met
			#             k = filter_funct(params)
			while c_w <= max_window:
				zmin = int(np.min(window))
				zmax = int(np.max(window))
				zmed = int(np.median(window))
				zxy = image[y - pad, x - pad]

				a1 = zmed - zmin
				a2 = zmed - zmax
				#                 print(a1)
				#                 print(a2)
				#                 print("-")

				if a1 > 0 and a2 < 0:
					b1 = zxy - zmin
					b2 = zxy - zmax
					if b1 > 0 and b2 < 0:
						k = zxy
						#                         print(k)
						break
					else:
						k = zmed
						#                         print(k)
						break
				else:  # Increase window
					c_w += 1
					m, n = (c_w, c_w)
					wpad = int((max(m, n) - 1) / 2)
					window = padded_image[y - (wpad):y + (wpad) + 1, x - (wpad):x + (wpad) + 1]
					params["window"] = window

				#             print(k)

			# Put the value in the final image
			filtered_image[y - pad, x - pad] = k
			c_w = params["min_window_size"][0]

	return filtered_image
