#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
from math import atan, degrees
from json import dumps, loads
from random import randint, choice, uniform
from lib.draw import DesignDraw
from lib.engine import Engine
from lib.draw_math import rotate_line

class ProblemEngine(Engine):
	name = u"Задача 6. Два прямоугольника (горизонтально)."

	def randomize_in_params(self):
		pass

	def load_preview_params(self):
		pass

	def adjust(self):
		pass

	def validate(self):
		pass

	def get_store_str(self, store_str):
		pass

	def get_in_params(self):
		pass

	def get_out_params(self):
		pass

	def calcuate(self):
		pass

	def draw(self, draw, stage):
		return draw

if __name__ == "__main__":
	pass