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
    name = u"Задача 7. Два прямоугольника (вертикально)."

    def randomize_in_params(self):
        pass

    def load_preview_params(self):
        h1 = 10.0
        b1 = 8.0
        h2 = 10.0
        b2 = 10.0
        z0 = 3.0

        (self.h1, self.b1, self.h2, 
                  self.b2, self.z0) = (h1, b1, h2, b2, z0)

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
        (h1, b1, h2, b2, z0) = (self.h1, self.b1,
                                self.h2, self.b2,
                                self.z0)
        # 1. Определим площади простых сечений
        A1 = h1 * b1
        A2 = h2 * b2
        logging.debug("1: A1=%.3f A2=%.3f" % (A1, A2))
        # 2. Определим кооридинаты центра тяжести 
        # каждой из простых фигур

    def draw(self, draw, stage):
        return draw

if __name__ == "__main__":
    engine = ProblemEngine()
    engine.load_preview_params()
    engine.calculate()