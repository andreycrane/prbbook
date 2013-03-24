#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
	name = models.CharField(max_length = 10, verbose_name = u"Индекс", unique = True)

	class Meta:
		verbose_name = u"Група"
		verbose_name_plural = u"Группы"

	def __unicode__(self):
		return u"%s" % self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    group = models.ForeignKey(Group, blank = True, verbose_name = u"Группа")

    class Meta:
    	verbose_name = u"Пользовательские данные"
    	verbose_name_plural = u"Пользовательские данные"
