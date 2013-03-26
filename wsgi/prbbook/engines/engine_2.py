#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.draw import DesignDraw
from math import atan, degrees
from lib.draw_math import rotate_line
from lib.engine import Engine
from json import dumps, loads
from random import randint
from termcolor import colored, cprint

class ProblemEngine(Engine):
    name = u"Задача 2. Квадрат с вырезом (справа)"
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

    # загрузка данных для предосмотра
    def load_preview_params(self):
        self.b1 = 12.0
        self.h1 = 12.0
        self.b2 = 6.0
        self.h2 = 8.0
        self.y0 = 3.0
        self.z0 = self.b1 - self.b2

    def get_in_params(self):
        params = [
            {'Внешний квадрат':
                [
                    ('Ширина b<sub>1</sub>',self.b1, 'b1'),
                    ('Высота h<sub>1</sub>',self.h1, 'h1')
                ]
            },
            {'Вырез':
                [
                    ('Ширина b<sub>2</sub>',self.b2, 'b2'),
                    ('Высота h<sub>2</sub>',self.h2, 'h2')
                ]

            },
            {'Координаты выреза':
                [
                    ('z<sub>0</sub>',self.z0, 'z0'),
                    ('y<sub>0</sub>',self.y0, 'y0')
                ]
            }
        ]
        return params

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
                    ('&alpha;<sub>max</sub>', self.alphamax),
                    ('&alpha;<sub>min</sub>', self.alphamin)
                ]
            }
        ]
        return params

    # выполняет расчет задачи
    def calculate(self):
        print colored("Calculate method", "red")
        # присваиваем глобальные переменные объекта локальным
        (b1, h1, b2, h2, y0, z0) = (self.b1, self.h1,
                                    self.b2, self.h2,
                                    self.y0, self.z0)
        # 1. Определим площади простых сечений
        A1 = h1 * b1
        A2 = h2 * b2
        print colored("1: ", "red"), 
        print colored("A1=%.3f A2=%.3f" % (A1, A2), "yellow")
        # 2. Определим координаты центра тяжести каждой из простых фигур
        z1 = b1 / 2.0
        z2 = b1 - b2 + (b2 / 2.0)
        y1 = h1 / 2.0
        y2 = y0 + (h2 / 2.0)
        (self.z1, self.z2, self.y1, self.y2) = (z1, z2, y1, y2)
        print colored("2: ", "red"), 
        print colored("z1=%.3f z2=%.3f y1=%.3f y2=%.3f" % 
                                (z1, z2, y1, y2), "yellow")
        # 3. Определяем координаты центра тяжести фигуры
        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)
        (self.zc, self.yc) = (zc, yc)
        print colored("3: ", "red"), 
        print colored("zc=%.3f yc=%.3f" % (zc, yc), "yellow")
        # 4. Определяем моменты инерции простых фигур состовляющих сечение
        Jz1 = (b1 * (h1 ** 3)) / 12.0
        Jz2 = (b2 * (h2 ** 3)) / 12.0
        Jy1 = ((b1 ** 3) * h1) / 12.0
        Jy2 = ((b2 ** 3) * h2) / 12.0
        print colored("4: ", "red"), 
        print colored("Jz1=%.3f Jz2=%.3f Jy1=%.3f Jy2=%.3f" % 
                                (Jz1, Jz2, Jy1, Jy2), "yellow")
        # 5. Найдем растояние между центральными осями всего сечения и
        #    центральными осями простых фигур
        a1 = y1 - yc
        a2 = y2 - yc
        c1 = z1 - zc
        c2 = z2 - zc
        print colored("5: ", "red"), 
        print colored("a1=%.3f a2=%.3f c1=%.3f c2=%.3f" % 
                                (a1, a2, c1, c2), "yellow")
        # 6. Найдем моменты инерции простых фигур относительно центральных 
        #    осей всего сечения
        Jzc1 = Jz1 + (a1 ** 2) * A1
        Jzc2 = Jz2 + (a2 ** 2) * A2
        Jyc1 = Jy1 + (c1 ** 2) * A1
        Jyc2 = Jy2 + (c2 ** 2) * A2
        Jzcyc1 = a1 * c1 * A1
        Jzcyc2 = a2 * c2 * A2
        print colored("6: ", "red"), 
        print colored("Jzc1=%.3f Jzc2=%.3f Jyc1=%.3f Jyc2=%.3f Jzcyc2=%.3f Jzcyc2=%.3f" % 
                                (Jzc1, Jzc2, Jyc1, Jyc2, Jzcyc1, Jzcyc2), "yellow")
        # 7. Найдем центральные моменты инерции всей фигуры
        Jzc = Jzc1 - Jzc2
        Jyc = Jyc1 - Jyc2
        Jzcyc = Jzcyc1 - Jzcyc2
        (self.Jzc, self.Jyc, self.Jzcyc) = (Jzc, Jyc, Jzcyc)
        print colored("7: ", "red"), 
        print colored("Jzc=%.3f Jyc=%.3f Jzcyc=%.3f" % 
                                (Jzc, Jyc, Jzcyc), "yellow")
        # 8. Найдем главные моменты инерции
        Jmax = ((Jzc + Jyc) / 2.0) + 0.5 * (((Jzc - Jyc) ** 2 + 4 * Jzcyc ** 2) ** 0.5)
        Jmin = ((Jzc + Jyc) / 2.0) - 0.5 * (((Jzc - Jyc) ** 2 + 4 * Jzcyc ** 2) ** 0.5)
        print colored("8: ", "red"),
        print colored("Jmax=%.3f Jmin=%.3f" % (Jmax, Jmin), "yellow")
        # 9. Найдем положение главных осей
        tanAmax = Jzcyc / (Jyc - Jmax)
        Amax = degrees(atan(tanAmax))
        tanAmin = Jzcyc / (Jyc - Jmin)
        Amin = degrees(atan(tanAmin))
        (self.alphamax, self.alphamin) = (Amax, Amin)
        print colored("9: ", "red"),
        print colored("tanAmax=%.3f Amax=%.3f tanAmin=%.3f Amin=%.3f" % 
                            (tanAmax, Amax, tanAmin, Amin), "yellow")
        return locals()


    def draw(self, draw, stage):
        (x, y) = (5, 5)
        (b1, h1, b2, h2, z0, y0) = (self.b1, 
                                    self.h1,
                                    self.b2,
                                    self.h2,
                                    self.z0,
                                    self.y0)
        # формируем координаты полигона фигуры
        polygon = ((x, y), 
                   (x, y + h1), 
                   (x + b1, y + h1),
                   (x + b1, y + h2 + y0),
                   (x + z0, y + h2 + y0),
                   (x + z0, y + y0),
                   (x + b1, y + y0),
                   (x + b1, y))
        # рисуем полигон фигуры
        draw.Polygon(polygon)
        # рисуем подписи внешней фигуры
        draw.Text("h1", x - 0.8, y + (h1 / 2.0) - 0.3)
        draw.Text("b1", x + (b1 / 2.0) - 0.8, y - 0.8) 
        # рисуем подписи выреза
        draw.Text("h2", x + z0 - 0.8, y + y0 + (h2 / 2.0) - 0.3)
        draw.Text("b2", x + z0 + (b2 / 2.0) - 0.3, y + y0 - 0.8)
        # рисуем стрелку для координаты z0
        draw.Line2FillArrow(x, y + y0, x + z0, y + y0)
        # рисуем подпись координаты
        draw.Text("z0", x + (z0 / 2.0) - 0.3, y + y0)
        # рисуем стрелку для координаты y0
        draw.Line2FillArrow(x + z0, y, x + z0, y + y0)
        # рисуем подпись координаты
        draw.Text("y0", x + z0, y + (y0 / 2.0) - 0.3)

        if stage >= 2:
            # рисуем координаты центра тяжести кажой из простых фигур
            (z1, z2, y1, y2) = (self.z1, self.z2, self.y1, self.y2)
            # координата внешней фигуры
            draw.Dot(x + z1, y + y1)
            # подпись координаты
            draw.Text("C1", x + z1, y + y1)
            # рисуем стрелки координат центра тяжести внешней фигуры
            draw.LineFillArrow(x + z1, y + y1, x + z1, y + 16)
            # рисуем подпись над стрелкой
            draw.Text("Y1", x + z1, y + 16)
            # рисуем стрелки координат центра тяжести выреза
            draw.LineFillArrow(x + z2, y + y2, x + z2, y + 16)
            # рисуем подпись над стрелкой
            draw.Text("Y2", x + z2, y + 16)
            # координата выреза
            draw.Dot(x + z2, y + y2)
            # подпись координаты
            draw.Text("C2", x + z2, y + y2)
            # рисуем координату центра тяжести всей фигуры
            (zc, yc) = (self.zc, self.yc)
            # координата всей фигуры
            draw.Dot(x + zc, y + yc)
            # подпись координаты
            draw.Text("C", x + zc, y + yc)
        return draw

if __name__ == '__main__':
    engine = ProblemEngine()
    engine.load_preview_params()
    engine.calculate()
    engine.get_image(stage = 2).show()