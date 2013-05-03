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
    name = "Задача 4. Прямоугольник с треугольником"
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
        # генерируем размеры внешней фигуры
        # ширина от 8 до 12
        b1 = float(randint(8, 10)) + choice((0.0, 0.5))
        # высота от 9 до 15
        h1 = float(randint(9, 15)) + choice((0.0, 0.5))
        # генерируем размеры треугольника
        # основание от 3 до b1 - 2.0
        b2 = round(uniform(3.0, b1 - 1.0), 2)
        # высота от 4 до h1 - 1.0
        h2 = round(uniform(4.0, h1 - 1.0), 2)
        # генерируем координаты треугольника
        z0 = round(uniform(0.8, b1 - b2 - 0.6), 2)
        y0 = round(uniform(0.8, h1 - h2 - 0.6), 2)

        (self.b1, self.h1, 
         self.b2, self.h2, 
         self.z0, self.y0) = (b1, h1, b2, h2, z0, y0)

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
        (b1, h1, b2, h2, z0, y0) = (self.b1, self.h1, 
                                    self.b2, self.h2, 
                                    self.z0, self.y0)
        z1 = b1 / 2.0
        z2 = z0 + (b2 / 2.0)
        y1 = h1 / 2.0
        y2 = y0 + (h2 / 3.0)

        if y0 < 0.5:
            raise Exception()
        if z0 < 1.0:
            raise Exception()

        if abs(z1 - z2) < 1.0:
            raise Exception()

        if abs(y1 - y2) < 1.0:
            raise Exception()

        A1 = h1 * b1
        A2 = 0.5 * h2 * b2
        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)

        if abs(y1 - yc) < 0.5:
            raise Exception()

        if abs(y2 - yc) < 0.5:
            raise Exception()

        if abs(z1 - zc) < 0.5:
            raise Exception()

        if abs(z2 - zc) < 0.5:
            raise Exception()

    def validate(self):
        # экспортируем переменные экземпляра (исходные данные)
        # к задаче в локальное пространство имен метода
        (h1, b1, h2, b2, z0, y0) = (self.h1, self.b1,
                                    self.h2, self.b2,
                                    self.z0, self.y0)
        if h1 <= (h2 + y0):
            raise Exception(u"Высота треугольника и/или координата y0 заданы некоректно")
        if b1 <= (b2 + z0):
            raise Exception(u"Ширина треугольника и/или координата z0 заданы некоректно")

    def get_store_str(self):
        dump_obj = {
            'b1': self.b1,
            'h1': self.h1,
            'b2': self.b2,
            'h2': self.h2,
            'z0': self.z0,
            'y0': self.y0
        }
        return dumps(dump_obj)

    def load_store_str(self, store_str):
        loads_obj = loads(store_str)
        self.b1 = float(loads_obj['b1'])
        self.h1 = float(loads_obj['h1'])
        self.b2 = float(loads_obj['b2'])
        self.h2 = float(loads_obj['h2'])
        self.z0 = float(loads_obj['z0'])
        self.y0 = float(loads_obj['y0'])

    def get_in_params(self):
        params = [
            {'Внешняя фигура':
                [
                    ('Ширина b<sub>1</sub>',self.b1, 'b1', '', 'см'),
                    ('Высота h<sub>1</sub>',self.h1, 'h1', '', 'см')
                ]
            },
            {'Треугольник (равнобедренный)':
                [
                    ('Ширина b<sub>2</sub>',self.b2, 'b2', '', 'см'),
                    ('Высота h<sub>2</sub>',self.h2, 'h2', '', 'см')
                ]

            },
            {'Координата треугольника':
                [
                    ('z<sub>0</sub>',self.z0, 'z0', '', 'см'),
                    ('y<sub>0</sub>', self.y0, 'y0', '', 'см')
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
            {'Координаты центра тежести фигуры':
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
        (self.z1, self.z2, self.y1, self.y2) = (z1, z2, y1, y2)
        logging.debug("2: z1=%.3f z2=%.3f y1=%.3f y2=%.3f" % (z1, z2, y1, y2))
        # 3. Определим координаты центра тяжести фигуры
        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)
        (self.zc, self.yc) = (zc, yc)
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
        (self.Jzc, self.Jyc, self.Jzcyc) = (Jzc, Jyc, Jzcyc)
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
        (x, y) = (5, 5)
        (b1, h1, b2, h2, z0, y0) = (self.b1,
                                    self.h1,
                                    self.b2,
                                    self.h2,
                                    self.z0,
                                    self.y0)

        # рисуем внешнюю фигуру
        draw.Rect(x, y, b1, h1)
        # формируем координаты полигона треугольника
        polygon = ((x + z0, y + y0),
                   (x + z0 + (b2 / 2.0), y + y0 + h2),
                   (x + z0 + b2, y + y0))
        # рисуем полигон треугольника
        draw.Polygon(polygon)
        # рисуем высоту треугольника
        draw.Line(x, y + y0, x - 1.5, y + y0)
        draw.Line(x, y + y0 + h2, x - 1.5, y + y0 + h2)
        draw.Line2FillArrow(x - 1.2, y + y0, x - 1.2, y + y0 + h2)
        # рисуем подпись высоты треугольника
        draw.LeftAlignText("h2", x - 1.2, y + y0 + (h2 / 2.0))
        # рисуем подпись ширина треугольника
        draw.BottomAlignText("b2", x + z0 + (b2 / 2.0), y + y0)
        # рисуем подписи внешней фигуры
        draw.BottomAlignText("b1", x + (b1 / 2.0), y)
        draw.LeftAlignText("h1", x, y + (h1 / 2.0))
        # рисуем стрелки координат треугольника
        draw.Line2FillArrow(x, y + y0, x + z0, y + y0)
        draw.Line2FillArrow(x + z0, y, x + z0, y + y0)
        # рисуем подписи над стрелками
        draw.TopAlignText("z0", x + (z0 / 2.0), y + y0)
        draw.RightAlignText("y0", x + z0, y + (y0 / 2.0))
        # рисуем примитивы второго уровня отрисовки
        if stage >= 2:
            # рисуем координаты центра тяжести каждой из простых фигур
            (z1, z2, y1, y2) = (self.z1, self.z2, self.y1, self.y2)
            # координата внешней фигуры
            draw.Dot(x + z1, y + y1)
            # подпись координаты
            draw.Text("C1", x + z1, y + y1)
            # рисуем стрелки координаты центра тяжести внешней фигуры
            # Y1
            draw.LineFillArrow(x + z1, y + y1, x + z1, y + h1 + 2)
            # рисуем подпись над стрелкой Y1
            draw.Text("Y1", x + z1, y + h1 + 2)
            # Z1 
            draw.LineFillArrow(x + z1, y + y1, x + b1 + 2,y + y1)
            # рисуем подпись над стрелкой Z1
            draw.Text("Z1", x + b1 + 2,y + y1)
            # координата внешней фигуры
            draw.Dot(x + z2, y + y2)
            # подпись координаты
            draw.Text("C2", x + z2, y + y2)
            # рисуем стрелки координаты центра тяжести выреза
            # Y2
            draw.LineFillArrow(x + z2, y + y2, x + z2, y + h1 + 2)
            # рисуем подпись над стрелкой
            draw.Text("Y2", x + z2, y + h1 + 2)
            # Z2
            draw.LineFillArrow(x + z2, y + y2, x + b1 + 2, y + y2)
            # рисуем подпись над стрелкой
            draw.Text("Z2",  x + b1 + 2, y + y2)
            # рисуем координаты центра тяжести всей фигуры
            (zc, yc) = (self.zc, self.yc)
            # координата всей фигуры
            draw.Dot(x + zc, y + yc)
            # подпись координаты
            draw.Text("C", x + zc, y + yc)
            # рисуем стрелки координаты центра тяжести всей фигуры
            # Yc
            draw.LineFillArrow(x + zc, y + yc, x + zc, y + h1 + 2)
            draw.Text("Yc", x + zc, y + h1 + 2)
            # Zc
            draw.LineFillArrow(x + zc, y + yc, x + b1 + 2, y + yc)
            draw.Text("Zc", x + b1 + 2, y + yc)
            # рисуем положение главных осей
            (alphamax, alphamin) = (self.alphamax, self.alphamin)

            (Xv, Yv) = rotate_line(x + zc, y + yc, x + b1 + 2, y + yc, alphamin)
            draw.LineFillArrow(x + zc, y + yc, Xv, Yv)
            draw.Text("V", Xv, Yv)
            logging.debug("Xv=%.3f Yv=%.3f" % (Xv, Yv))
            (Xu, Yu) = rotate_line(x + zc, y + yc, x + b1 + 2, y + yc, alphamax)
            draw.LineFillArrow(x + zc, y + yc, Xu, Yu)
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