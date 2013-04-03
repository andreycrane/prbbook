#!/usr/bin/env python
# -*- coding: utf-8 -*-
from engine import Engine
import logging
# менеджер движков
class EngineManager:
	"""
	Класс менеджера классов задач. Регистрирует новые классы
	задач, предоставляет интерфейс для форм выбора задач.
	"""
	engines = []

	@classmethod
	def add_engine(cls, engine_cls):
		"""
		Регистрация нового класса задачи.
		"""
		if issubclass(engine_cls, Engine):
			cls.engines.append(engine_cls)

	@classmethod
	def get_choices(cls):
		"""
		Возвращает кортеж со списом имен задач и классов их реализующих.
		Используется в формах.
		"""
		return [(engine.short_name, engine.name) for engine in cls.engines]

	@classmethod
	def get_subcat_choices(cls):
		"""
		Идентичен get_choices, но классы задач сортируются по категориям.
		"""
		cats = {}
		for engine in cls.engines:
			if not cats.get(engine.category, False):
				cats[engine.category] = []
			cats[engine.category].append((engine.short_name, engine.name))
		logging.debug("Subcat choices: %s" % cats)
		return [[category, cats[category]] for category in cats]

	@classmethod
	def get_engine(cls, short_name):
		"""
		Возвращает класс задачи указанный по короткому имени (идентификатору).
		"""
		for engine in cls.engines:
			if engine.short_name == short_name:
				return engine