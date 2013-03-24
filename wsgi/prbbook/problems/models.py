#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# импортируем менеджер движков
from prbbook import settings

engines = settings.EngineManager.get_choices()


class ProblemGroup(models.Model):
	name = models.CharField(max_length = 255, blank = True, default = u"Без названия", 
							verbose_name = u"Название группы заданий")
	date = models.DateField(auto_now = True, auto_now_add = True, verbose_name = u"Дата создания")

	class Meta:
		verbose_name = u"Группа заданий"
		verbose_name_plural = u"Группы заданий"
		ordering = ["-date", "-name"]

	def __unicode__(self):
		return u"%s %s" % (self.name, self.date)

class Problem(models.Model):
	user = models.ForeignKey(User, verbose_name = u"Пользователь")
	problem_engine = models.CharField(max_length = 255, choices = engines, verbose_name = u"Задача")
	problem_in_params = models.TextField(verbose_name = u"Исходные данные")
	group = models.ForeignKey(ProblemGroup, verbose_name = u"Группа")

	class Meta:
		verbose_name = u"Задание"
		verbose_name_plural = u"Задания"

	def __unicode__(self):
		return u"%s %s %s %s" % (self.user, self.problem_engine, self.problem_in_params, self.problem_out_params)
