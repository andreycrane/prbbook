#!/usr/bin/env python
# -*- coding: utf-8 -*-
from engine import Engine
# менеджер движков
class EngineManager:
	engines = []

	@classmethod
	def add_engine(cls, engine_cls):
		if issubclass(engine_cls, Engine):
			cls.engines.append(engine_cls)

	@classmethod
	def get_choices(cls):
		return [(engine.short_name, engine.name) for engine in cls.engines]

	@classmethod
	def get_engine(cls, short_name):
		for engine in cls.engines:
			if engine.short_name == short_name:
				return engine