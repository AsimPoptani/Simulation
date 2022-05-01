from config import WIDTH, HEIGHT, X_OFF, Y_OFF
from locations import locations

def map_value(x, smn, smx, tmn, tmx):
	"""Map x in the source range, [smn,smx], to the target range, [tmn,tmx]"""
	return tmn + (tmx - tmn) * ((x - smn) / (smx - smn))

def map_x(x):
	"""Maps the given horizontal position in meters into pixels on the display"""
	return map_value(x, 0, locations[-1][0], X_OFF, WIDTH - 2*X_OFF)

def map_y(y):
	"""Maps the given vertical position in meters into pixels on the display"""
	return map_value(y, 0, locations[-1][1], Y_OFF, HEIGHT - 2*Y_OFF)

