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
    name = u"Задача 1. Два квадрата"
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

    def __init__(self):
        pass

    # прозводит рандомизацию исходных
    # данных к задаче
    def randomize_in_params(self):
        # генерируем ширину и высоту внешней фигуры
        # генерируем ширину и высоту внешней фигуры
        b1 = float(randint(10, 15)) + choice((0.0, 0.5))
        h1 = float(randint(8, 12)) + choice((0.0, 0.5))

        logging.debug(u"Ширина внешней фигуры: %.3f" % b1)
        logging.debug(u"Высота внешней фигуры: %.3f" % h1)

        b2 = round(uniform(2.0, (b1 - 2.0)), 2)
        h2 = round(uniform(2.0, (h1 - 2.0)), 2)

        logging.debug(u"Ширина внутренней фигуры: %.3f" % b2)
        logging.debug(u"Высота внутренне фигуры: %.3f" % h2)

        y0 = round(uniform(0.7, h1 - 0.6 - h2), 2)
        z0 = round(uniform(0.7, b1 - 0.6 - b2), 2)

        logging.debug(u"Отступ y0: %.3f" % y0)
        logging.debug(u"Отступ z0: %.3f" % z0)

        self.b1 = b1
        self.h1 = h1
        self.b2 = b2
        self.h2 = h2
        self.z0 = z0
        self.y0 = y0

    # производит корректировку параметров задачи
    def adjust(self):
        (b1, h1, b2, h2, y0, z0) = (self.b1, self.h1,
                                    self.b2, self.h2,
                                    self.y0, self.z0)
        z1 = b1 / 2
        z2 = z0 + b2/2
        y1 = h1 / 2
        y2 = y0 + h2 / 2

        if (b1 - b2 - z0) < 0.5:
            raise Exception()

        if abs(y1 - y2) < 0.9:
            raise Exception()

        A1 = h1 * b1
        A2 = h2 * b2
        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)

        if (abs(yc -y1) < 1.0):
            raise Exception()

        if abs(yc - y2) < 1.0:
            raise Exception()

        if abs(zc - z1) < 0.7:
            raise Exception()

        if abs(zc - z2) < 0.7:
            raise Exception()
        
    # Проверка заданных исходных данных к задаче
    def validate(self):
        if self.z0 + self.b2 >= self.b1:
            raise Exception("Внутренний квадрат выходит за границы внешнего")
        if self.y0 + self.h2 >= self.h1:
            raise Exception("Внутренний квадрат выходит за границы внешнего")

    # возвращает строку с исходными данными 
    # для сохранения в БД
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

    # загружает данные в движок из строки JSON формата
    # данного движка
    def load_store_str(self, store_str):
        loads_obj = loads(store_str)
        self.b1 = float(loads_obj['b1'])
        self.h1 = float(loads_obj['h1'])
        self.b2 = float(loads_obj['b2'])
        self.h2 = float(loads_obj['h2'])
        self.z0 = float(loads_obj['z0'])
        self.y0 = float(loads_obj['y0'])

    # загружает сиходные данные для предосмотра
    # задачи
    def load_preview_params(self):
        self.b1 = 11.0
        self.h1 = 13.0
        self.b2 = 4.0
        self.h2 = 9.0
        self.z0 = 1.0
        self.y0 = 1.0

    # возвращает исходные данные к задаче
    def get_in_params(self):
        params = [
            {'Внешний квадрат':
                [
                    ('Ширина b<sub>1</sub>',self.b1, 'b1'),
                    ('Высота h<sub>1</sub>',self.h1, 'h1')
                ]
            },
            {'Внутренний квадрат':
                [
                    ('Ширина b<sub>2</sub>',self.b2, 'b2'),
                    ('Высота h<sub>2</sub>',self.h2, 'h2')
                ]

            },
            {'Координаты внутреннего квадрата':
                [
                    ('z<sub>0</sub>',self.z0, 'z0'),
                    ('y<sub>0</sub>',self.y0, 'y0')
                ]
            }
        ]
        return params

    # возвращает данные решения
    def get_out_params(self):
        params = [
            {'Координаты центра тяжести каждой из простых фигур':
                [
                    ('z<sub>1</sub>',self.z1),
                    ('z<sub>2</sub>',self.z2),
                    ('y<sub>1</sub>',self.y1),
                    ('y<sub>2</sub>',self.y2)
                ]
            },
            {'Координаты центра тежести фигуры':
                [
                    ('z<sub>c</sub>',self.zc),
                    ('y<sub>c</sub>',self.yc)
                ]
            },
            {'Центральные моменты инерции всей фигуры':
                [
                    ('J<sub>zc</sub>',self.Jzc),
                    ('J<sub>yc</sub>',self.Jyc),
                    ('J<sub>zcyc</sub>',self.Jzcyc)
                ]
            },
            {'Положение главных осей':
                [
                    ('&alpha;<sub>max</sub>', self.alphmax),
                    ('&alpha;<sub>min</sub>', self.alphamin)
                ]
            }
        ]
        return params

    # производит расчет задачи
    def calculate(self):
        b1 = self.b1
        h1 = self.h1
        b2 = self.b2
        h2 = self.h2
        z0 = self.z0
        y0 = self.y0
        # 1. Определим площади простых сечений
        A1 = h1 * b1
        A2 = h2 * b2
        logging.debug("1) A1=%.3f A2=%.3f" % (A1, A2))
        # 2. Определим координаты центра тяжести каждой из фигур
        z1 = b1 / 2
        z2 = z0 + b2/2
        y1 = h1 / 2
        y2 = y0 + h2 / 2
        (self.z1, self.y1, self.z2, self.y2) = (z1, y1, z2, y2)
        logging.debug("2) z1=%.3f y1=%.3f z2=%.3f y2=%.3f" % (z1, y1, z2, y2))
        # 3. Определяем координаты центра тяжести фигуры
        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)
        (self.zc, self.yc) = (zc, yc)
        logging.debug("3) zc=%.3f yc=%.3f" % (zc, yc))
        # 4. Определяем моменты инерции простых фигур составляющих сечение
        Jz1 = (b1 * pow(h1, 3)) / 12
        Jz2 = (b2 * pow(h2, 3)) / 12
        Jy1 = (pow(b1, 3) * h1) / 12
        Jy2 = (pow(b2, 3) * h2) / 12
        logging.debug("4) Jz1=%.3f Jz2=%.3f Jy1=%.3f Jy2=%.3f" % (Jz1, Jz2, Jy1, Jy2))
        # 5. Найдем растояние между центральными осями всего
        # сечение и центральными осями простых фигур
        a1 = y1 - yc
        a2 = y2 - yc
        c1 = z1 - zc
        c2 = z2 - zc
        logging.debug("5) a1=%.3f a2=%.3f c1=%.3f c2=%.3f" % (a1, a2, c1, c2))
        # 6. Найдем моменты инерции простых фигур относительно 
        # центральных осей всего сечения
        Jzci = Jz1 + pow(a1, 2) * A1
        Jzcii = Jz2 + pow(a2, 2) * A2
        Jyci = Jy1 + pow(c1, 2) * A1
        Jycii = Jy2 + pow(c2, 2) * A2
        Jzcyci = a1 * c1 * A1
        Jzcycii = a2 * c2 * A2
        logging.debug("6) Jzci=%.3f, Jzcii=%.3f, Jyci=%.3f, Jycii=%.3f, Jzcyci=%.3f, Jzcycii=%.3f"  % 
            (Jzci, Jzcii, Jyci, Jycii, Jzcyci, Jzcycii))
        # 7. Найдем центральные моменты инерции всей фигуры
        Jzc = Jzci - Jzcii
        Jyc = Jyci - Jycii
        Jzcyc = Jzcyci - Jzcycii
        logging.debug("7) Jzc=%.3f, Jyc=%.3f, Jzcyc=%.3f" % (Jzc, Jyc, Jzcyc))
        (self.Jzc, self.Jyc, self.Jzcyc) = (Jzc, Jyc, Jzcyc)
        # 8. Найдем главные моменты инерции
        a = ((Jzc + Jyc) / 2)
        b = pow(Jzc - Jyc, 2)
        c = 4 * pow(Jzcyc, 2)
        Jmax = a + 0.5 * pow(b + c, 0.5)
        Jmin = a - 0.5 * pow(b + c, 0.5)
        #print "8) ", Jmax, Jmin
        # 9. Найдем положение главных осей
        tanAmax = Jzcyc / (Jyc - Jmax)
        alphamax = degrees(atan(tanAmax))
        tanAmin = Jzcyc / (Jyc - Jmin)
        alphamin = degrees(atan(tanAmin))
        logging.debug("9) alphamax=%.3f, alphamin=%.3f" % (alphamax, alphamin))
        (self.alphmax, self.alphamin) = (alphamax, alphamin)

    # производит отрисовку задачи
    def draw(self, draw, stage):
        x = 5
        y = 5
        b1 = self.b1
        h1 = self.h1
        b2 = self.b2
        h2 = self.h2
        z0 = self.z0
        y0 = self.y0

        (z1, y1, z2, y2) = (self.z1, self.y1, self.z2, self.y2)
        (zc, yc) = (self.zc, self.yc)

        # первый этап - рисунок к задаче
        if stage >= 1:
            # внешний прямоугольник
            draw.Rect(x, y, b1, h1)
            # внутренний прямоугольник
            draw.Rect(z0 + x, y0 + y, b2, h2)
            # подпись высоты внешнего прямоугольника
            draw.Text("h1", x - 0.8, y + h1/2)
            # подпись ширины внешнего прямоугольника
            draw.Text('b1', x + b1/2, y - 0.8)
            # подпись высоты внутреннего прямоугольника
            draw.Text('h2', z0 + x - 0.8, y0 + y + h2/2)
            # подпись ширины внутреннего треугольника
            draw.Text('b2', z0 + x + b2/2, y0 + y - 0.8)
            # расстояние по Z0 от внешнего квадрата
            draw.Line2FillArrow(z0 + x, y0 + y, x, y0 + y)
            # подпись над расстонием Z0
            draw.Text('z0', x + z0/2 - 0.4, y0 + y)
            # расстояние по y0 от внешнего квадрата
            draw.Line2FillArrow(z0 + x, y0 + y, z0 + x, y)
            # подпись над расстонием y0
            draw.Text('y0', z0 + x, y + y0/2 - 0.3)

        # второй этап решение
        if stage >= 2:
            draw.Dot(x + z1, y + y1)
            text = "c1(%.2g;%.2g)" % (z1, y1)
            draw.Text("C2", x + z1, y + y1)

            draw.Dot(x + z2, y + y2)
            text = "c1(%.2g;%.2g)" % (z2, y2)
            draw.Text("C1", x + z2, y + y2)

            draw.Dot(x + zc, y + yc)
            text = "C(%.2g;%.2g)" % (zc, yc)
            draw.Text("C", x + zc, y + yc)

            draw.LineFillArrow(x + zc, y + yc, x + b1 + 2,y + yc)
            draw.Text("Zc", x + b1 + 2,y + yc)
            draw.LineFillArrow(x + zc, y + yc, x + zc, y + h1 + 1)
            draw.Text("Yc", x + zc, y + h1 + 1)

            (alphamax, alphamin) = (self.alphmax, self.alphamin) 
            (Xu, Yu) = rotate_line(x + zc, y + yc,  x + b1 + 2, y + yc, alphamax)
            draw.LineFillArrow(x + zc, y + yc, Xu, Yu)
            draw.Text("U", Xu, Yu)
            (Xv, Yv) = rotate_line(x + zc, y + yc,  x + b1 + 2, y + yc, alphamin)
            draw.LineFillArrow(x + zc, y + yc,Xv, Yv)
            draw.Text("V", Xv, Yv)

        return draw

if __name__ == '__main__':
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

    for i in xrange(1):
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