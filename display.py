from config import WIDTH, HEIGHT, WIDTH_RATIO, HEIGHT_RATIO
from config import MIN_AREA_X, MIN_AREA_Y, MAX_AREA_X, MAX_AREA_Y

def map_value(x, smn, smx, tmn, tmx):
	"""Map x in the source range, [smn,smx], to the target range, [tmn,tmx]"""
	return tmn + (tmx - tmn) * ((x - smn) / (smx - smn))

def x_to_pixels(x):
	"""Maps the given horizontal position in meters into pixels on the display"""
	return map_value(x, MIN_AREA_X, MAX_AREA_X, 0, WIDTH * WIDTH_RATIO)

def y_to_pixels(y):
	"""Maps the given vertical position in meters into pixels on the display"""
	return map_value(y, MIN_AREA_Y, MAX_AREA_Y, 0, HEIGHT * HEIGHT_RATIO)

def pixels_to_x(x):
	"""Maps the given horizontal position in pixels on the display into meters"""
	return map_value(x, 0, WIDTH * WIDTH_RATIO, MIN_AREA_X, MAX_AREA_X)

def pixels_to_y(y):
	"""Maps the given vertical position in pixels on the display into meters"""
	return map_value(y, 0, HEIGHT * HEIGHT_RATIO, MIN_AREA_Y, MAX_AREA_Y)
