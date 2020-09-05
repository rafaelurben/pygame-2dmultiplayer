# Creator: https://github.com/rafaelurben

# Imports
 
import math

# Helper functions

sin = lambda a: math.sin(math.radians(a))
cos = lambda a: math.cos(math.radians(a))
tan = lambda a: math.tan(math.radians(a))
asin = lambda v: math.degrees(math.asin(v))
acos = lambda v: math.degrees(math.acos(v))
atan = lambda v: math.degrees(math.atan(v))

ceil = math.ceil
floor = math.floor

# Utility Functions

def calculate_relative_pos(x, y, angle, distance):
    angle = angle % 360

    x_offset = cos(angle)*distance
    y_offset = sin(angle)*distance

    coords = (x+x_offset, y+y_offset)

    return coords

def is_out_of_map(x, y, width, height, min_distance=0):
    return x-min_distance < 0 or y-min_distance < 0 or x+min_distance > width or y+min_distance > height

def coord_distance(x, y, x2, y2):
    return math.sqrt(math.pow(x-x2, 2) + math.pow(y-y2, 2))

def coord_angle(x, y, x2, y2):
    return atan(y-y2/x-x2)
