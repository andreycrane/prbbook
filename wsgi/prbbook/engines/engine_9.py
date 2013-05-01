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
		pass

	def get_store_str(self):
		pass

	def get_in_params(self):
		params = [
			{'Длины участков':
				[
					('l<sub>1</sub>', self.l1),
					('l<sub>2</sub>', self.l2),
					('l<sub>3</sub>', self.l3)
				]
			},
			{'Силы действующие на участках':
                [
                    ('P<sub>1</sub>',self.P1),
                    ('P<sub>2</sub>',self.P2),
                    ('P<sub>3</sub>',self.P3)
                ]
            },
            {'Другие параметры':
            	[
            		('&sigma;',self.Qt),
            		('n<sub>T</sub>', self.nt),
            		('E', self.E, 'noedit')
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
			{'Значения допускаемого няпржения':
				[
					('[&sigma;]', self.Q),
					('d<sub>1</sub>', self.d1)
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

	def draw(self, draw, stage):
		(x, y) = (5, 5)
		(l1, l2, l3,
		 df1, df2, a) = (self.l1, self.l2, self.l3, 
		 				 self.df1, self.df2, self.a)
		if stage == 1:
			# отрисовка боковой проекции фигуры
			draw.Line(x, y + 5, x, y + 11)
			draw.Rect(x, y + 6, l3, 3)
			draw.Rect(x + l3, y + 6.5, l2, 2)
			draw.Rect(x + l3 + l2, y + 6, l1, 3)
			# граница третьего участка
			draw.Line(x + l3, y + 9, x + l3, y + 11)
			# граница второго участка
			draw.Line(x + l3 + l2, y + 9, x + l3 + l2, y + 11)
			# граница первого участка
			draw.Line(x + l3 + l2 + l1, y + 9, x + l3 + l2 + l1, y + 11)
			# длина третьего участка
			draw.Line2FillArrow(x, y + 10, x + l3, y + 10)
			draw.TopAlignText("l3", x + (l3 / 2.0), y + 10)
			# длина второго учатска
			draw.Line2FillArrow(x + l3, y + 10, x + l3 + l2, y + 10)
			draw.TopAlignText("l2", x + l3 + (l2 / 2.0), y + 10)
			# длина третьего участка
			draw.Line2FillArrow(x + l3 + l2, y + 10, x + l3 + l2 + l1, y + 10)
			draw.TopAlignText("l1", x + l3 + l2 + (l1 / 2.0), y + 10)
			# направление сил
			# P1
			draw.LineFillArrow(x + l3 + l2 + l1, y + 7.5, x + l3 + l2 + l1 + 1, y + 7.5, width = 2)
			draw.Text("P1", x + l3 + l2 + l1 + 1, y + 7.5)
			# P2
			draw.LineFillArrow(x + l3 + l2, y + 7.5, x + l3 + l2 + 0.7, y + 7.5, width = 2)
			draw.Text("P2", x + l3 + l2 + 0.7, y + 7.5)
			# P3
			draw.LineFillArrow(x + l3, y + 7.5, x + l3 + 0.7, y + 7.5, width = 2)
			draw.Text("P3", x + l3 + 0.7, y + 7.5)
			# рисуем контуры и размеры первой фигуры
			draw.Rect(x, y, 3, 3)
			draw.Line(x, y, x - 1, y)
			draw.Line(x, y + 3, x - 1, y + 3)
			draw.Line2FillArrow(x - 0.5, y, x - 0.5, y + 3)
			draw.LeftAlignText("a", x - 0.5, y + 1.5)
			draw.Line(x, y, x, y - 1)
			draw.Line(x + 3, y, x + 3, y - 1)
			draw.Line2FillArrow(x, y - 0.5, x + 3, y - 0.5)
			draw.BottomAlignText("a", x + 1.5, y - 0.5)
			# рисукм контуры и размеры второй фигуры
			draw.Circle(x + 4.5, y + 1.5, 1)
			draw.Line(x + 4, y + 1.5, x + 4, y - 1)
			draw.Line(x + 5, y + 1.5, x + 5, y - 1)
			draw.Line2FillArrow(x + 4, y - 0.5, x + 5, y - 0.5)
			draw.BottomAlignText("d2", x + 4.5, y - 0.5)
			# рисуем контуры и размеры третьей фигуры
			draw.Circle(x + 7, y + 1.5, 1.5)
			draw.Line(x + 7 - (1.5 / 2.0), y + 1.5, x + 7 - (1.5 / 2.0), y - 1)
			draw.Line(x + 7 + (1.5 / 2.0), y + 1.5, x + 7 + (1.5 / 2.0), y - 1)
			draw.Line2FillArrow(x + 7 - (1.5 / 2.0), y - 0.5, x + 7 + (1.5 / 2.0), y - 0.5)
			draw.BottomAlignText("d2", x + 7, y - 0.5)
		elif stage == 2:
			# отрисовка боковой проекции фигуры
			draw.Line(x, y + 5, x, y + 11)
			draw.Rect(x, y + 6, l3, 3)
			draw.Rect(x + l3, y + 6.5, l2, 2)
			draw.Rect(x + l3 + l2, y + 6, l1, 3)
			# граница третьего участка
			draw.Line(x + l3, y + 9, x + l3, y + 11)
			# граница второго участка
			draw.Line(x + l3 + l2, y + 9, x + l3 + l2, y + 11)
			# граница первого участка
			draw.Line(x + l3 + l2 + l1, y + 9, x + l3 + l2 + l1, y + 11)
			# длина третьего участка
			draw.Line2FillArrow(x, y + 10, x + l3, y + 10)
			draw.TopAlignText("l3", x + (l3 / 2.0), y + 10)
			# длина второго учатска
			draw.Line2FillArrow(x + l3, y + 10, x + l3 + l2, y + 10)
			draw.TopAlignText("l2", x + l3 + (l2 / 2.0), y + 10)
			# длина третьего участка
			draw.Line2FillArrow(x + l3 + l2, y + 10, x + l3 + l2 + l1, y + 10)
			draw.TopAlignText("l1", x + l3 + l2 + (l1 / 2.0), y + 10)
			# направление сил
			# P1
			draw.LineFillArrow(x + l3 + l2 + l1, y + 7.5, x + l3 + l2 + l1 + 1, y + 7.5, width = 2)
			draw.Text("P1", x + l3 + l2 + l1 + 1, y + 7.5)
			# P2
			draw.LineFillArrow(x + l3 + l2, y + 7.5, x + l3 + l2 + 0.7, y + 7.5, width = 2)
			draw.Text("P2", x + l3 + l2 + 0.7, y + 7.5)
			# P3
			draw.LineFillArrow(x + l3, y + 7.5, x + l3 + 0.7, y + 7.5, width = 2)
			draw.Text("P3", x + l3 + 0.7, y + 7.5)
			# рисуем контуры и размеры первой фигуры
			draw.Rect(x, y, 3, 3)
			draw.Line(x, y, x - 1, y)
			draw.Line(x, y + 3, x - 1, y + 3)
			draw.Line2FillArrow(x - 0.5, y, x - 0.5, y + 3)
			draw.LeftAlignText("a", x - 0.5, y + 1.5)
			draw.Line(x, y, x, y - 1)
			draw.Line(x + 3, y, x + 3, y - 1)
			draw.Line2FillArrow(x, y - 0.5, x + 3, y - 0.5)
			draw.BottomAlignText("a", x + 1.5, y - 0.5)
			# рисукм контуры и размеры второй фигуры
			draw.Circle(x + 4.5, y + 1.5, 1)
			draw.Line(x + 4, y + 1.5, x + 4, y - 1)
			draw.Line(x + 5, y + 1.5, x + 5, y - 1)
			draw.Line2FillArrow(x + 4, y - 0.5, x + 5, y - 0.5)
			draw.BottomAlignText("d2", x + 4.5, y - 0.5)
			# рисуем контуры и размеры третьей фигуры
			draw.Circle(x + 7, y + 1.5, 1.5)
			draw.Line(x + 7 - (1.5 / 2.0), y + 1.5, x + 7 - (1.5 / 2.0), y - 1)
			draw.Line(x + 7 + (1.5 / 2.0), y + 1.5, x + 7 + (1.5 / 2.0), y - 1)
			draw.Line2FillArrow(x + 7 - (1.5 / 2.0), y - 0.5, x + 7 + (1.5 / 2.0), y - 0.5)
			draw.BottomAlignText("d2", x + 7, y - 0.5)
		return draw

if __name__ == "__main__":
	logging.basicConfig(level = logging.DEBUG)

	engine = ProblemEngine()
	engine.load_preview_params()
	engine.calculate()
	engine.get_image(stage = 2).show()