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
        h1 = y0 = 9.0
        b1 = 9.0
        h2 =9.0
        b2 = 7.0
        z0 = 6.0

        (self.h1, self.b1, self.h2, 
         self.b2, self.z0, self.y0) = (h1, b1, h2, b2, z0, y0)

    def adjust(self):
        pass

    def validate(self):
        pass

    def get_store_str(self):
        pass

    def load_store_str(self):
        pass

    def get_in_params(self):
        pass

    def get_out_params(self):
        pass

    def calculate(self):
        (h1, b1, h2, b2, z0, y0) = (self.h1, self.b1, self.h2, 
                                    self.b2, self.z0, self.y0)
        # определим площади простых сечений
        A1 = h1 * b1
        A2 = 0.5 * h2 * b2
        logging.debug("1) A1=%.3f A2=%.3f" % (A1, A2))
        # определим координаты центра тяжести каждой из простых фигур
        z1 = b1 / 2.0
        z2 = z0 + (b2 / 2.0)
        y1 = h1 / 2.0
        y2 = y0 + (h2 / 3.0)
        (self.z1, self.z2, self.y1, self.y2) = (z1, z2, y1, y2)
        logging.debug("2) z1=%.3f z2=%.3f y1=%.3f y2=%.3f" % (z1, z2, y1, y2))
        # определяем координаты центра тяжести фигуры
        zc = (A1 * z1 + A2 * z2) / (A1 + A2)
        yc = (A1 * y1 + A2 * y2) / (A1 + A2)
        (self.zc, self.yc) = (zc, yc)
        logging.debug("3) zc=%.3f yc=%.3f" % (zc, yc))
        # определяем моменты инерции простых фигур состовляющих сечение
        Jz1 = (b1 * (h1 ** 3.0)) / 12.0
        Jz2 = (b2 * (h2 ** 3.0)) / 36.0
        Jy1 = ((b1 ** 3.0) * h1) / 12.0
        Jy2 = ((b2 ** 3.0) * h2) / 48.0
        logging.debug("4) Jz1=%.3f Jz2=%.3f Jy1=%.3f Jy2=%.3f" % 
                (Jz1, Jz2, Jy1, Jy2))
        # Найдем растояние между центральными осями всего сечения и 
        # центральными осями простых фигур
        a1 = y1 - yc
        a2 = y2 - yc
        c1 = z1 - zc
        c2 = z2 - zc
        logging.debug("5) a1=%.3f a2=%.3f c1=%.3f c2=%.3f" % 
                (a1, a2, c1, c2))
        # Найдем моменты инерции простых фигур относительно 
        # центральных осей всего сечения
        Jzc1 = Jz1 + ((a1 ** 2) * A1)
        Jzc2 = Jz2 + ((a2 ** 2) * A2)
        Jyc1 = Jy1 + ((c1 ** 2) * A1)
        Jyc2 = Jy2 + ((c2 ** 2) * A2)
        Jzcyc1 = a1 * c1 * A1
        Jzcyc2 = a2 * c2 * A2
        logging.debug("6) Jzc1=%.3f Jzc2=%.3f Jyc1=%.3f Jyc2=%.3f Jzcyc1=%.3f Jzcyc2=%.3f" % 
                (Jzc1, Jzc2, Jyc1, Jyc2, Jzcyc1, Jzcyc2))
        # Найдем центральные моменты инерции всей фигуры
        Jzc = Jzc1 + Jzc2
        Jyc = Jyc1 + Jyc2
        Jzcyc = Jzcyc1 + Jzcyc2
        (self.Jzc, self.Jyc, self.Jzcyc) = (Jzc, Jyc, Jzcyc)
        logging.debug("7) Jz=%.3f Jyc=%.3f Jzcyc=%.3f" % 
                (Jzc, Jyc, Jzcyc))
        # Найдем главные моменты инерции
        Jmax = ((Jzc + Jyc) / 2.0) + 0.5 * (((Jzc - Jyc) ** 2 + 4 * Jzcyc ** 2) ** 0.5)
        Jmin = ((Jzc + Jyc) / 2.0) - 0.5 * (((Jzc - Jyc) ** 2 + 4 * Jzcyc ** 2) ** 0.5)
        logging.debug("8) Jmax=%.3f Jmin=%.3f" % (Jmax, Jmin))
        # Найдем положение главных осей
        tanAmax = Jzcyc / (Jyc - Jmax)
        Amax = degrees(atan(tanAmax))
        tanAmin = Jzcyc / (Jyc - Jmin)
        Amin = degrees(atan(tanAmin))
        (self.alphamax, self.alphamin) = (Amax, Amin)
        logging.debug("9) tanAmax=%.3f Amax=%.3f tanAmin=%.3f Amin=%.3f" % 
                          (tanAmax, Amax, tanAmin, Amin))

    def draw(self, draw, stage):
        (x, y) = (5, 5)
        (h1, b1, h2, b2, z0, y0) = (self.h1, self.b1, self.h2, 
                                    self.b2, self.z0, self.y0)
        # рисуем внешнюю фигуру
        draw.Rect(x, y, b1, h1)
        # формируем полигон треугольника
        polygon = ((x + z0, y + h1),
                   (x + z0 + (b2 / 2.0), y + h1 + h2),
                   (x + z0 + b2, y + h1))
        # рисуем полигон треугольника
        draw.Polygon(polygon)
        # рисуем подписи размеров прямоугольника
        # ширина
        draw.BottomAlignText("b1", x + (b1 / 2.0), y)
        # высота
        draw.LeftAlignText("h1", x, y + (h1 / 2.0))
        # рисуем высоту треугольника
        draw.Line(x + z0 + b2, y + h1, x + z0 + b2 + 1,  y + h1)
        draw.Line(x + z0 + (b2 / 2.0), y + h1 + h2, x + z0 + b2 + 1, y + h1 + h2)
        draw.Line2FillArrow(x + z0 + b2 + 0.5,  y + h1, x + z0 + b2 + 0.5,  y + h1 + h2)
        draw.RightAlignText("h2", x + z0 + b2 + 0.5,  y + h1 + (h2 / 2.0))
        # рисуем ширину треугольника
        draw.Line(x + z0, y + h1, x + z0, y + h1 - 1)
        draw.Line(x + z0 + b2, y + h1, x + z0 + b2, y + h1 - 1)
        draw.Line2FillArrow(x + z0, y + h1 - 0.5,  x + z0 + b2, y + h1 - 0.5)
        draw.BottomAlignText("b2", x + z0 + (b2 / 2.0), y + h1 - 0.5)
        # рисуем координату z0
        draw.Line(x, y + h1, x, y + h1 + 1)
        draw.Line(x + z0, y + h1, x + z0, y + h1 + 1)
        draw.Line2FillArrow(x, y + h1 + 0.5, x + z0, y + h1 + 0.5)
        draw.TopAlignText("z0", x + (z0 / 2.0), y + h1 + 0.5)
        # рисуем примитивы второго уровня отрисовки
        if stage >= 2:
            # рисуем координаты центра тяжести каждой из простых фигур
            (z1, z2, y1, y2) = (self.z1, self.z2, self.y1, self.y2)
            # рисуем координату прямоугольника
            draw.Dot(x + z1, y + y1)
            # подпись координаты
            draw.Text("C1", x + z1, y + y1)
            # рисуем координату треугольника
            draw.Dot(x + z2, y + y2)
            # подпись координаты
            draw.Text("C2", x +z2, y + y2)
            # рисуем координаты центра тяжести всей фигуры
            (zc, yc) = (self.zc, self.yc)
            # координата всей фигуры
            draw.Dot(x + zc, y + yc)
            # подпись координаты
            draw.Text("C", x + zc, y + yc)
            # рисуем положение главных осей
            (alphamax, alphamin) = (self.alphamax, self.alphamin)
            (Xv, Yv) = rotate_line(x + zc, y + yc, x + b1 + 2, y + yc, alphamin)
            draw.LineFillArrow(x + zc, y + yc, Xv, Yv, headlen = 7, headwid = 6)
            draw.Text("V", Xv, Yv)
            logging.debug("Xv=%.3f Yv=%.3f" % (Xv, Yv))
            (Xu, Yu) = rotate_line(x + zc, y + yc, x + b1 + 2, y + yc, alphamax)
            draw.LineFillArrow(x + zc, y + yc, Xu, Yu, headlen = 7, headwid = 6)
            draw.Text("U", Xu, Yu)
        return draw

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    engine = ProblemEngine()
    engine.load_preview_params()
    engine.calculate()
    engine.get_image(stage = 2).show()