# Creator: rafaelurben
 
import math

# Helper functions

def sin(a):
    return math.sin(math.radians(a))

def cos(a):
    return math.cos(math.radians(a))

def tan(a):
    return math.tan(math.radians(a))

def asin(a):
    return math.asin(math.radians(a))

def acos(a):
    return math.acos(math.radians(a))

def atan(a):
    return math.atan(math.radians(a))

# Utility Functions

def calculate_relative_pos(x, y, angle, distance):
    angle = angle % 360

    x_offset = cos(angle)*distance
    y_offset = sin(angle)*distance

    coords = (x+x_offset, y+y_offset)

    return coords

def is_out_of_map(x, y, width, height, min_distance=0):
    return x-min_distance < 0 or y-min_distance < 0 or x+min_distance > width or y+min_distance > height