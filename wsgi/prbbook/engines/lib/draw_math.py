#!/usr/bin/env python
# -*- coding: utf8 -*-

from math import atan2, pi, cos, sin, radians

def rotate_line(x1, y1, x2, y2, angle):
    angle = radians(angle)
    r_y = x1 + (x2 - x1) * cos(angle) + (y2 - y1) * sin(angle)
    r_x = y1 -(x2 - x1) * sin(angle) + (y2 - y1) * cos(angle)
    return (r_x, r_y)