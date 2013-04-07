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
    def randomize_in_params(self):
        pass

    def load_preview_params(self):
        # ширина и высота внешней фигуры
        self.b1 = 11.0
        self.h1 = 10.0
        # основание и высота треугольника
        self.b2 = 6.0
        self.h2 = 8.0
        # координаты треугольника
        self.z0 = 4.0
        self.y0 = 1.0

    def adjust(self):
        pass

    def validate(self):
        pass

    def get_store_str(self):
        pass

    def load_store_str(self, sore_str):
        pass

    def get_in_params(self):
        pass

    def get_out_params(self):
        pass

    def calculate(self):
        # экспортируем переменные экземпляра (исходные данные)
        # к задаче в локальное пространство имен метода
        (h1, b1, h2, b2, z0, y0) = (self.h1, self.b1,
                                    self.h2, self.b2,
                                    self.z0, self.y0)
        # 1. Определим площади простых сечений
        A1 = h1 * b1
        A2 = 0.5 * h2 * b2
        logging.debug("1: A1=%.3f A2=%.3f" % (A1, A2))
        # 2. Определим координаты центра тяжести каждой из простых фигур
        z1 = b1 / 2.0
        z2 = z0 + (b2 / 2.0)
        y1 = h1 / 2.0
        y2 = y0 + (h2 / 3.0)
        logging.debug("2: z1=%.3f z2=%.3f y1=%.3f y2=%.3f" % (z1, z2, y1, y2))
        # 3. Определим координаты центра тяжести фигуры
        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)
        logging.debug("3: zc=%.3f yc=%.3f" % (zc, yc))
        # 4. Определяем моменты инерции простых фигур состовляющих сечение
        Jz1 = (b1 * (h1 ** 3.0)) / 12.0
        Jz2 = (b2 * (h2 ** 3.0)) / 36.0
        Jy1 = ((b1 ** 3.0) * h1) / 12.0
        Jy2 = ((b2 ** 3.0) * h2) / 48.0
        logging.debug("4: Jz1=%.3f Jz2=%.3f Jy1=%.3f Jy2=%.3f" % 
                (Jz1, Jz2, Jy1, Jy2))
        # 5. Найдем растояние между центральными осями всего сечения и 
        # центральными осями простых фигур
        a1 = y1 - yc
        a2 = y2 - yc
        c1 = z1 - zc
        c2 = z2 - zc
        logging.debug("5: a1=%.3f a2=%.3f c1=%.3f c2=%.3f" % 
                (a1, a2, c1, c2))
        # 6. Найдем моменты инерции простых фигур относительно 
        # центральных осей всего сечения
        Jzc1 = Jz1 + ((a1 ** 2) * A1)
        Jzc2 = Jz2 + ((a2 ** 2) * A2)
        Jyc1 = Jy1 + ((c1 ** 2) * A1)
        Jyc2 = Jy2 + ((c2 ** 2) * A2)
        Jzcyc1 = a1 * c1 * A1
        Jzcyc2 = a2 * c2 * A2
        logging.debug("6: Jzc1=%.3f Jzc2=%.3f Jyc1=%.3f Jyc2=%.3f Jzcyc1=%.3f Jzcyc2=%.3f" % 
                (Jzc1, Jzc2, Jyc1, Jyc2, Jzcyc1, Jzcyc2))
        # 7. Найдем центральные моменты инерции всей фигуры
        Jzc = Jzc1 - Jzc2
        Jyc = Jyc1 - Jyc2
        Jzcyc = Jzcyc1 - Jzcyc2
        logging.debug("7: Jz=%.3f Jyc=%.3f Jzcyc=%.3f" % 
                (Jzc, Jyc, Jzcyc))
        # 8. Найдем главные моменты инерции
        Jmax = ((Jzc + Jyc) / 2.0) + 0.5 * (((Jzc - Jyc) ** 2 + 4 * Jzcyc ** 2) ** 0.5)
        Jmin = ((Jzc + Jyc) / 2.0) - 0.5 * (((Jzc - Jyc) ** 2 + 4 * Jzcyc ** 2) ** 0.5)
        logging.debug("8: Jmax=%.3f Jmin=%.3f" % (Jmax, Jmin))
         # 9. Найдем положение главных осей
        tanAmax = Jzcyc / (Jyc - Jmax)
        Amax = degrees(atan(tanAmax))
        tanAmin = Jzcyc / (Jyc - Jmin)
        Amin = degrees(atan(tanAmin))
        (self.alphamax, self.alphamin) = (Amax, Amin)
        logging.debug("9: tanAmax=%.3f Amax=%.3f tanAmin=%.3f Amin=%.3f" % 
                          (tanAmax, Amax, tanAmin, Amin))

    def draw(self, draw, stage):
        return draw

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    engine = ProblemEngine()
    engine.load_preview_params()
    engine.calculate()