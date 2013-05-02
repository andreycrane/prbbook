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
    name = u"Задача 5. Прямоугольник и треугольник (сверху)."
    short_name = __name__
    category = "Геометрические характеристики поперечных сечений"
    description = """
                  Для заданного поперечного сечения определить центр 
                  тяжести, центральные и главные моменты инерции сечения.
                  <br />
                  Порядок расчета:
                  <ol>
                    <li>Найти центр тяжести сечения</li>
                    <li>Найти центральные моменты инерции сечения</li>
                    <li>Найти главные моменты инерции сечения</li>
                    <li>Построить центральные оси сечения</li>
                  </ol>
                  """
    stage_count = 2

    def randomize_in_params(self):
        # генерируем размеры прямоугольника
        self.h1 = float(randint(5, 10)) + choice((0.0, 0.5))
        self.b1 = float(randint(4, 8)) + choice((0.0, 0.5))
        # генерируем размеры треугольника
        self.h2 = float(randint(5, 9)) + choice((0.0, 0.5))
        self.b2 = float(randint(4, 7)) + choice((0.0, 0.5))
        # генерируем координату z0
        self.z0 = float(randint(1, int(self.b1 - 2)))
        self.y0 = self.h1

    def load_preview_params(self):
        h1 = y0 = 9.0
        b1 = 9.0
        h2 =9.0
        b2 = 7.0
        z0 = 6.0

        (self.h1, self.b1, self.h2, 
         self.b2, self.z0, self.y0) = (h1, b1, h2, b2, z0, y0)

    def adjust(self):
        (h1, b1, h2, b2, z0, y0) = (self.h1, self.b1,
                                    self.h2, self.b2,
                                    self.z0, self.y0)
        if z0 < 1.0:
            raise Exception()

        z1 = b1 / 2.0
        z2 = z0 + (b2 / 2.0)
        y1 = h1 / 2.0
        y2 = y0 + (h2 / 3.0)

        if abs(y1 - y2) < 1.0:
            raise Exception()

        A1 = h1 * b1
        A2 = 0.5 * h2 * b2
        zc = (A1 * z1 + A2 * z2) / (A1 + A2)
        yc = (A1 * y1 + A2 * y2) / (A1 + A2)

        if abs(z1 - zc) < 0.5:
            raise Exception()

        if abs(z2 - zc) < 0.5:
            raise Exception()

        if abs(y1 - yc) < 0.5:
            raise Exception()

        if abs(y2 - yc) < 0.5:
            raise Exception()

        if abs(h1 - yc) < 0.5:
            raise Exception()

    def validate(self):
        (h1,b1, h2, b2, z0) = (self.h1, self.b1, 
                               self.h2, self.b2, self.z0)

        if z0 >= b1:
            raise Exception(u"Сдвиг z0 больше ширины прямоугольника")

    def get_store_str(self):
        dump_obj = {
            'b1': self.b1,
            'h1': self.h1,
            'b2': self.b2,
            'h2': self.h2,
            'z0': self.z0
        }
        return dumps(dump_obj)

    def load_store_str(self, store_str):
        loads_obj = loads(store_str)
        self.b1 = float(loads_obj['b1'])
        self.h1 = float(loads_obj['h1'])
        self.b2 = float(loads_obj['b2'])
        self.h2 = float(loads_obj['h2'])
        self.z0 = float(loads_obj['z0'])
        self.y0 = self.h1

    def get_in_params(self):
        params = [
            {'Прямоугольник':
                [
                    ('Ширина b<sub>1</sub>',self.b1, 'b1', '', 'см'),
                    ('Высота h<sub>1</sub>',self.h1, 'h1', '', 'см')
                ]
            },
            {'Треугольник (равнобедренный)':
                [
                    ('Основание b<sub>2</sub>',self.b2, 'b2', '', 'см'),
                    ('Высота h<sub>2</sub>',self.h2, 'h2', '', 'см')
                ]

            },
            {'Координата треугольника':
                [
                    ('z<sub>0</sub>',self.z0, 'z0', '', 'см'),
                ]
            }
        ]
        return params

    def get_out_params(self):
        params = [
            {'Координаты центра тяжести каждой из простых фигур':
                [
                    ('z<sub>1</sub>',self.z1, 'см'),
                    ('z<sub>2</sub>',self.z2, 'см'),
                    ('y<sub>1</sub>',self.y1, 'см'),
                    ('y<sub>2</sub>',self.y2, 'см')
                ]
            },
            {'Координаты центра тежести всей фигуры':
                [
                    ('z<sub>c</sub>',self.zc, 'см'),
                    ('y<sub>c</sub>',self.yc, 'см')
                ]
            },
            {'Центральные моменты инерции всей фигуры':
                [
                    ('J<sub>zc</sub>',self.Jzc, 'см<sup>4</sup>'),
                    ('J<sub>yc</sub>',self.Jyc, 'см<sup>4</sup>'),
                    ('J<sub>zcyc</sub>',self.Jzcyc, 'см<sup>4</sup>')
                ]
            },
            {'Положение главных осей':
                [
                    ('&alpha;<sub>max</sub>', self.alphamax, '&deg;'),
                    ('&alpha;<sub>min</sub>', self.alphamin, '&deg;')
                ]
            }
        ]
        return params

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
            (Xv, Yv) = rotate_line(x + zc, y + yc, x + b1 + 5, y + yc, alphamin)
            draw.LineFillArrow(x + zc, y + yc, Xv, Yv, headlen = 7, headwid = 6)
            draw.Text("V", Xv, Yv)
            logging.debug("Xv=%.3f Yv=%.3f" % (Xv, Yv))
            (Xu, Yu) = rotate_line(x + zc, y + yc, x + b1 + 5, y + yc, alphamax)
            draw.LineFillArrow(x + zc, y + yc, Xu, Yu, headlen = 7, headwid = 6)
            draw.Text("U", Xu, Yu)
        return draw

if __name__ == "__main__":
    logging.basicConfig(level = logging.WARNING)

    engine = ProblemEngine()
    uniq_hash = {}
    all_iters = 0
    for i in xrange(1000):
        while True:
            all_iters += 1
            try:
                engine.randomize_in_params()
                engine.adjust()
                engine.calculate()
            except Exception as e:
                logging.debug(traceback.format_exc())
            else:
                #engine.get_image(stage = 2)
                if uniq_hash.get(engine.get_store_str(), False):
                    continue
                else:
                    uniq_hash[engine.get_store_str()] = engine.get_store_str()
                    logging.warning(u"Сгенерирована задача: %d" % i)
                    break

    logging.warning(u"Количество полученных уникальных: %d" % len(uniq_hash))
    logging.warning(u"Всего было выполнено итераций: %d" % all_iters)

    while True:
        try:
            engine.randomize_in_params()
            engine.adjust()
            engine.calculate()
        except Exception as e:
            logging.debug(traceback.format_exc())
        else:
            engine.get_image(stage = 2).show()
            break