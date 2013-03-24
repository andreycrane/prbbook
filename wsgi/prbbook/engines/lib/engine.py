# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from draw import DesignDraw

class Engine(object):
	__metaclass__ = ABCMeta

	def get_image(self, width = 400.0, height = 400.0, stage = 1):
		"""
		Возвращает сгенерированное изображение PIL Image.
		"""
		# создаем объект для рисования
		draw = DesignDraw(1000, 1000)
		draw = self.draw(draw, stage)
		draw.Crop()
		(im_width, im_height) = draw.Size()
		print im_width, im_height

		alpha_width = int((width * draw.alpha) / im_width)
		alpha_height = int((height * draw.alpha) / im_height)
		draw = DesignDraw(1000, 1000, min(alpha_width, alpha_height))
		draw = self.draw(draw, stage)
		draw.Crop()
		return draw.im

	@abstractmethod
	def randomize_in_params(self):
		"""
		Производит генерацию исходных данных к задаче
		"""

	@abstractmethod
	def get_store_str(self):
		"""
		Возвращает строку с исходными данными для
		хранения в БД. Предпологается JSON
		"""

	@abstractmethod
	def load_store_str(self, store_str):
		"""
		Загружает данные в движок из строки JSON, формата
		данного движка
		"""

	@abstractmethod
	def load_preview_params(self):
		"""
		Загружает данные для предосмотра задачи.
		"""

	@abstractmethod
	def get_in_params(self):
		"""
		Возвращает исходные данные к задаче.
		"""

	@abstractmethod
	def get_out_params(self):
		"""
		Возвращает данные решения.
		"""

	@abstractmethod
	def calculate(self):
		"""
		Производит расчет задачи.
		"""

	@abstractmethod
	def draw(self, draw, stage):
		"""
		Прозводит отрисову задачи. Возвращает объект класса DesignDraw.
		"""

	@abstractmethod
	def adjust(self):
		"""
		Производит корректировку исходных данных задачи.
		"""

	@abstractmethod
	def validate(self):
		"""
		Проверка заданных исходных данных к задаче.
		"""