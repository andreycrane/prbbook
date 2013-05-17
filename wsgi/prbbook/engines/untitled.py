#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.draw import DesignDraw
from math import atan, degrees
from lib.draw_math import rotate_line
from lib.engine import Engine
from json import dumps, loads
from random import randint, choice, uniform
import logging
import traceback

class ProblemEngine(Engine):
	name = u""
    short_name = __name__
    category = ""
    description = """
                  """
    stage_count = 2

    def randomize_in_params(self):
    	pass

    def adjust(self):
    	pass

    def validate(self):
    	pass

    def get_store_str(self):
    	pass

    def load_store_str(self, store_str):
    	pass

    def get_in_params(self):
    	pass

    def get_out_params(self):
    	pass

    def calculate(self):
    	pass

    def draw(self, draw, stage):
    	return draw

if __name__ == "__main__":
	logging.basicConfig(level = logging.WARNING)

	engine = ProblemEngine()