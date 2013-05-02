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

def round_list(lst):
    return [round(item, 3) for item in lst]

class ProblemEngine(Engine):
    name = "Задача 3. Квадрат с вырезом (сверху)"
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
        "Генерация исходных данных к задаче."
        # генерируем ширину и высоту внешней фигуры
        b1 = float(randint(10, 15)) + choice((0.0, 0.5))
        h1 = float(randint(8, 12)) + choice((0.0, 0.5))

        logging.debug(u"Ширина внешней фигуры: %.3f" % b1)
        logging.debug(u"Высота внешней фигуры: %.3f" % h1)

        # генерируем высоту выреза
        # минимум 3.0 см максимум h1 - 1.0
        h2 = round(uniform(3.5, h1 - 1.0), 2)
        logging.debug(u"Высота выреза: %.3f" % h2)
        # генерируем ширину выреза
        # минимум 3.0 см максимум b1 - 2.0
        b2 = round(uniform(3.0, (b1 - 2.0)), 2)
        logging.debug(u"Ширина выреза: %.3f" % b2)
        # генерируем отступ z0
        # минимум 0.7 максимум b1 - b2 - 0.6
        z0 = round(uniform(0.9, (b1 - b2 - 0.7)), 2)
        logging.debug(u"Отступ выреза: %.3f" % z0)

        (self.b1, self.h1, self.b2, self.h2, self.z0) = (b1, h1, b2, h2, z0)

    def load_preview_params(self):
        "Загрузка исходных данных для предварительного просмотра."
        
        self.h1 = 9.0 # высота внешней фигуры
        self.b1 = 10.0 # ширина
        self.h2 = 6.0 # высота выреза
        self.b2 = 7.0 # ширина
        self.z0 = 2.0 # отступ выреза от левого края

    def adjust(self):
        """
        Метод выполняющий проверку корректности сгенерированных 
        исходных данных. В случае если данные не корректны, и 
        имеется возможность их исправить - данные исправляются,
        в отсутствие возможности - даннные отбрасываются.
        """
        (b1, h1, b2, h2, z0) = (self.b1, self.h1, self.b2, self.h2, self.z0)

        if (b1 - (z0 + b2)) < 0.5:
            raise Exception(u"Расстояние между вырезом и краем внешней фигуры меньше 0.5")
        if (h1 - h2) < 0.5:
            raise Exception(u"Расстояние между вырезом и нижним краем вншней фигуры меньше 0.5")

        A1 = h1 * b1
        A2 = h2 * b2
 
        z1 = b1 / 2.0
        z2 = z0 + (b2 / 2.0)
        y1 = h1 / 2.0
        y2 = h1 - h2 + (h2 / 2.0)

        if abs(y1 - y2) < 1.0:
            raise Exception(u"Растояние между центрами тяжести простых фигур по y слишком мало")
        if abs(z1 - z2) < 1.0:
            raise Exception(u"Растояние между центрами тяжести простых фигур по z слишком мало")

        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)

        if abs(zc - z1) < 1.0:
            raise Exception(u"Растояние между центрам тяжести простой фигуры и всей фигуры по z слишком мало")
        if abs(zc - z2) < 1.0:
            raise Exception(u"Растояние между центрам тяжести выреза и всей фигуры по z слишком мало")
        if abs(yc - y1) < 1.0:
            raise Exception(u"Растояние между центрам тяжести простой фигуры и всей фигуры по y слишком мало")
        if abs(yc - y2) < 1.0:
            raise Exception(u"Растояние между центрам тяжести выреза и всей фигуры по y слишком мало")

    def validate(self):
        "Метод валидации полученных исходных данных."
        (h1, b1, h2, b2, z0) = (self.h1, self.b1, self.h2, self.b2, self.z0)

        if (h1 - h2) <= 0.0:
            raise Exception(u"Высота выреза должна быть меньше высоты фигуры.")
        if (b1 - (b2 + z0)) <= 0.0:
            raise Exception(u"Ширина выреза + отступ слишком большие для данной фигуры.")

    def get_store_str(self):
        """
        Метод возвращающий строку с исходными данными для хранения 
        в БД.
        """
        dump_obj = {
            'b1': self.b1,
            'h1': self.h1,
            'b2': self.b2,
            'h2': self.h2,
            'z0': self.z0
        }
        return dumps(dump_obj)

    def load_store_str(self, store_str):
        """
        Метод выполняющий загрузку исходных данных из 
        предоставленной строки.
        """
        loads_obj = loads(store_str)
        self.b1 = float(loads_obj['b1'])
        self.h1 = float(loads_obj['h1'])
        self.b2 = float(loads_obj['b2'])
        self.h2 = float(loads_obj['h2'])
        self.z0 = float(loads_obj['z0'])

    def get_in_params(self):
        """
        Возвращает структуру данных описывающую исходные данные
        к задаче.
        """
        params = [
            {'Внешний квадрат':
                [
                    ('Ширина b<sub>1</sub>',self.b1, 'b1', '', 'см'),
                    ('Высота h<sub>1</sub>',self.h1, 'h1', '', 'см')
                ]
            },
            {'Вырез':
                [
                    ('Ширина b<sub>2</sub>',self.b2, 'b2', '', 'см'),
                    ('Высота h<sub>2</sub>',self.h2, 'h2', '', 'см')
                ]

            },
            {'Координата выреза':
                [
                    ('z<sub>0</sub>',self.z0, 'z0', '', 'см')
                ]
            }
        ]
        return params

    def get_out_params(self):
        """
        Возвращает структуру данных описывающую расчитанные данные
        к задаче.
        """
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
        "Метод выполняеющий расчет задачи."
        
        # экспортируем переменные экземпляра (исходные данные)
        # к задаче в локальное пространство имен метода
        (h1, b1, h2, b2, z0) = (self.h1, self.b1, 
                                self.h2, self.b2, self.z0)
        # 1. Определим площади простых сечений
        A1 = h1 * b1
        A2 = h2 * b2
        logging.debug("1: A1=%.3f A2=%.3f" % (A1, A2))
        # 2. Определим координаты центра тяжести каждой из
        # простых фигур
        z1 = b1 / 2.0
        z2 = z0 + (b2 / 2.0)
        y1 = h1 / 2.0
        y2 = h1 - h2 + (h2 / 2.0)
        (z1, z2, y1, y2) = round_list((z1, z2, y1, y2))
        (self.z1, self.z2, self.y1, self.y2) = (z1, z2, y1, y2)
        logging.debug("2: z1=%.3f z2=%.3f y1=%.3f y2=%.3f" % 
                (z1, z2, y1, y2))
        # 3. Определяем координаты центра тяжести фигуры
        zc = (A1 * z1 - A2 * z2) / (A1 - A2)
        yc = (A1 * y1 - A2 * y2) / (A1 - A2)
        (zc, yc) = round_list((zc, yc))
        (self.zc, self.yc) = (zc, yc)
        logging.debug("3: zc=%.3f yc=%.3f" % (zc, yc))
        # 4. Определяем моменты инерции простых фигур
        # состовляющих сечение
        Jz1 = (b1 * (h1 ** 3)) / 12.0
        Jz2 = (b2 * (h2 ** 3)) / 12.0
        Jy1 = ((b1 ** 3) * h1) / 12.0
        Jy2 = ((b2 ** 3) * h2) / 12.0
        (Jz1, Jz2, Jy1, Jy2) = round_list((Jz1, Jz2, Jy1, Jy2))
        logging.debug("4: Jz1=%.3f Jz2=%.3f Jy1=%.3f Jy2=%.3f" % 
                (Jz1, Jz2, Jy1, Jy2))
        # 5. Найдем растояние между центральными осями всего 
        # сечения и центральями осями простых фигур
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
        (self.Jzc, self.Jyc, self.Jzcyc) = (Jzc, Jyc, Jzcyc)
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
        "Метод выполняеющий отрисовку расчетной схемы."
        (x, y) = (5, 5)
        (b1, h1, b2, h2, z0) = (self.b1, 
                                self.h1,
                                self.b2,
                                self.h2,
                                self.z0)
        y0 = h1 - h2
        # формируем координаты полигона всей фигуры
        polygon = ((x, y),
                   (x, y + h1),
                   (x + z0, y + h1),
                   (x + z0, y + y0),
                   (x + z0 + b2, y + y0),
                   (x + z0 + b2, y + h1),
                   (x + b1, y + h1),
                   (x + b1, y))
        # рисуем полигон фигуры
        draw.Polygon(polygon)
        # рисуем подписи внешней фигуры
        draw.Text("b1", x + b1 / 2.0 - 0.5, y - 0.7)
        draw.Text("h1", x - 0.7, y + h1 / 2.0)
        # рисуем подписи выреза
        draw.Text("b2", x + z0 + b2 / 2.0 - 0.5, y + y0 - 0.7)
        draw.Text("h2", x + z0 - 0.7, y + y0 + h2 / 2.0 - 0.7)
        # рисуем стралку для координаты z0
        draw.Line2FillArrow(x, y + y0, x + z0, y + y0)
        # рисуем подпись координаты z0
        draw.Text("z0", x + (z0 / 2.0) - 0.3, y + y0)
        # рисуем примитивы для уровня два отрисовки
        if stage >= 2:
            # рисуем координаты центра тяжести каждой из простых фигур
            (z1, z2, y1, y2) = (self.z1, self.z2, self.y1, self.y2)
            # координата внешней фигуры
            draw.Dot(x + z1, y + y1)
            # подпись координаты
            draw.Text("C1", x + z1, y + y1)
            # рисуем стрелки координаты центра тяжести внешней фигуры
            # Y1
            draw.LineFillArrow(x + z1, y + y1, x + z1, y + h1 + 3)
            # рисуем подпись над стрелкой Y1
            draw.Text("Y1", x + z1, y + h1 + 3)
            # Z1 
            draw.LineFillArrow(x + z1, y + y1, x + b1 + 3,y + y1)
            # рисуем подпись над стрелкой Z1
            draw.Text("Z1", x + b1 + 3,y + y1)
            # координата внешней фигуры
            draw.Dot(x + z2, y + y2)
            # подпись координаты
            draw.Text("C2", x + z2, y + y2)
            # рисуем стрелки координаты центра тяжести выреза
            # Y2
            draw.LineFillArrow(x + z2, y + y2, x + z2, y + h1 + 3)
            # рисуем подпись над стрелкой
            draw.Text("Y2", x + z2, y + h1 + 3)
            # Z2
            draw.LineFillArrow(x + z2, y + y2, x + b1 + 3, y + y2)
            # рисуем подпись над стрелкой
            draw.Text("Z2",  x + b1 + 3, y + y2)
            # рисуем координаты центра тяжести всей фигуры
            (zc, yc) = (self.zc, self.yc)
            # координата всей фигуры
            draw.Dot(x + zc, y + yc)
            # подпись координаты
            draw.Text("C", x + zc, y + yc)
            # рисуем стрелки координаты центра тяжести всей фигуры
            # Yc
            draw.LineFillArrow(x + zc, y + yc, x + zc, y + h1 + 3)
            draw.Text("Yc", x + zc, y + h1 + 3)
            # Zc
            draw.LineFillArrow(x + zc, y + yc, x + b1 + 3, y + yc)
            draw.Text("Zc", x + b1 + 3, y + yc)
            # рисуем положение главных осей
            (alphamax, alphamin) = (self.alphamax, self.alphamin)

            (Xv, Yv) = rotate_line(x + zc, y + yc, x + zc + 5, y + yc, alphamin)
            draw.LineFillArrow(x + zc, y + yc, Xv, Yv)
            draw.Text("V", Xv, Yv)
            logging.debug("Xv=%.3f Yv=%.3f" % (Xv, Yv))
            (Xu, Yu) = rotate_line(x + zc, y + yc, x + zc + 5, y + yc, alphamax)
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