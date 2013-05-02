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
import math

class ProblemEngine(Engine):
    name = u"Задача 9. Растяжение"
    short_name = __name__
    category = "Задачи на растяжение и сжатие"
    description = """
                  Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                  tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                  quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                  consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                  cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                  proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                  """
    stage_count = 2

    def randomize_in_params(self):
        pass

    def load_preview_params(self):
        self.l1 = 4.0
        self.l2 = 1.0
        self.l3 = 3.0
        self.P1 = 50.0
        self.P2 = 20.0
        self.P3 = -60.0
        self.Qt = 280.0
        self.nt = 1.6
        self.E = 210

    def adjust(self):
        pass

    def validate(self):
        pass

    def validate(self):
        pass

    def load_store_str(self, store_str):
        loads_obj = loads(store_str)
        self.l1 = float(loads_obj['l1'])
        self.l2 = float(loads_obj['l2'])
        self.l3 = float(loads_obj['l3'])
        self.P1 = float(loads_obj['P1'])
        self.P2 = float(loads_obj['P2'])
        self.P3 = float(loads_obj['P3'])
        self.Qt = float(loads_obj['Qt'])
        self.nt = float(loads_obj['nt'])
        self.E = 210.0

    def get_store_str(self):
        pass

    def get_in_params(self):
        params = [
            {'Длины участков':
                [
                    ('l<sub>1</sub>', self.l1, 'l1'),
                    ('l<sub>2</sub>', self.l2, 'l2'),
                    ('l<sub>3</sub>', self.l3, 'l3')
                ]
            },
            {'Силы действующие на участках':
                [
                    ('P<sub>1</sub>',self.P1, 'P1'),
                    ('P<sub>2</sub>',self.P2, 'P2'),
                    ('P<sub>3</sub>',self.P3, 'P3')
                ]
            },
            {'Другие параметры':
                [
                    ('&sigma;',self.Qt, 'Qt'),
                    ('n<sub>T</sub>', self.nt, 'nt'),
                    ('E', self.E, 'E', 'noedit')
                ]
            }
        ]

        return params

    def get_out_params(self):
        params = [
            {'Усилия действующие на каждом участке':
                [
                    ('N<sub>1</sub>', self.N1),
                    ('N<sub>2</sub>', self.N2),
                    ('N<sub>3</sub>', self.N3)
                ]
            },
            {'Значение допускаемого няпржения':
                [
                    ('[&sigma;]', self.Q)
                ]
            },
            {'Размеры поперечного сечения':
                [
                    ('d<sub>1</sub>', self.d1),
                    ('d<sub>2</sub>', self.d2),
                    ('a', self.a)
                ]
            },
            {'Удлинения участков стержня:':
                [  
                    ('&Delta;<sub>1</sub>', self.dl1),
                    ('&Delta;<sub>2</sub>', self.dl2),
                    ('&Delta;<sub>3</sub>', self.dl3)
                ]
            },
            {'Перемещения характерных сечений стержня':
                [
                    ('&Delta;<sub>B</sub>', self.dlB),
                    ('&Delta;<sub>C</sub>', self.dlC),
                    ('&Delta;<sub>D</sub>', self.dlD),
                ]
            }
        ]
        return params
    
    def calculate(self):
        (l1, l2, l3, 
         P1, P2, P3,
         Qt, nt, E) = (self.l1, self.l2, self.l3,
                       self.P1, self.P2, self.P3,
                       self.Qt, self.nt, self.E)
        # Определяем усилия действующие на каждом участке
        # Используем метод сечений
        # Участок 1
        N1 = P1
        # Участок 2
        N2 = P1 + P2
        # Участок 3
        N3 = P1 + P2 + P3
        (self.N1, self.N2, self.N3) = (N1, N2, N3)
        logging.debug("2: N1=%.3f N2=%.3f N3=%.3f" % (N1, N2, N3))
        # Определяем размеры поперечного сечения стержня
        # Определим значение допускаемого напряжения
        Q = (Qt / nt)
        self.Q = Q
        logging.debug("Q=%.3f" % Q)
        # Участок 1
        A1 = (abs(N1) / Q) * 1000
        d1 = ((4.0 * A1) / 3.14) ** 0.5
        self.d1 = d1
        # округляем полученное значени до целого числа в большую сторону
        # принимаем
        df1 = math.ceil(d1)
        self.df1 = df1
        # Определим фактическую площадь сечения
        Af1 = (3.14 * (df1 ** 2)) / 4
        logging.debug("A1=%.3f d1=%.3f df1=%.3f Af1=%.3f" % (A1, d1, df1, Af1))
        # Участок 2
        A2 = (abs(N2) / Q) * 1000
        d2 = ((4.0 * A2) / 3.14) ** 0.5
        self.d2 = d2
        # Округляем полученное значение до целого числа в большую сторону
        # Принимаем
        df2 = math.ceil(d2)
        self.df2 = df2
        # Определяем фактическую площадь сечения
        Af2 = ((3.14 * (df2 ** 2)) / 4.0)
        logging.debug("A2=%.3f d2=%.3f df2=%.3f Af2=%.3f" % (A2, d2, df2, Af2))
        # Участок 3
        A3 = (abs(N3) / Q) * 1000
        a = A3 ** 0.5
        # Округляем полученное значение до целого числа в большую сторону
        # Принимаем
        a = math.ceil(a)
        self.a = a
        # Определим фактическую площадь сечения
        Af3 = a ** 2
        logging.debug("A3=%.3f a=%.3f Af3=%.3f" % (A3, a, Af3))
        # 4. Определим максимальные напряжения на каждом участке
        q1 = (abs(N1) / Af1) * 1000
        q1 = Q if q1 < Q else q1
        q2 = (abs(N2) / Af2) * 1000
        q2 = Q if q2 < Q else q2
        q3 = (abs(N3) / Af3) * 1000
        q3 = Q if q3 < Q else q3
        logging.debug("q1=%.3f q2=%.3f q3=%.3f" % (q1, q2, q3))
        # 5. Определим удлинение участков стержня
        dl1 = ((N1 * l1) / (E * Af1)) * 1000
        dl2 = ((N2 * l2) / (E * Af2)) * 1000
        dl3 = ((N3 * l3) / (E * Af3)) * 1000
        (self.dl1, self.dl2, self.dl3) = (dl1, dl2, dl3)
        logging.debug("dl1=%.3f dl2=%.3f dl3=%.3f" % (dl1, dl2, dl3))
        # 6. Определим перемещения характерных сечений стержня
        dlA = 0.0
        dlB = dlA + dl3
        dlC = dlB + dl2
        dlD = dlC + dl1
        (self.dlB, self.dlC, self.dlD) = (dlB, dlC, dlD)
        logging.debug("dlB=%.3f dlC=%.3f dlD=%.3f" % (dlB, dlC, dlD))

    def draw(self, draw, stage = 1):
        (x, y) = (5, 5)
        (l1, l2, l3,
         df1, df2, a,
         P1, P2, P3) = (self.l1, self.l2, self.l3, 
                         self.df1, self.df2, self.a,
                         self.P1, self.P2, self.P3)
        # начинаем все заново
        # получеам значение суммы длин всех трех участков
        Le = 10.0 # эталонное для рисунка
        L = sum((l1, l2, l3))
        # перерасчитываем длины участков для рисунка через пропорцию к эталонному
        lx1 = (l1 * Le) / L
        lx2 = (l2 * Le) / L
        lx3 = (l3 * Le) / L
        logging.debug("lx1=%.3f lx2=%.3f lx3=%.3f" % (lx1, lx2, lx3))
        # начинаем рисовать всю фигуру
        if stage == 1 or stage == 2:
            # рисуем граничную линию
            draw.Line(x, y + 5, x, y + 11)
            # эталонная величина сечения для неизвестного - 4
            # рисуем участок номер 3
            draw.Rect(x, y + 6, lx3, 4)
            # рисуем участок номер 2
            draw.Rect(x + lx3, y + 6.5, lx2, 3)
            # рисуем участок номер 1
            draw.Rect(x + lx3 + lx2, y + 6, lx1, 4)
            # рисуем размеры трех участков
            # 3
            draw.Line(x + lx3, y + 10, x + lx3, y + 11)
            draw.Line2FillArrow(x, y + 10.5, x + lx3, y + 10.5)
            draw.TopAlignText("l3", x + (lx3 / 2.0), y + 10.5)
            # 2
            draw.Line(x + lx3 + lx2, y + 9.5, x + lx3 + lx2, y + 11)
            draw.Line2FillArrow(x + lx3, y + 10.5, x + lx3 + lx2, y + 10.5)
            draw.TopAlignText("l2", x + lx3 + (lx2 / 2.0), y + 10.5)
            # 1
            draw.Line(x + lx3 + lx2 + lx1, y + 10, x + lx3 + lx2 + lx1, y + 11)
            draw.Line2FillArrow(x + lx3 + lx2, y + 10.5, x + lx3 + lx2 + lx1, y + 10.5)
            draw.TopAlignText("l3", x + lx3 + lx2 + (lx1 / 2.0), y + 10.5)
            # переходим к отрисовке направлений сил
            # определяем направления сил
            direction1 = 0.8 if P1 > 10 else -0.8
            direction2 = 0.8 if P2 > 10 else -0.8
            direction3 = 0.8 if P3 > 10 else -0.8
            # 3
            draw.LineFillArrow(x + lx3, y + 8, x + lx3 + direction3, y + 8)
            draw.TopAlignText("P3", x + lx3 + (direction3 / 2.0), y + 8)
            # 2
            draw.LineFillArrow(x + lx3 + lx2, y + 8, x + lx3 + lx2 + direction2, y + 8)
            draw.TopAlignText("P2", x + lx3 + lx2 + (direction2 / 2.0), y + 8)
            # 1
            draw.LineFillArrow(x + lx3 + lx2 + lx1, y + 8, x + lx3 + lx2 + lx1 + direction1, y + 8)
            draw.TopAlignText("P1", x + lx3 + lx2 + lx1 + (direction1 / 2.0), y + 8)
            # переходим к отрисовке контуров фигур
            # отрисовываем первый квадрат
            draw.Rect(x + 1, y, 3, 3)
            # отрисовываем его размеры
            draw.Line(x, y, x + 1, y)
            draw.Line(x, y + 3, x + 1, y + 3)
            draw.Line2FillArrow(x + 0.5, y, x + 0.5, y + 3)
            draw.LeftAlignText("a", x + 0.5, y + 1.5)
            draw.Line(x + 1, y, x + 1, y - 1)
            draw.Line(x + 4, y, x + 4, y - 1)
            draw.Line2FillArrow(x + 1, y - 0.5, x + 4, y - 0.5)
            draw.BottomAlignText("a", x + 2.5, y - 0.5)
            # рисуем первый круг
            draw.Circle(x + 6.0, y + 1.5, 1.5)
            # рисуем диаметр первого круга
            draw.Line(x + 5.25, y + 1.5, x + 5.25, y - 1)
            draw.Line(x + 6.75, y + 1.5, x + 6.75, y - 1)
            draw.Line2FillArrow(x + 5.25, y - 0.5, x + 6.75, y - 0.5)
            draw.BottomAlignText("d2", x + 6.0, y - 0.5)
            # рисуем второй круг
            draw.Circle(x + 9.0, y + 1.5, 3.0)
            # рисуем диаметр второго круга
            draw.Line(x + 7.5, y + 1.5, x + 7.5, y - 1)
            draw.Line(x + 10.5, y + 1.5, x + 10.5, y - 1)
            draw.Line2FillArrow(x + 7.5, y - 0.5, x + 10.5, y - 0.5)
            draw.BottomAlignText("d1", x + 9.0, y - 0.5)
        elif stage == 2:
            pass
        return draw

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    engine = ProblemEngine()
    engine.load_preview_params()
    engine.calculate()
    engine.get_image(stage = 2).show()