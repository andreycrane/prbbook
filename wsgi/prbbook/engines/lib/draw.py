#!/usr/bin/env python
# -*- coding: utf8 -*-

import Image, ImageFont, ImageOps
from ImageDraw import Draw
from math import atan2, pi, cos, sin, pow
from os.path import dirname, abspath

class DesignDraw:
    def __init__(self, width = 300, height = 300, alpha = 30):
        # сохраняем высоту и ширину картинки
        self.width = width
        self.height = height
        self.im = Image.new('RGB', (width, height), (255, 255, 255)) # создаем пустое изображение
        self.draw = Draw(self.im)
        self.font = ImageFont.truetype(dirname(abspath(__file__)) + '/GOST_A.TTF', 17)
        self.alpha = alpha

    # функция преобразующая сантиметры в пиксели
    def sm2px(self, sm):
        return (sm * self.alpha)
        
    # функция преобразующая координаты из декартовой
    # в экранную систему координат
    # координаты в пикселях
    def dec2screen(self, x, y):
        return (x, self.height - y)

    def Show(self):
        invert_im = ImageOps.invert(self.im)
        bbox = invert_im.getbbox()
        self.im = self.im.crop((bbox[0] -5, bbox[1] - 5, bbox[2] + 5, bbox[3] + 5))
        self.im.show()

    def Crop(self):
        invert_im = ImageOps.invert(self.im)
        bbox = invert_im.getbbox()
        self.im = self.im.crop((bbox[0] -5, bbox[1] - 5, bbox[2] + 5, bbox[3] + 5))

    def Size(self):
        """
        Возвращает (ширину, высоту) изображения.
        """
        return self.im.size

    def Resize(self, width = 400, height = 400):
        self.im = self.im.resize((width, height), Image.ANTIALIAS)

    # функция рисующая точку 
    # принимаемые координаты в декартовой системе координат
    # в сантиметрах
    def Dot(self, x, y, radius = 5):
        halfr = radius / 2
        x = self.sm2px(x)
        y = self.sm2px(y)
        (x, y) = self.dec2screen(x, y)
        self.draw.ellipse((x - halfr, y - halfr, x + halfr, y + halfr), fill=(0, 0, 0, 0))

    # функция рисующая прямоугольник
    # принимаемые координаты в декартовой системе координат
    # в сантиметрах
    # x, y - нижний левый угол
    def Rect(self, x, y, width, height):
        x = self.sm2px(x)
        y = self.sm2px(y)
        width = self.sm2px(width)
        height = self.sm2px(height)
        (x, y) = self.dec2screen(x, y)
        self.draw.rectangle((x, y - height, x + width, y), outline="black")

    # функция рисующая линию с незакрашенной стрелкой в конце
    # принимаемые координаты в декартовой системе
    # в сантиметрах
    def LineStrokeArrow(self, x1, y1, x2, y2, headlen = 10, headwid = 6):
        [x1, y1, x2, y2] =  [self.sm2px(x1), self.sm2px(y1), self.sm2px(x2), self.sm2px(y2)]
        [x1, y1] = self.dec2screen(x1, y1)
        [x2, y2] = self.dec2screen(x2, y2)

        angle = atan2(y2 - y1, x2 - x1)
        self.draw.line((x1, y1, x2, y2), fill="black")
        # координаты левого крыла
        (lwx, lwy) = (x2 - headlen * cos(angle - pi / headwid), y2 - headlen * sin(angle - pi / headwid))
        # координаты правого крыла
        (rwx, rwy) = (x2 - headlen * cos(angle + pi / headwid), y2 - headlen * sin(angle + pi / headwid))
        # рисуем крылья
        self.draw.line((x2, y2, lwx, lwy), fill="black")
        self.draw.line((x2, y2, rwx, rwy), fill="black")

    # функция рисующая линию с закрашенной стрелкой в конце
    # принимаемые координаты в декартовой системе
    # в сантиметрах
    def LineFillArrow(self, x1, y1, x2, y2, headlen = 10, headwid = 6):
        [x1, y1, x2, y2] =  [self.sm2px(x1), self.sm2px(y1), self.sm2px(x2), self.sm2px(y2)]
        [x1, y1] = self.dec2screen(x1, y1)
        [x2, y2] = self.dec2screen(x2, y2)

        angle = atan2(y2 - y1, x2 - x1)
        self.draw.line((x1, y1, x2, y2), fill="black")
        # координаты левого крыла
        (lwx, lwy) = (x2 - headlen * cos(angle - pi / headwid), y2 - headlen * sin(angle - pi / headwid))
        # координаты правого крыла
        (rwx, rwy) = (x2 - headlen * cos(angle + pi / headwid), y2 - headlen * sin(angle + pi / headwid))
        lines = [(x2, y2), (lwx, lwy), (rwx, rwy)]
        self.draw.polygon(lines, fill="black")

    # функция рисующая линию с закрашенными стрелками на концах
    # принимаемые координаты в декартовой системе
    # в сантиметрах
    def Line2FillArrow(self, x1, y1, x2, y2, headlen = 5, headwid = 5):
        [x1, y1, x2, y2] =  [self.sm2px(x1), self.sm2px(y1), self.sm2px(x2), self.sm2px(y2)]
        [x1, y1] = self.dec2screen(x1, y1)
        [x2, y2] = self.dec2screen(x2, y2)

        angle = atan2(y2 - y1, x2 - x1)
        self.draw.line((x1, y1, x2, y2), fill="black")
        # первая стрелка
        # координаты левого крыла
        (lwx, lwy) = (x2 - headlen * cos(angle - pi / headwid), y2 - headlen * sin(angle - pi / headwid))
        # координаты правого крыла
        (rwx, rwy) = (x2 - headlen * cos(angle + pi / headwid), y2 - headlen * sin(angle + pi / headwid))
        lines = [(x2, y2), (lwx, lwy), (rwx, rwy)]
        self.draw.polygon(lines, fill="black")
        # вторая стрелка
        # координаты левого крыла
        (lwx, lwy) = (x1 + headlen * cos(angle - pi / headwid), y1 + headlen * sin(angle - pi / headwid))
        # координаты правого крыла
        (rwx, rwy) = (x1 + headlen * cos(angle + pi / headwid), y1 + headlen * sin(angle + pi / headwid))
        lines = [(x1, y1), (lwx, lwy), (rwx, rwy)]
        self.draw.polygon(lines, fill="black")

    # функция рисующая линию с незакрашенной стрелкой в конце
    # принимаемые координаты в декартовой системе
    # в сантиметрах
    def Line(self, x1, y1, x2, y2):
        [x1, y1, x2, y2] =  [self.sm2px(x1), self.sm2px(y1), self.sm2px(x2), self.sm2px(y2)]
        [x1, y1] = self.dec2screen(x1, y1)
        [x2, y2] = self.dec2screen(x2, y2)

        self.draw.line((x1, y1, x2, y2), fill="black")

    # функция рисующая текст
    # принимаемые координаты в декартовой системе
    # в сантиметрах   
    def Text(self, text, x, y):
        [x, y] =  [self.sm2px(x), self.sm2px(y)]
        [x, y] = self.dec2screen(x, y)
        self.draw.text((x + 4, y - 18), text, font=self.font, fill="black")

    def BottomAlignText(self, text, x, y):
        [x, y] =  [self.sm2px(x), self.sm2px(y)]
        [x, y] = self.dec2screen(x, y)
        (textw, texth) = self.font.getsize(text)
        self.draw.text((x - (textw / 2.0), y), text, font=self.font, fill="black")

    def LeftAlignText(self, text, x, y):
        [x, y] =  [self.sm2px(x), self.sm2px(y)]
        [x, y] = self.dec2screen(x, y)
        (textw, texth) = self.font.getsize(text)
        self.draw.text((x - textw - 2, y - (texth / 2.0)), text, font=self.font, fill="black")

    def RightAlignText(self, text, x, y):
        [x, y] =  [self.sm2px(x), self.sm2px(y)]
        [x, y] = self.dec2screen(x, y)
        (textw, texth) = self.font.getsize(text)
        self.draw.text((x + 2, y - (texth / 2.0)), text, font=self.font, fill="black")

    def Polygon(self, xy):
        screen_xy = [self.dec2screen(self.sm2px(x), self.sm2px(y)) for x, y in xy]
        self.draw.polygon(screen_xy, outline="black")

    def TextSize(self, text):
        return self.font.getsize(text)