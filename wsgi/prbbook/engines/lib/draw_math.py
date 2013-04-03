#!/usr/bin/env python
# -*- coding: utf8 -*-

from math import atan2, pi, cos, sin, radians

def rotate_line(x0, y0, xs, ys, angle):
    angle = radians(angle)
    r_x = ((xs -x0) * cos(angle)) - ((ys - y0) * sin(angle)) + x0
    r_y = ((xs - x0) * sin(angle)) + ((ys - y0) * cos(angle)) + y0
    return (r_x, r_y)